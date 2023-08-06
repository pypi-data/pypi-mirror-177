from fdfs_client.client import Fdfs_client
import redis
import glob
import requests
import json
import sys
import os

tracker_conf = {
    'host_tuple': ['192.168.1.47'],
    'port': 22122,
    'timeout': 60,
    'use_storage_id': False
}

fdfs_client = Fdfs_client(tracker_conf)

redis_client = redis.Redis(host='192.168.1.48', port=16380, password='knn3.14159', decode_responses=True)


def run_xxl_job(job_name):
    # 获取配置文件
    content = redis_client.hget('job:%s:info' % job_name, 'job_conf')
    job_conf = json.loads(content)

    # 下载作业文件
    for item in redis_client.hscan_iter('job:%s:files' % job_name):
        fdfs_client.download_to_file(item[0], item[1].encode())

    # 执行验证文件
    os.system(job_conf['command'])




if __name__ == "__main__":
    job_conf_file = sys.argv[1]
    run_xxl_job(job_conf_file)