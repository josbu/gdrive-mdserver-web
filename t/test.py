#!/usr/bin/python
# coding: utf-8

# python3 plugins/gdrive/t/test.py
# https://console.cloud.google.com/apis/credentials/consent?project=plated-inn-369901

# https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=226011946234-d3e1vashgag64utjedu1ljt9u39ncrpq.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fdrive.aapanel.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.file&state=I2da4aZUwqgmikrgrqAwwSjyoEHVs1&access_type=offline&prompt=consent&include_granted_scopes=false


# https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Overview/appId/08125e6b-6502-4ac9-9548-ad682f00848d/objectId/62b1d655-9828-47ed-be99-65eb18c3a929/isMSAApp~/false/defaultBlade/Overview/appSignInAudience/AzureADandPersonalMicrosoftAccount/servicePrincipalCreated~/true

# 0WA8Q~sZkZFZKv50ryP4ux~.fpVtbHw7BuTZmbQB
# client_id:d9878fac-8526-4ff6-8036-e1c92dd9dd80

# 08125e6b-6502-4ac9-9548-ad682f00848d


# https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=d9878fac-8526-4ff6-8036-e1c92dd9dd80&redirect_uri=http://localhost&scope=offline_access+Files.ReadWrite.All+User.Read&state=cwopMdHiPIkze4MvgFL6WfSl8LdYAl&prompt=login


# http://localhost/?code=M.C106_BAY.2.3e12c859-6107-0c5b-9ef4-14b3fb8269ba&state=JzHdzHXmA7x6zl7Be6cJ6uOlf9Bg69


# python3 /Users/midoks/Desktop/mwdev/server/mdserver-web/plugins/msonedrive/index.py site t1.cn 3
# python3 /Users/midoks/Desktop/mwdev/server/mdserver-web/plugins/msonedrive/index.py database t1 3
# python3
# /Users/midoks/Desktop/mwdev/server/mdserver-web/plugins/msonedrive/index.py
# path /Users/midoks/Desktop/dev/python 3


import sys
import io
import os
import time
import re
import json


sys.path.append(os.getcwd() + "/class/core")
import mw


def getPluginName():
    return 'gdrive'


def getPluginDir():
    return mw.getPluginDir() + '/' + getPluginName()


def getServerDir():
    return mw.getServerDir() + '/' + getPluginName()


# print(getPluginDir())
sys.path.append(getPluginDir() + "/class")
from gdriveclient import gdriveclient


gd = gdriveclient(getPluginDir(), getServerDir())
gd.setDebug(True)
# sign_in_url, state = gd.get_sign_in_url()
# print(sign_in_url)

# url = 'https://localhost/?state=GH2YZ1VeytzVB1BqJJpQZIBk2GGAub&code=4/0Adeu5BXnD2dQvXx8Sg0WPn1XiMpihcRBNaG1yaFKIo86gUiG7q65KU1MaNCxrj_f2bjkwQ&scope=https://www.googleapis.com/auth/drive.file'
# t = gd.set_auth_url(url)
# print(t)

# def set_auth_url(url):
#     try:
#         if url.startswith("http://"):
#             url = url.replace("http://", "https://")
#         token = msodc.get_token_from_authorized_url(
#             authorized_url=url)
#         msodc.store_token(token)
#         msodc.store_user()
#         return mw.returnJson(True, "授权成功！")
#     except Exception as e:
#         print(e)
#         return mw.returnJson(False, "授权失败2！:" + str(e))
#     return mw.returnJson(False, "授权失败！:" + str(e))

# url = 'http://localhost/?code=M.C106_BAY.2.310112f3-a158-c400-9667-d158cbd1de6c&state=jEJz0ucR9bpZYD9PGxp2GgRDotrzO6'
# token = set_auth_url(url)
# print(token)

# token = msodc.get_token()
# print("token:", token)

t = gd.get_list('')
print(t)

t = gd.get_id_list('1u7LjXGj1KoN-ltAdTRaib7IZJpsEnPdz')
print(t)

# t = gd.create_folder('backup_demo')
# print(t)

# t = msodc.delete_object('backup')
# print(t)


# t = gd.upload_file('web_t1.cn_20230830_134549.tar.gz', 'site')
# print(t)
# print(gd.error_msg)

# /Users/midoks/Desktop/mwdev/server/mdserver-web/paramiko.log
# backup/site/paramiko.log
# |-正在上传到 backup/site/paramiko.log...
# True


# t = msodc.upload_abs_file(
#     'web_t1.cn_20230830_134549.tar.gz', 'site')
# print(t)
# print(msodc.error_msg)
