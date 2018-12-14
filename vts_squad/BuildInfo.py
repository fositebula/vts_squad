import urllib2
import re
from time import sleep

INFO_ENUM = {
    "JOB":"",
    "BUILD_NUMBER":"",
    "BUILD_ID":"",
    "NODE":"",
    "TRIGGER":"",
    "BUILD_LIST":"",
    "GERRIT_IDS":"",
    "BUILD_TYPE":"",
    "LAVA_TEST":"",
    "TEST_PARA":"",
    "TEST_CASE":"",
    "TEST_MODULE":"",
    "JOINT_LIST":"",
    "CHANGES":"",
    "BUILD_RESULT":"",
}

class BuildInfo(object):
    def __init__(self, buildinfo_url):
        # url http://10.0.64.29:8080/jenkins/job/gerrit_do_verify_sprdroidn/49938/
        # url http://10.0.64.29:8080/jenkins/job/gerrit_do_verify_sprdroidn/49938/artifact/buildinfo.log
        self.buildinfo_url = buildinfo_url + "/artifact/buildinfo.log"

    def load_info(self):
        open_retry = 600
        re_st = False
        while open_retry>0:
            try:
                print open_retry
                print self.buildinfo_url
                response = urllib2.urlopen(self.buildinfo_url)
                re_st = True
                break
            except Exception as e:
                print e
                re_st = False
            sleep(1)
            open_retry = open_retry - 1

        if not re_st:
            return False

        info_str = response.read()
        info_list = info_str.split('\n')[1:]

        for key in INFO_ENUM.keys():
            for info in info_list:
                if key in info:
                    #CHANGES:375311:4:kernel/common:sprdlinux4.4,375327:4:kernel/common:sprdlinux4.4,375332:2:device/sprd/sharkl2:sprdroid7.0_trunk,375750:1:device/sprd/sharklj1:sprdroid7.0_trunk,375749:1:device/sprd/isharkl2:sprdroid7.0_trunk
                    if key == "CHANGES":
                        INFO_ENUM[key] = info
                    else:
                        INFO_ENUM[key] = info.split(":")[1:]
        return INFO_ENUM

    def get_changes(self):
        infos = self.load_info()
        changes = infos["CHANGES"]
        changes_l = changes.split(',')
        changes_lr = reduce(lambda x, y : x + y, map(lambda x: re.findall('\d+:\d{1,2}:(.*):(.*)', x), changes_l))
        return changes_lr

    def get_all_infos(self):
        infos = self.load_info()
        changes = self.get_changes()
        infos["CHANGES"] = changes
        return infos

if __name__ == "__main__":

    buildinfo = BuildInfo("http://cmverify.spreadtrum.com:8080/jenkins/job/gerrit_do_verify_sprdroidp/26643")
    print buildinfo.get_all_infos()

