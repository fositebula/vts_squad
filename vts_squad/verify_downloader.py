# coding=utf-8
import sh
import os
from django.conf import settings
import re
import multiprocessing

DOWNLOAD_DIR = '/home/local/SPREADTRUM/pl.dong/PycharmProjects/vts_test/vts_squad/static/vts_squad/android_imgs/'


def make_download_dir(verify_url):
    verifyid = re.search(r'/([0-9]+)/', verify_url).group(1)
    target_dir = os.path.join(DOWNLOAD_DIR, verifyid)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    return target_dir


def verify_dowloader(target_url):
    where_to_download = make_download_dir(target_url)
    my_file_name = target_url.split('/')[-1]
    target = os.path.join(where_to_download, my_file_name)
    target_log = os.path.join(where_to_download, my_file_name+'.log')

    #如果存在就gz文件就不下载
    if not os.path.exists(where_to_download):
        sh.wget([target_url, "--tries=0", "--output-document=" + target,
             "--continue", "--timeout=1800", "--output-file=" + target_log])

    sh.tar(['xvzf', target, '-C', where_to_download])
    k, v, files = next(os.walk(where_to_download))
    verifyid = re.search(r'/([0-9]+)/', target_url).group(1)
    return verifyid, files


def download_file(verify_url):
    p = multiprocessing.Process(target=verify_dowloader, args=verify_url, name='download_verify')
    p.start()
    verifyid = re.search(r'/([0-9]+)/', verify_url).group(1)
    return p.pid, os.path.join(DOWNLOAD_DIR, verifyid)