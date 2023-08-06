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

xxl_job_admin_url = 'http://192.168.1.48:8666/xxl-job-admin'


# 执行作业
def run_job(job_conf_file='./job.conf'):
    # 检查作业配置文件是否存在
    if not os.path.exists(job_conf_file):
        print('作业配置文件不存在')
        return False

    # 读取作业配置内容
    with open(job_conf_file, encoding='utf-8') as file:
        content = file.read()
    job_conf = json.loads(content)

    # 清空远程作业文件
    for item in redis_client.hscan_iter('job:%s:files' % job_conf['name']):
        result = fdfs_client.delete_file(item[1].encode())
        if result[0] == 'Delete file successed.':
            redis_client.hdel('job:%s:files' % job_conf['name'], item[0])

    # 清空输出文件
    for item in redis_client.hscan_iter('job:%s:output' % job_conf['name']):
        result = fdfs_client.delete_file(item[1].encode())
        if result[0] == 'Delete file successed.':
            redis_client.hdel('job:%s:output' % job_conf['name'], item[0])

    # 获取本地作业文件
    job_files = []
    for f in job_conf['files']:
        job_files.extend(glob.glob(f))
    # 上传作业文件到fdfs
    for f_name in job_files:
        result = fdfs_client.upload_by_filename(f_name)
        if 'Status' in result and result['Status'] == 'Upload successed.':
            remote_file_id = result['Remote file_id'].decode()
            remote_file_size = result['Uploaded size']
            redis_client.hset('job:%s:files' % job_conf['name'], f_name, remote_file_id)
    # 保存配置文件
    redis_client.hset('job:%s:info' % job_conf['name'], 'job_conf', content)

    # 获取xxl-job的token
    cookie = {}
    body = {
        'userName': 'admin',
        'password': '123456'
    }

    resp = requests.post('%s/login' % xxl_job_admin_url, data=body)
    cookies = resp.cookies
    cookie = requests.utils.dict_from_cookiejar(cookies)

    # 触发xxl-job任务
    body = {
        'id': '5',
        'executorParam': job_conf['name'],
        'addressList': ''
    }
    requests.post('%s/jobinfo/trigger' % xxl_job_admin_url, data=body, cookies=cookie)


if __name__ == "__main__":
    job_conf_file = sys.argv[1]
    run_job(job_conf_file)


