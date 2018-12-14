import requests
import traceback
from celery import Celery
from  StringIO import StringIO
import yaml
from vts_squad.models import LavaDeviceType, DelployImgs

from verify_downloader import verify_dowloader

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

celery_app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

def _submit_to_squad(lava_job, qa_server_api, qa_server_base, qa_token, quiet=False):
    headers = {
        "Auth-Token": qa_token
    }
    try:
        data = {
            "definition": lava_job,
            "backend": urlsplit('http://sprd_lava_01').netloc  # qa-reports backends are named as lava instances
        }
        print("Submit to: %s" % qa_server_api)
        results = requests.post(qa_server_api, data=data, headers=headers, timeout=31)
        if results.status_code < 300:
            print("%s/api/testjobs/%s" % (qa_server_base, results.text))
            return "%s/api/testjobs/%s" % (qa_server_base, results.text)
        else:
            print(results.status_code)
            print(results.text)
    except requests.exceptions.RequestException as err:
        print traceback.format_exc()
        print("QA Reports submission failed")
        if not quiet:
            print("offending job definition:")
            print(lava_job)

@celery_app.task
def submit_to_squad(verifyurl, lava_job, qa_server_api, qa_server_base, qa_token, quiet=False):
    #TODO:First: download images and decompress
    verifyid, files = verify_dowloader(verifyurl)
    pre_url = 'http://10.0.70.92:8000/vts/static/'

    like_file = StringIO(lava_job)
    d_values = yaml.load(like_file)
    device_type = d_values['device_type']

    dtd = LavaDeviceType.objects.get(name=device_type)

    for f in files:
        try:
            d = dtd.deploy_imgs.all().get(img=f)
        except DelployImgs.DoesNotExist:
            continue
        d_values['actions'][3]['deploy']['images'][d.name]['url'] = pre_url + verifyid+'/'+f

    d_values['job_name'] = 'kernel VTS {}'.format(verifyid)
    like_file.close()
    lava_job = StringIO('')
    yaml.dump(d_values, lava_job)
    lava_job.seek(0)
    lava_job_str = lava_job.read()
    lava_job.close()

    return _submit_to_squad(lava_job_str, qa_server_api, qa_server_base, qa_token)
