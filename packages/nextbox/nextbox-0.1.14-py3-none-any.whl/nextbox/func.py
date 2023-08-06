import os


def run_server(conf_fp, port=8222):
    os.system(f"nats-server --js -m {port} -c {conf_fp}")
