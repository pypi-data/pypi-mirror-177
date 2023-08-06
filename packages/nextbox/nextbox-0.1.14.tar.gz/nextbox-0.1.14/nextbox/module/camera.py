import json

import cv2
import numpy as np
import time
import os
from loguru import logger


class Camera:
    def __init__(self, uri, record_dir, record_video_enable=False, record_video_fps=30,
                 record_clip_duration=600, enable_time_tag=True, time_tag_color=(0, 0, 0)):
        """
        摄像头模块
        :param uri: 摄像头地址
        :param record_dir: 记录保存路径
        :param record_video_enable: 是否开启视频记录
        :param record_video_fps: 视频记录的fps
        :param record_clip_duration: 视频记录片段的时长
        :param enable_time_tag: 是否开启时间字符串显示
        :param time_tag_color: 时间戳字符串颜色
        """
        self._uri = uri
        # 连续尝试重连最大次数
        self.re_conn_max_times = 5
        self.cap = cv2.VideoCapture(self._uri)
        self.record_dir = record_dir

        # 拍摄图片保存路径
        self.record_pic_dir = os.path.join(self.record_dir, "pic")
        # 拍摄视频保存路径
        self.record_video_dir = os.path.join(self.record_dir, "video")
        # 初始化目录
        os.makedirs(self.record_pic_dir, exist_ok=True)
        os.makedirs(self.record_video_dir, exist_ok=True)

        # 摄像头宽高信息
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 当前帧
        self._frame = None
        self._frame_at = time.time_ns()
        time.time()

        # 视频保存相关
        self.record_video_enable = record_video_enable
        self.record_video_fps = record_video_fps
        self.record_clip_duration = record_clip_duration
        self.video_writer = None
        self._start_record_at = -1

        # 画面配置
        self.enable_time_tag = enable_time_tag
        self.time_tag_color = time_tag_color

        # 写入元数据
        self._dump_metadata()

    def _dump_metadata(self):
        metadata = {
            "uri": self._uri,
            "size": (self.w, self.h),
            "record_video_enable": self.record_video_enable,
            "record_video_fps": self.record_video_fps,
            "record_clip_duration": self.record_clip_duration,
            "enable_time_tag": self.enable_time_tag,
            "start_at": self._crt_time_str()
        }

        # 写入元信息
        metadata_fp = os.path.join(self.record_dir, "metadata.json")
        with open(metadata_fp, 'w') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)

    def _crt_time_str(self):
        """
        返回当前时间的字符串表示
        示例：'2022-11-13_15-34-29'
        :return:
        """
        return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    def _cft_fn(self):
        return f"{self._crt_time_str()}_{int(time.time() % 1 * 1000)}"

    def crt_img_fn(self):
        return f"{self._cft_fn()}.jpg"

    def crt_video_fn(self):
        return f"{self._cft_fn()}.mp4"

    def is_open(self):
        return self.cap.isOpened()

    def release(self):
        logger.info("release")
        self.cap.release()

    def _re_conn(self):
        """
        TODO 断线重连机制
        :return:
        """
        pass

    def _read(self):
        """
        读取摄像头画面
        :return:
        """
        ret, _frame = self.cap.read()

        # 添加画面内容
        if self.enable_time_tag:
            _frame = self._time_str_tag(_frame)

        self._frame = _frame
        self._frame_at = time.time_ns()

        # 记录到视频文件
        if self.record_video_enable:
            self._record_video(self._frame)

        # 尝试重连
        re_conn_times = 0
        while not ret:
            if re_conn_times > self.re_conn_max_times:
                raise Exception(f"camera {self._uri} connect error!")
            # 尝试重连
            self._re_conn()
            ret, self._frame = self.cap.read()
            self._frame_at = time.time_ns()
            re_conn_times += 1

        return self._frame, self._frame_at

    def read(self):
        """
        读取摄像头画面
        :return:
        """
        frame, time_at_ns = self._read()
        return frame

    def take_picture(self):
        """
        拍摄画面
        :return:
        """
        logger.info("take_picture")
        if self.record_dir:
            fp = os.path.join(self.record_pic_dir, f"{self._cft_fn()}.jpg")
            frame = self._process_display_frame(self._frame)
            cv2.imwrite(fp, frame)
        else:
            raise Exception(f"record_dir is {self.record_dir}, please set!")

    def show(self):
        while self.is_open():
            frame = self.read()
            frame = self._process_display_frame(frame)  # 显示读取到的这一帧画面
            cv2.imshow('frame', frame)
            key = cv2.waitKey(25)  # 等待一段时间，并且检测键盘输入
            if key == ord(' '):
                # 拍照
                c.take_picture()
            elif key == ord('q'):  # 若是键盘输入'q',则退出，释放视频
                # 退出
                c.release()  # 释放视频
                break

    def _process_display_frame(self, frame):
        return frame

    def _record_video(self, frame):
        """
        写入视频文件
        :param frame:
        :return:
        """
        self._recreate_video_writer()
        # 写入每一帧
        frame = self._process_display_frame(frame)
        self.video_writer.write(frame)

    def _recreate_video_writer(self):
        """
        开始录制
        :return:
        """
        if time.time() - self._start_record_at > self.record_clip_duration:
            self._start_record_at = time.time()
            fp = os.path.join(self.record_video_dir, f"{self._cft_fn()}.mp4")
            if self.video_writer is not None:
                self.video_writer.release()
            self.video_writer = cv2.VideoWriter(fp, cv2.VideoWriter_fourcc(*'mp4v'), self.record_video_fps,
                                                (self.w, self.h), True)
            logger.info(f"start record video > {fp}")

    def _time_str_tag(self, frame):
        """
        给视频画面添加时间戳
        :param frame:
        :return:
        """
        _t = time.localtime()
        time_str = f"{_t.tm_year}-{_t.tm_mon}-{_t.tm_mday} {_t.tm_hour}:{_t.tm_min:0>2d}:{_t.tm_sec:0>2d}"
        frame = cv2.putText(frame, time_str, (20, 40),
                            fontScale=1,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            color=self.time_tag_color,
                            thickness=1,
                            lineType=4)
        return frame


class MaskedCamera(Camera):
    """
    带有mask信息的摄像头
    """

    def __init__(self, uri, mask_points: list, record_dir, record_video_enable=False, record_video_fps=30,
                 record_clip_duration=600, enable_time_tag=True, time_tag_color=(0, 0, 0)):
        super().__init__(uri,
                         record_dir=record_dir,
                         record_video_enable=record_video_enable,
                         record_video_fps=record_video_fps,
                         record_clip_duration=record_clip_duration,
                         enable_time_tag=enable_time_tag,
                         time_tag_color=time_tag_color)

        if mask_points and len(mask_points) > 0:
            points = [[int(p[0]), int(p[1])] for p in mask_points]
            self.mask = cv2.fillPoly(np.zeros(shape=(self.h, self.w), dtype=np.uint8), [np.array(points)], 1)
        else:
            self.mask = np.ones(shape=(self.h, self.w), dtype=np.uint8)

    def _process_display_frame(self, frame):
        _mask = (1 - self.mask) * 255
        _mask = cv2.cvtColor(_mask, cv2.COLOR_GRAY2RGB)
        return cv2.addWeighted(frame, 1, _mask, 0.3, 0)


if __name__ == '__main__':
    c = Camera(uri=1, record_dir="record", record_video_enable=True, record_clip_duration=10, enable_time_tag=False)
    # c = MaskedCamera(uri=1,
    #                  mask_points=[[0, 0], [0, 100], [100, 100], [100, 0]],
    #                  record_dir="record",
    #                  record_video_enable=True,
    #                  record_clip_duration=10)
    # c.read()
    # c.take_picture()
    # frame = c.read()
    # cv2.imwrite("./test.jpg", frame)
    c.show()
