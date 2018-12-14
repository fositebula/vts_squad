# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from models import *

import requests
from requests.exceptions import ConnectionError

from jinja2 import Template
import yaml
from StringIO import StringIO

from task import submit_to_squad

import traceback
from BuildInfo import BuildInfo
# Create your views here.
def index(request):
    return render(request, 'job_list.html', {})

# @require_http_methods
def job_submit(request):
    if request.method == "GET":
        vv = VtsVersion.objects.all()
        render_body = {
            'vts_version':vv
        }
        from django.conf import settings
        # make_download_dir()
        print settings.VTS_TEST_IMGS_DIR
        return render(request, 'job_submit.html', render_body)
    else:
        vts_version = request.POST.get('vts-version')
        vts_module = request.POST.get('vts-module')
        verify_url = request.POST.get('verify-url')
        pac_url = request.POST.get('pac-url')
        
        try:
            r = requests.head(verify_url)
            print r
            if r.status_code > 300:
                vv = VtsVersion.objects.all()
                message = {
                    'message':'Verify URL not correct!',
                    'vts_version':vv,
                    'vts_v': VtsVersion.objects.get(id=vts_version),
                    'vts_module': vts_module,
                    'verify_url':verify_url,
                    'pac_url':pac_url
                }
                return render(request, 'job_submit.html', message)
        except ConnectionError:
            vv = VtsVersion.objects.all()
            message = {
                'message': 'Connect error',
                    'vts_version':vv,
                    'vts_v': VtsVersion.objects.get(id=vts_version),
                    'vts_module': vts_module,
                    'verify_url':verify_url,
                    'pac_url':pac_url
            }
            return render(request, 'job_submit.html', message)
        # print vts_version, vts_module, verify_url, pac_url
        try:
            device_type = LavaDeviceType.objects.get(pac_url=pac_url)
        except LavaDeviceType.DoesNotExist:
            vv = VtsVersion.objects.all()
            message= {
                'message':'Not device type for %s'%pac_url,
                'vts_version':vv,
                    'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url':verify_url,
                'pac_url':pac_url
            }
            return render(request, 'job_submit.html', message)

        vts_url = VtsVersion.objects.get(id=vts_version)
        print vts_url.tar_url
        token = device_type.squad_api
        template = Template(device_type.template)
        lava_job = template.render(vts_module=vts_module, vts_version=vts_url.tar_url, img_url=device_type.worker05_pac, imgs=device_type.deploy_imgs.all())
        # try:
        #     lava_job_string_io = StringIO(lava_job)
        #     # job_values = yaml.load(lava_job_string_io)
        #     # pid, download_dir = download_file(verify_url)
        # except:
        #     vv = VtsVersion.objects.all()
        #     message = {
        #         'message':traceback.format_exc(),
        #             'vts_v': VtsVersion.objects.get(id=vts_version),
        #             'vts_version':vv,
        #             'vts_module': vts_module,
        #             'verify_url':verify_url,
        #             'pac_url':pac_url
        #     }
        #     return render(request, 'job_submit.html', message)

        try:

            buildinfo = BuildInfo('/'.join(verify_url.split('/')[:8]))
            verifyinfos = buildinfo.get_all_infos()

            job = Job(jenkins_job=verifyinfos['JOB'], jenkins_build_num=verifyinfos['BUILD_NUMBER'],
                      jenkins_node=verifyinfos['NODE'], jenkins_trigger=verifyinfos['TRIGGER'],
                      jenkins_build_type=verifyinfos['BUILD_TYPE'], jenkins_lavatest=verifyinfos['LAVA_TEST'],
                      jenkins_changes=verifyinfos['CHANGES'], jenkins_list=verifyinfos['BUILD_LIST'])
            job.save()
            print job.id

            # http://cmverify.spreadtrum.com:8080/jenkins/job/gerrit_do_verify_sprdroidp/26393//artifact/sps.image/sprdroid9.0_trunk/sp9832e_1h10_gofu-userdebug-gms.tar.gz
            verify_url_list = verify_url.split('/')
            squad_job_name = '_'.join([verify_url_list[-2], verify_url_list[-1].split('.')[0], vts_module])
            print squad_job_name
            res = submit_to_squad.delay(verify_url, lava_job, device_type.squad_api.api.format(qa_server_build=squad_job_name),
                                  'http://10.0.70.105:8000', token.token, )

            return render(request, 'successfully.html', {'result':res})
        except:
            vv = VtsVersion.objects.all()
            message = {
                'message':traceback.format_exc(),
                    'vts_v': VtsVersion.objects.get(id=vts_version),
                    'vts_version':vv,
                    'vts_module': vts_module,
                    'verify_url':verify_url,
                    'pac_url':pac_url
            }
            return render(request, 'job_submit.html', message)

def job_info(request):
    return render(request, 'job_info.html', {})

