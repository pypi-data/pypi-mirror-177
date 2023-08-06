import os
import time


class los:
    """
    local object storage
    """

    def __init__(self, base_dir="./los", valid_time=60):
        """
        初始化
        :param base_dir: 数据根路径
        :param valid_time: 数据有效期（秒）
        """
        self.base_dir = base_dir
        self.valid_time = valid_time
        os.makedirs(self.base_dir, exist_ok=True)

    def set(self, key: str, value):
        """
        写入数据（如果存在则覆盖）
        :param key:
        :param value:
        :return:
        """
        assert not key.startswith(os.sep)
        assert ".." not in key
        if os.sep in key:
            tar_dir = os.path.join(self.base_dir, os.sep.join(key.split(os.sep)[:-1]))
            os.makedirs(tar_dir, exist_ok=True)
        fp = os.path.join(self.base_dir, key)
        with open(fp, "wb") as f:
            f.write(value)

    def get(self, key, mode="rb"):
        """
        读取数据
        :param key:
        :param mode:
        :return:
        """
        fp = os.path.join(self.base_dir, key)
        self._is_valid(key)

        with open(fp, mode) as f:
            return f.read()

    def get_filepath(self, key):
        """
        获取对象绝对路径
        :param key:
        :return:
        """
        self._is_valid(key)
        fp = os.path.join(self.base_dir, key)
        return fp

    def new_writeable_filepath(self, key):
        """
        获取一个可以被写入的文件路径
        :param key:
        :return:
        """
        fp = os.path.join(self.base_dir, key)
        assert not os.path.exists(fp)
        return fp

    def gc(self):
        for root, dirs, files in os.walk(self.base_dir):  # 对文件夹进行遍历
            for name in files:
                fp = os.path.join(root, name)
                if time.time() >= self.valid_time + os.path.getmtime(fp):
                    os.remove(fp)

    def _is_valid(self, key):
        """
        当前key是否有效
        :param key:
        :return:
        """
        fp = os.path.join(self.base_dir, key)
        assert os.path.exists(fp)
        return time.time() < self.valid_time + os.path.getmtime(fp)
