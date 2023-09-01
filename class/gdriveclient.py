# coding:utf-8

import sys
import io
import os
import time
import re
import json
import io


sys.path.append(os.getcwd() + "/class/core")
import mw

# -----------------------------
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


class gdriveclient():
    __plugin_dir = ''
    __server_dir = ''

    __credentials = "/root/credentials.json"
    __backup_dir_name = "backup"
    __creds = None
    __exclude = ""
    __scpos = ['https://www.googleapis.com/auth/drive.file']
    _title = 'Google Drive'
    _name = 'Google Drive'
    __debug = False

    _DEFAULT_AUTH_PROMPT_MESSAGE = (
        'Please visit this URL to authorize this application: {url}')
    """str: The message to display when prompting the user for
    authorization."""
    _DEFAULT_AUTH_CODE_MESSAGE = (
        'Enter the authorization code: ')
    """str: The message to display when prompting the user for the
    authorization code. Used only by the console strategy."""

    _DEFAULT_WEB_SUCCESS_MESSAGE = (
        'The authentication flow has completed, you may close this window.')

    def __init__(self, plugin_dir, server_dir):
        self.__plugin_dir = plugin_dir
        self.__server_dir = server_dir
        self.set_creds()
        # self.set_libList()

        # self.get_exclode()

    def setDebug(self, d=False):
        self.__debug = d

    def D(self, msg=''):
        if self.__debug:
            print(msg)

    # 检查gdrive连接
    def _check_connect(self):
        try:
            service = build('drive', 'v3', credentials=self.__creds)
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            results.get('files', [])
        except:
            return False
        return True

    # 设置creds
    def set_creds(self):
        token_file = self.__server_dir + '/token.json'
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                tmp_data = json.load(token)['credentials']
                self.__creds = google.oauth2.credentials.Credentials(
                    tmp_data['token'],
                    tmp_data['refresh_token'],
                    tmp_data['id_token'],
                    tmp_data['token_uri'],
                    tmp_data['client_id'],
                    tmp_data['client_secret'],
                    tmp_data['scopes'])
            # if not self._check_connect():
            #     return False
            # else:
            #     return True

    def get_sign_in_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.__plugin_dir + '/credentials.json',
            scopes=self.__scpos)
        flow.redirect_uri = 'https://localhost'
        auth_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='false')
        return auth_url, state

    def set_auth_url(self, url):
        token_file = self.__server_dir + '/token.json'
        if os.path.exists(token_file):
            return mw.returnJson(True, "验证成功")

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.__plugin_dir + '/credentials.json',
            scopes=self.__scpos,
            state=url.split('state=')[1].split('&code=')[0])
        flow.redirect_uri = 'https://localhost'
        flow.fetch_token(authorization_response=url)
        credentials = flow.credentials

        credentials_data = {}
        credentials_data['credentials'] = {
            'token': credentials.token,
            'id_token': credentials.id_token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
        with open(token_file, 'w') as token:
            json.dump(credentials_data, token)
        if not self.set_creds():
            return mw.returnJson(False, "验证失败，请根据页面1 2 3 步骤完成验证")
        return mw.returnJson(True, "验证成功")

    def set_libList(self):
        libList = public.readFile("/www/server/panel/data/libList.conf")
        if libList:
            libList = json.loads(libList)
        for i in libList:
            if "gdrive" in i.values():
                return
        d = {
            "name": "Google Drive",
            "type": "Cron job",
            "ps": "Back up your website or database to Google Cloud Storage.",
            "status": False,
            "opt": "gdrive",
            "module": "os",
            "script": "gdrive",
            "help": "http://forum.aapanel.com",
            "key": "",
            "secret": "",
            "bucket": "",
            "domain": "",
            "check": ["/www/server/panel/plugin/gdrive/gdrive_main.py",
                      "/www/server/panel/script/backup_gdrive.py"]
        }
        d1 = {
            "name": "谷歌硬盘",
            "type": "计划任务",
            "ps": "将网站或数据库打包备份到谷歌硬盘.",
            "status": False,
            "opt": "gdrive",
            "module": "os",
            "script": "gdrive",
            "help": "http://www.bt.cn/bbs",
            "key": "",
            "secret": "",
            "bucket": "",
            "domain": "",
            "check": ["/www/server/panel/plugin/gdrive/gdrive_main.py",
                      "/www/server/panel/script/backup_gdrive.py"]
        }
        language = public.readFile("/www/server/panel/config/config.json")
        if "English" in language:
            data = d
        else:
            data = d1
        libList.append(data)
        public.writeFile("/www/server/panel/data/libList.conf",
                         json.dumps(libList))
        return libList

    # 获取token
    def get_token(self, get):
        token_file = self.__server_dir + '/token.json'
        import requests
        try:
            respone = requests.get("https://www.google.com", timeout=2)
        except:
            return mw.returnJson(False, "连接谷歌失败")
        if respone.status_code != 200:
            return mw.returnJson(False, "连接谷歌失败")
        if not self.set_creds():
            return mw.returnJson(False, "验证失败，请根据页面1 2 3 步骤完成验证")
        if not os.path.exists(token_file):
            return mw.returnJson(False, "验证失败，请根据页面1 2 3 步骤完成验证")
        return mw.returnJson(True, "验证成功")

    # 获取auth_url
    def get_auth_url(self, get):
        self.get_sign_in_url()
        if os.path.exists("/tmp/auth_url"):
            return mw.readFile("/tmp/auth_url")

    # 检查连接
    def check_connect(self, get):
        token_file = self.__server_dir + '/token.json'
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.set_creds()
        else:
            self.D("Failed to get Google token, please verify before use")
            return mw.returnJson(True, "Failed to get Google token, please verify before use")
        service = build('drive', 'v3', credentials=self.__creds)
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        try:
            results.get('files', [])
            return mw.returnJson(False, "验证失败，请根据页面1 2 3 步骤完成验证")
            return mw.returnJson(True, "验证成功")
        except:
            return mw.returnJson(False, "验证失败，请根据页面1 2 3 步骤完成验证")

    def _get_filename(self, filename):
        l = filename.split("/")
        return l[-1]

    def _create_folder_cycle(self, filepath):
        l = filepath.split("/")
        fid_list = []
        for i in l:
            if not i:
                continue
            fid = self.__get_folder_id(i)
            if fid:
                fid_list.append(fid)
                continue
            if not fid_list:
                fid_list.append("")
            fid_list.append(self.create_folder(i, fid_list[-1]))
        return fid_list[-1]

    def build_object_name(self, data_type, file_name):
        """根据数据类型构建对象存储名称

        :param data_type:
        :param file_name:
        :return:
        """

        import re
        prefix_dict = {
            "site": "web",
            "database": "db",
            "path": "path",
        }
        file_regx = prefix_dict.get(data_type) + "_(.+)_20\d+_\d+\."
        sub_search = re.search(file_regx.lower(), file_name)
        sub_path_name = ""
        if sub_search:
            sub_path_name = sub_search.groups()[0]
            sub_path_name += '/'
        # 构建OS存储路径
        object_name = self.__backup_dir_name + \
            '/{}/{}'.format(data_type, sub_path_name)

        if object_name[:1] == "/":
            object_name = object_name[1:]
        return object_name

    # 上传文件
    def upload_file(self, filename, data_type=None):
        """
        get.filename 上传后的文件名
        get.filepath 上传文件路径
        被面板新版计划任务调用时
        get表示file_name
        :param get:
        :return:
        """
        # filename = filename
        filepath = self.build_object_name(data_type, filename)
        filename = self._get_filename(filename)
        print(filepath)
        print(filename)

        parents = self._create_folder_cycle(filepath)
        print(parents)
        # drive_service = build('drive', 'v3', credentials=self.__creds)
        # file_metadata = {'name': filename, 'parents': [parents]}
        # media = MediaFileUpload(filename, resumable=True)
        # file = drive_service.files().create(
        #     body=file_metadata, media_body=media, fields='id').execute()
        # print('Upload Success ,File ID: %s' % file.get('id'))
        return True

    def _get_file_id(self, filename):
        service = build('drive', 'v3', credentials=self.__creds)
        results = service.files().list(pageSize=10, q="name='{}'".format(
            filename), fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            return []
        else:
            for item in items:
                return item["id"]

    def delete_file(self, filename=None, data_type=None):
        file_id = self._get_file_id(filename)
        self._delete_file(file_id)

    def _delete_file(self, file_id):
        try:
            drive_service = build('drive', 'v3', credentials=self.__creds)
            drive_service.files().delete(fileId=file_id).execute()
        except:
            pass
        print("delete ok")

    # 获取目录id
    def __get_folder_id(self, floder_name):
        service = build('drive', 'v3', credentials=self.__creds)
        results = service.files().list(pageSize=10, q="name='{}' and mimeType='application/vnd.google-apps.folder'".format(floder_name),
                                       fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            return []
        else:
            for item in items:
                return item["id"]

    def get_list(self, path=''):
        service = build('drive', 'v3', credentials=self.__creds)
        results = service.files().list(pageSize=10, q="name='{}' and mimeType='application/vnd.google-apps.folder'".format(floder_name),
                                       fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        print(items)

    # 创建目录
    def create_folder(self, folder_name, parents=""):
        self.D(self.__creds)
        self.D("folder_name: {}\nparents: {}".format(folder_name, parents))
        service = build('drive', 'v3', credentials=self.__creds)
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parents:
            file_metadata['parents'] = [parents]
        folder = service.files().create(body=file_metadata, fields='id').execute()
        self.D('Create Folder ID: %s' % folder.get('id'))
        return folder.get('id')

    # 获取数据库编码
    def get_database_character(self, db_name):
        try:
            import panelMysql
            tmp = panelMysql.panelMysql().query("show create database `%s`" % db_name.strip())
            c_type = str(re.findall("SET\s+([\w\d-]+)\s", tmp[0][1])[0])
            c_types = ['utf8', 'utf-8', 'gbk', 'big5', 'utf8mb4']
            if not c_type.lower() in c_types:
                return 'utf8'
            return c_type
        except:
            return 'utf8'

    def get_exclode(self, exclude=[]):
        if not exclude:
            tmp_exclude = os.getenv('BT_EXCLUDE')
            if tmp_exclude:
                exclude = tmp_exclude.split(',')
        if not exclude:
            return ""
        for ex in exclude:
            self.__exclude += " --exclude=\"" + ex + "\""
        self.__exclude += " "
        return self.__exclude

    def download_file(self, filename):
        file_id = self._get_file_id(filename)
        service = build('drive', 'v3', credentials=self.__creds)
        request = service.files().get_media(fileId=file_id)
        with open('/tmp/{}'.format(filename), 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

        # 备份网站
    def backup_site(self, name, count, exclude=[]):
        print(count)
        sql = db.Sql()
        path = sql.table('sites').where('name=?', (name,)).getField('path')
        startTime = time.time()
        if not path:
            endDate = time.strftime('%Y/%m/%d %X', time.localtime())
            log = "The site [" + name + "] does not exist!"
            print("★[" + endDate + "] " + log)
            print(
                "----------------------------------------------------------------------------")
            return

        backup_path = sql.table('config').where(
            "id=?", (1,)).getField('backup_path') + '/site'
        if not os.path.exists(backup_path):
            public.ExecShell("mkdir -p " + backup_path)

        filename = backup_path + "/Web_" + name + "_" + time.strftime('%Y%m%d_%H%M%S',
                                                                      time.localtime()) + '_' + public.GetRandomString(
            8) + '.tar.gz'
        public.ExecShell("cd " + os.path.dirname(path) + " && tar zcvf '" + filename +
                         "' '" + os.path.basename(path) + "'" + self.__exclude + " > /dev/null")
        endDate = time.strftime('%Y/%m/%d %X', time.localtime())

        if not os.path.exists(filename):
            log = "Website [" + name + "] backup failed!"
            print("★[" + endDate + "] " + log)
            print(
                "----------------------------------------------------------------------------")
            return

        # 上传文件
        get = getObject()
        get.filename = filename
        get.filepath = 'bt_backup/sites/' + name
        print("Start upload")
        self.upload_file(get)
        outTime = time.time() - startTime
        pid = sql.table('sites').where('name=?', (name,)).getField('id')
        download = get.filepath + '/' + os.path.basename(filename)
        sql.table('backup').add('type,name,pid,filename,addtime,size',
                                ('0', download, pid, 'gdrive', endDate, os.path.getsize(filename)))
        log = "The website [" + name + "] has been successfully backed up to Google Drive, using [" + \
            str(round(outTime, 2)) + "] seconds"
        public.WriteLog('TYPE_CRON', log)
        print("★[" + endDate + "] " + log)
        print("|---Keep the latest [" + count + "] backups")
        print("|---File name:" + os.path.basename(filename))

        # 清理本地文件
        # public.ExecShell("rm -f " + filename)

        # # 清理多余备份
        # backups = sql.table('backup').where('type=? and pid=? and filename=?', ('0', pid, 'gdrive')).field(
        #     'id,name,filename').select()
        # num = len(backups) - int(count)
        # if num > 0:
        #     for backup in backups:
        #         print(backup['filename'])
        #         if os.path.exists(backup['filename']):
        #             public.ExecShell("rm -f " + backup['filename'])
        #         # get.filename = 'bt_backup/sites/' + name + '/' + backup['name'].split("/")[-1]
        #         name = self._get_filename(backup['name'].split("/")[-1])
        #         file_id = self._get_file_id(name)
        #         try:
        #             self._delete_file(file_id)
        #         except Exception as e:
        #             print(e)
        #         sql.table('backup').where('id=?', (backup['id'],)).delete()
        #         num -= 1
        #         print("|---The expired backup file has been cleaned up：" + backup['name'])
        #         if num < 1: break
        backups = sql.table('backup').where(
            'type=? and pid=? and '
            'filename LIKE \'%{}%\''.format(self._name),
            ('0', pid)).field('id,name,filename').select()

        num = len(backups) - int(count)
        if num > 0:
            for backup in backups:
                _base_file_name = backup["name"]
                _local_file_name = os.path.join(backup_path,
                                                _base_file_name)

                if os.path.isfile(_local_file_name):
                    public.ExecShell("rm -f " + _local_file_name)
                    self.echo_info("已清理本地备份文件:" + _local_file_name)

                _file_name = backup["filename"]
                if _file_name.find(self.CONFIG_SEPARATOR) != -1:
                    os_file_name = _file_name.split(self.CONFIG_SEPARATOR)[0]
                else:
                    os_file_name = _file_name
                self.delete_object(os_file_name)
                sql.table('backup').where('id=?', (backup['id'],)).delete()
                num -= 1
                self.echo_info("已清理{}过期备份文件：".format(self._title) +
                               os_file_name)
                if num < 1:
                    break

        return None

    # 备份数据库
    def backup_database(self, name, count):
        sql = db.Sql()
        path = sql.table('databases').where('name=?', (name,)).getField('id')
        startTime = time.time()
        if not path:
            endDate = time.strftime('%Y/%m/%d %X', time.localtime())
            log = "The database [" + name + "] does not exist!"
            print("★[" + endDate + "] " + log)
            print(
                "----------------------------------------------------------------------------")
            return

        backup_path = sql.table('config').where(
            "id=?", (1,)).getField('backup_path') + '/database'
        if not os.path.exists(backup_path):
            public.ExecShell("mkdir -p " + backup_path)

        filename = backup_path + "/Db_" + name + "_" + time.strftime('%Y%m%d_%H%M%S',
                                                                     time.localtime()) + '_' + public.GetRandomString(
            8) + ".sql.gz"

        import re
        mysql_root = '"' + \
            sql.table('config').where(
                "id=?", (1,)).getField('mysql_root') + '"'
        mycnf = public.readFile('/etc/my.cnf')
        rep = "\[mysqldump\]\nuser=root"
        sea = "[mysqldump]\n"
        subStr = sea + "user=root\npassword=" + mysql_root + "\n"
        mycnf = mycnf.replace(sea, subStr)
        if len(mycnf) > 100:
            public.writeFile('/etc/my.cnf', mycnf)
        sh = "/www/server/mysql/bin/mysqldump --default-character-set=" + \
            self.get_database_character(
                name) + " --force --opt " + name + " | gzip > " + filename
        public.ExecShell(sh)
        if not os.path.exists(filename):
            endDate = time.strftime('%Y/%m/%d %X', time.localtime())
            log = "Database [" + name + "] backup failed!"
            print("★[" + endDate + "] " + log)
            print(
                "---------------------------------------------------------------------------")
            return
        mycnf = public.readFile('/etc/my.cnf')
        mycnf = mycnf.replace(subStr, sea)
        if len(mycnf) > 100:
            public.writeFile('/etc/my.cnf', mycnf)
        # 上传
        get = getObject()
        get.filename = filename
        get.filepath = 'bt_backup/database/' + name
        print("开始上传文件：", get.filename, get.filepath)
        self.upload_file(get)
        endDate = time.strftime('%Y/%m/%d %X', time.localtime())
        outTime = time.time() - startTime
        pid = sql.table('databases').where('name=?', (name,)).getField('id')
        download = get.filepath + '/' + os.path.basename(filename)
        sql.table('backup').add('type,name,pid,filename,addtime,size',
                                (1, download, pid, 'gdrive', endDate, os.path.getsize(filename)))
        log = "The database [" + name + "] has been successfully backed up to Google Drive, using [" + \
            str(round(outTime, 2)) + "] seconds"
        public.WriteLog('TYPE_CRON', log)
        print("★[" + endDate + "] " + log)
        print("|---Keep the latest [" + count + "] backups")
        print("|---File name:" + os.path.basename(filename))
        # 清理本地文件
        public.ExecShell("rm -f " + filename)
        # 清理多余备份
        backups = sql.table('backup').where('type=? and pid=? and filename=?', ('1', pid, 'gdrive')).field(
            'id,name,filename').select()
        num = len(backups) - int(count)
        if num > 0:
            for backup in backups:
                if os.path.exists(backup['filename']):
                    public.ExecShell("rm -f " + backup['filename'])
                # get.filename = 'bt_backup/database/' + name + '/' + backup['name'].split("/")[-1]
                name = self._get_filename(backup['name'].split("/")[-1])
                file_id = self._get_file_id(name)
                try:
                    self._delete_file(file_id)
                except Exception as e:
                    print(e)
                sql.table('backup').where('id=?', (backup['id'],)).delete()
                num -= 1
                print(
                    "|---The expired backup file has been cleaned up：" + backup['name'])
                if num < 1:
                    break
        return None

    # 备份指定目录
    def backup_path(self, path, count, exclude=[]):
        print(count)
        sql = db.Sql()
        startTime = time.time()
        if path[-1:] == '/':
            path = path[:-1]
        name = os.path.basename(path)
        backup_path = sql.table('config').where(
            "id=?", (1,)).getField('backup_path') + '/path'
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        filename = backup_path + "/Path_" + name + "_" + time.strftime('%Y%m%d_%H%M%S',
                                                                       time.localtime()) + '.tar.gz'
        os.system("cd " + os.path.dirname(path) + " && tar zcvf '" + filename +
                  "' '" + os.path.basename(path) + "'" + self.__exclude + " > /dev/null")

        get = getObject()
        get.filename = filename
        get.filepath = 'bt_backup/path/' + name
        self.upload_file(get)

        endDate = time.strftime('%Y/%m/%d %X', time.localtime())
        if not os.path.exists(filename):
            log = "Directory [" + path + "] backup failed"
            print("★[" + endDate + "] " + log)
            print(
                "----------------------------------------------------------------------------")
            return
        outTime = time.time() - startTime
        download = get.filepath + '/' + os.path.basename(filename)
        sql.table('backup').add('type,name,filename,addtime,size',
                                ('2', download, 'gdrive', endDate, os.path.getsize(filename)))

        log = "The directory [" + path + "] is successfully backed up, using [" + \
            str(round(outTime, 2)) + "] seconds"
        public.WriteLog('TYPE_CRON', log)
        print("★[" + endDate + "] " + log)
        print("|---Keep the latest [" + count + "] backups")
        print("|---File name:" + filename)

        # 清理多余备份
        backups = sql.table('backup').where(
            'type=? and filename=?', ('2', "gdrive")).field('id,name,filename').select()
        # 清理本地备份
        if os.path.exists(filename):
            os.remove(filename)

        num = len(backups) - int(count)
        if num > 0:
            for backup in backups:
                if os.path.exists(backup['filename']):
                    public.ExecShell("rm -f " + backup['filename'])
                name = self._get_filename(backup['name'].split("/")[-1])
                file_id = self._get_file_id(name)
                try:
                    self._delete_file(file_id)
                except Exception as e:
                    print(e)
                sql.table('backup').where('id=?', (backup['id'],)).delete()
                num -= 1
                print("|---The expired backup file has been cleaned up：" +
                      backup['filename'])
                if num < 1:
                    break
        return None

    def backup_all_site(self, save):
        sites = public.M('sites').field('name').select()
        for site in sites:
            self.backup_site(site['name'], save)

    def backup_all_databases(self, save):
        databases = public.M('databases').field('name').select()
        for database in databases:
            self.backup_database(database['name'], save)

    def get_function_args(self, func):
        import sys
        if sys.version_info[0] == 3:
            import inspect
            return inspect.getfullargspec(func).args
        else:
            return func.__code__.co_varnames

    def execute_command(self, args):
        client = self
        cls_args = self.get_function_args(panelBackup.backup.__init__)
        if "cron_info" in cls_args and len(args) == 5:
            cron_name = args[4]
            cron_info = {
                "echo": cron_name
            }
            backup_tool = panelBackup.backup(cloud_object=client,
                                             cron_info=cron_info)
        else:
            backup_tool = panelBackup.backup(cloud_object=client)
        _type = args[1]
        data = None
        if _type == 'site':
            if args[2] == 'ALL':
                backup_tool.backup_site_all(save=int(args[3]))
            else:
                backup_tool.backup_site(args[2], save=int(args[3]))
            exit()
        elif _type == 'database':
            if args[2] == 'ALL':
                backup_tool.backup_database_all(int(args[3]))
            else:
                backup_tool.backup_database(args[2],
                                            save=int(args[3]))
            exit()
        elif _type == 'path':
            backup_tool.backup_path(args[2], save=int(args[3]))
            exit()
        # elif _type == 'upload':
        #     data = client.upload_file(args[2])
        # elif _type == 'download':
        #     data = client.download_blob(args[2])
        # # elif _type == 'get':
        # #     data = client.get_files(args[2]);
        # elif _type == 'list':
        #     path = "/"
        #     if len(args) == 3:
        #         path = args[2]
        #     data = client.list_blobs_with_prefix(path);
        # elif _type == 'lib':
        #     data = client.get_lib()
        # elif _type == 'delete_file':
        #     result = client.delete_file(args[2]);
        #     if result:
        #         print("The file {} was deleted successfully.".format(args[2]))
        #     else:
        #         print("File {} deletion failed!".format(args[2]))
        else:
            data = 'ERROR: The parameter is incorrect!'
        if data:
            print()
            print(json.dumps(data))


class getObject:
    pass

if __name__ == "__main__":
    import json
    import panelBackup

    data = None

    new_version = True if panelBackup._VERSION >= 1.2 else False

    q = gdrive_main()
    # 检查获取验证
    q.set_creds()
    type = sys.argv[1]
    if not new_version:
        if type == 'site':
            if sys.argv[2] == 'ALL':
                q.backup_all_site(sys.argv[3])
            else:
                q.backup_site(sys.argv[2], sys.argv[3])
            exit()
        elif type == 'database':
            if sys.argv[2] == 'ALL':
                data = q.backup_all_databases(sys.argv[3])
            else:
                data = q.backup_database(sys.argv[2], sys.argv[3])
            exit()
        elif type == 'path':
            data = q.backup_path(sys.argv[2], sys.argv[3])
        else:
            data = 'ERROR: The parameter is incorrect!'
    else:
        q.execute_command(sys.argv)
