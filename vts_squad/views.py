# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import requests
from jinja2 import Template
import yaml
from StringIO import StringIO
import traceback
import xmlrpc.client

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *

from requests.exceptions import ConnectionError

from task import submit_to_squad

from BuildInfo import BuildInfo


ITEM_NUM = 20
OLD_PAGE = 0
# Create your views here.
def index(request):
    global OLD_PAGE
    try:
        gg = GongGao.objects.get(id=1)
        if not gg.fabu_or_not:
            gonggao = ''
        else:
            gonggao = gg.content
    except GongGao.DoesNotExist:
        gonggao = ''

    jobs = Job.objects.all().order_by('-id')
    jobs_count = len(jobs)
    page = request.GET.get('page')
    page_length = request.GET.get('length')
    if not page:
        jobs = Job.objects.all().order_by('-id')[0: ITEM_NUM]
        return render(request, 'job_list.html', {'jobs': jobs, 'all_pages': jobs_count/ITEM_NUM,
                                                 'page': 0, 'jobs_count': jobs_count,
                                                 'page_length': ITEM_NUM, 'pre_page': 0,
                                                 'next_page': 1, 'gonggao':gonggao})

    page = int(page)
    page_length = int(page_length)
    pages = jobs_count / page_length

    start = page * page_length

    stop = start + page_length

    if stop > jobs_count:
        stop = jobs_count
    if start < 0:
        start = 0

    pre_page = page - 1
    if pre_page < 0:
        pre_page = 0
    next_page = page + 1
    if next_page > pages:
        next_page = pages

    jobs = Job.objects.all().order_by('-id')[start: stop]

    return render(request, 'job_list.html', {'jobs':jobs, 'all_pages':pages,
                                             'page':page, 'jobs_count':jobs_count,
                                             'page_length': page_length, 'pre_page': pre_page,
                                             'next_page': next_page, 'gonggao':gonggao})

def my_submit(request):
    global OLD_PAGE
    print request.user
    jobs = Job.objects.filter(user=request.user).order_by('-id')
    jobs_count = len(jobs)
    page = request.GET.get('page')
    page_length = request.GET.get('length')
    if not page:
        jobs = jobs.order_by('-id')[0: ITEM_NUM]
        return render(request, 'my_submit.html', {'jobs': jobs, 'all_pages': jobs_count/ITEM_NUM,
                                                 'page': 0, 'jobs_count': jobs_count,
                                                 'page_length': ITEM_NUM, 'pre_page': 0,
                                                 'next_page': 1})

    page = int(page)
    page_length = int(page_length)
    pages = jobs_count / page_length

    start = page * page_length

    stop = start + page_length

    if stop > jobs_count:
        stop = jobs_count
    if start < 0:
        start = 0

    pre_page = page - 1
    if pre_page < 0:
        pre_page = 0
    next_page = page + 1
    if next_page > pages:
        next_page = pages

    jobs = jobs.order_by('-id')[start: stop]
    return render(request, 'my_submit.html', {'jobs':jobs, 'all_pages':pages,
                                             'page':page, 'jobs_count':jobs_count,
                                             'page_length': page_length, 'pre_page': pre_page,
                                             'next_page': next_page})

# @require_http_methods
@login_required
def job_submit(request):
    if request.method == "GET":
        vv = VtsVersion.objects.all()
        pac_url = LavaDeviceType.objects.all()
        render_body = {
            'vts_version':vv,
            'pac_url':pac_url
        }
        return render(request, 'job_submit.html', render_body)
    else:
        vts_version = request.POST.get('vts-version')
        vts_module = request.POST.get('vts-module')
        verify_url = request.POST.get('verify-url')
        pac_url = request.POST.get('pac-url')

        if not vts_version:
            vv = VtsVersion.objects.all()
            message = {
                'message':'vts version is required!',
                'vts_version': vv,
                'vts_module': vts_module,
                'verify_url': verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)
        if not vts_module:
            vv = VtsVersion.objects.get(id=vts_version)
            message = {
                'message':'vts module is required!',
                'vts_version': vv,
                'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url': verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)


        if not verify_url:
            vv = VtsVersion.objects.get(id=vts_version)
            message = {
                'message':'verify url is required!',
                'vts_version': vv,
                'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url': verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)


        if not pac_url:
            vv = VtsVersion.objects.get(id=vts_version)
            message = {
                'message':'pac url is required!',
                'vts_version': vv,
                'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url': verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)

        project = verify_url.split('/')[-1].replace('.tar.gz', '')

        if project not in LavaDeviceType.objects.get(id=pac_url).pac_url:
            vv = VtsVersion.objects.get(id=vts_version)
            message = {
                'message':'verify url does not match pac url!',
                'vts_version': vv,
                'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url': verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)

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
                    'pac_url': LavaDeviceType.objects.all()
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
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)
        # print vts_version, vts_module, verify_url, pac_url
        try:
            device_type = LavaDeviceType.objects.get(id=pac_url)
        except LavaDeviceType.DoesNotExist:
            vv = VtsVersion.objects.all()
            message= {
                'message':'Not device type for %s'%pac_url,
                'vts_version':vv,
                'vts_v': VtsVersion.objects.get(id=vts_version),
                'vts_module': vts_module,
                'verify_url':verify_url,
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)

        vts_url = VtsVersion.objects.get(id=vts_version)
        print vts_url.tar_url
        token = device_type.squad_api
        template = Template(device_type.template)
        lava_job = template.render(vts_module=vts_module, vts_version=vts_url.tar_url, img_url=device_type.worker05_pac, imgs=device_type.deploy_imgs.all())

        try:

            buildinfo = BuildInfo('/'.join(verify_url.split('/')[:7]))
            verifyinfos = buildinfo.get_all_infos()

            job = Job(jenkins_job=verifyinfos['JOB'], jenkins_build_num=verifyinfos['BUILD_NUMBER'],
                      jenkins_node=verifyinfos['NODE'], jenkins_trigger=verifyinfos['TRIGGER'],
                      jenkins_build_type=verifyinfos['BUILD_TYPE'], jenkins_lavatest=verifyinfos['LAVA_TEST'],
                      jenkins_changes=verifyinfos['CHANGES'], jenkins_list=verifyinfos['BUILD_LIST'],
                      verify_url=verify_url, )
            job.user = request.user
            job.vts_version = VtsVersion.objects.get(id=vts_version)
            job.device_type = device_type
            job.vts_module = vts_module
            job.save()
            print job.id

            # http://cmverify.spreadtrum.com:8080/jenkins/job/gerrit_do_verify_sprdroidp/26393//artifact/sps.image/sprdroid9.0_trunk/sp9832e_1h10_gofu-userdebug-gms.tar.gz
            verify_url_list = verify_url.split('/')
            squad_job_name = '_'.join([verify_url_list[-2], verify_url_list[-1].split('.')[0], vts_module])
            print squad_job_name
            res = submit_to_squad.delay(job.id, verify_url, lava_job, device_type.squad_api.api.format(qa_server_build=squad_job_name),
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
                'pac_url': LavaDeviceType.objects.all()
            }
            return render(request, 'job_submit.html', message)

# @login_required
def job_resubmit(request):
    jid = request.GET.get('jid')
    print jid
    job = Job.objects.get(id=jid)
    new_job = Job.objects.create()

    new_job.user = job.user
    new_job.verify_url = job.verify_url
    new_job.jenkins_job = job.jenkins_job
    new_job.jenkins_build_num = job.jenkins_build_num
    new_job.jenkins_node = job.jenkins_node
    new_job.jenkins_trigger = job.jenkins_trigger
    new_job.jenkins_list = job.jenkins_list
    new_job.jenkins_build_type = job.jenkins_build_type
    new_job.jenkins_lavatest = job.jenkins_lavatest
    new_job.jenkins_changes = job.jenkins_changes
    new_job.download_compress_status = job.download_compress_status
    new_job.download_log = job.download_log
    new_job.vts_version = job.vts_version
    new_job.vts_module = job.vts_module
    new_job.device_type = job.device_type

    new_job.save()
    verify_url_list = job.verify_url.split('/')
    squad_job_name = '_'.join([verify_url_list[-2], verify_url_list[-1].split('.')[0], job.vts_module])
    try:
        res = submit_to_squad.delay(new_job.id, job.verify_url, job.lava_job_yaml,
                                    job.device_type.squad_api.api.format(qa_server_build=squad_job_name),
                                    'http://10.0.70.105:8000', job.device_type.squad_api.token, )
        return render(request, 'successfully.html', {'result': res})
    except:
        vv = VtsVersion.objects.all()
        message = {
            'message': traceback.format_exc(),
            'vts_v': job.vts_version,
            'vts_version': vv,
            'vts_module': job.vts_module,
            'verify_url': job.verify_url,
            'pac_url': LavaDeviceType.objects.all()
        }
        return render(request, 'job_submit.html', message)

def job_info(request):

    return render(request, 'job_info.html', {})

def job_info_detail(request, jid):
    job = Job.objects.get(id=jid)
    if not job.lava_job:
        log_file_name = job.verify_url.split('/')[-1]+'.log'

        log_file_path = os.path.join(settings.STATIC_ROOT, job.jenkins_build_num.strip("['").strip("']"), log_file_name)
        print settings.STATIC_URL
        print settings.STATIC_ROOT
        print log_file_path
        with open(log_file_path) as f:
            log_lines = f.readlines()
            log_lines.sort(reverse=True)
            for line in log_lines:
                schedule = re.findall('.+ ([0-9]+%) .+', line)
                if len(schedule):
                    break
            print schedule[0]
            return render(request, 'job_info.html', {'schedule':schedule[0]})


    jr = requests.get(job.lava_job).json()

    lava_job_url = jr.get('external_url')
    lava_job_id = jr.get('job_id')
    lava_job_submittime = jr.get('submitted_at')

    server = xmlrpc.client.ServerProxy("http://%s:%s@%s/RPC2" % ('apuser',
                                                                 '4q0arwon8xzacq89l4572l481d3h0xojhn3p2b27pj0smh64lfgzh4iy3f6670jp1undg3uq0j50qixnz4u46b3ry8csm8q0qc8f2ditatw4j4o66chw3cq0bkps0d5e',
                                                                 '10.0.70.142'))


    lava_job_status = server.scheduler.job_status(lava_job_id).get('job_status')
    if lava_job_status == "Complete":
        lava_job_log = requests.get(lava_job_url+'/log_file/plain')

        t_stringIO = StringIO(server.results.get_testjob_suites_list_yaml(lava_job_id))

        test_suit_names = map(lambda x:x.get('name'), yaml.load(t_stringIO))
        print test_suit_names, 'vts-'+job.vts_module

        lava_job_case_result_d = {}
        # if 'vts-'+job.vts_module in map(lambda x:x.split('_')[-1], test_suit_names):
        for name in test_suit_names:
            if 'vts-' in name:
                lava_job_case_result_y = server.results.get_testsuite_results_yaml(lava_job_id, name)
                status_strIO = StringIO(lava_job_case_result_y)
                lava_job_case_result_d = yaml.load(status_strIO)

        if lava_job_log.status_code > 300:
            lava_job_log = 'LAVA job not starting, please wait!'
        else:
            lava_job_log = lava_job_log.content
        render_body = {
            'job': job,
            'lava_job_url': lava_job_url,
            'lava_job_id': lava_job_id,
            'lava_job_submittime': lava_job_submittime,
            'lava_job_status': lava_job_status,
            'lava_job_log':lava_job_log,
            'lava_job_case_result':lava_job_case_result_d,
            'job_bread_crumb':'/vts/job_info/'+jid
        }

        return render(request, 'job_info.html', render_body)
    else:

        lava_job_log = 'LAVA job not starting, please wait!'

        render_body = {
            'job': job,
            'lava_job_url': lava_job_url,
            'lava_job_id': lava_job_id,
            'lava_job_submittime': lava_job_submittime,
            'lava_job_status': lava_job_status,
            'lava_job_log': lava_job_log,
            'lava_job_case_result': [],
            'job_bread_crumb':'/vts/job_info/'+jid

        }
        return render(request, 'job_info.html', render_body)

@login_required
def my_comment(request):
    return render(request, 'my_comment.html', {})