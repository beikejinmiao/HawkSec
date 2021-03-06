#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
import socket
import os
import json
import traceback
from stat import S_ISDIR
from collections import Counter
from conf.paths import DUMP_HOME, DOWNLOADS
from libs.regex import img, video, executable
from libs.client.downloader import Downloader
from libs.pyaml import configure
from libs.enums import TABLES
from libs.logger import logger


"""
https://gist.github.com/johnfink8/2190472
"""


class SSHSession(Downloader):
    def __init__(self, hostname, username='root', password=None, port=22, timeout=5,
                 remote_root=None, out_dir=DOWNLOADS, path_queue=None, db_queue=None):
        super().__init__(out_dir=out_dir, path_queue=path_queue, db_queue=db_queue)
        #
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))
        self.t = paramiko.Transport(self.sock)
        _timeout = configure.get('timeout')
        self.timeout = _timeout if _timeout else timeout
        self.t.banner_timeout = self.timeout
        self.t.start_client()
        if password is not None:
            self.t.auth_password(username, password, fallback=False)
        else:
            raise Exception('Must supply either key_file or password')
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

        # Create object of SSHClient and connecting to SSH
        self.ssh = paramiko.SSHClient()
        # Adding new host key to the local
        # HostKeys object(in case of missing)
        # AutoAddPolicy for missing host key to be set before connection setup.
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, port=port, username=username, password=password, timeout=self.timeout)
        #
        self.files = []
        self._filepath_archive = open(os.path.join(DUMP_HOME, 'filepath.txt'), 'w')
        self.remote_root = remote_root

    @staticmethod
    def _path_join(*args):
        #  Bug fix for Windows clients, we always use / for remote paths
        return '/'.join(args)

    def _sftp_walk(self, remotepath):
        # Kindof a stripped down  version of os.walk, implemented for
        # sftp.  Tried running it flat without the yields, but it really
        # chokes on big directories.
        path = remotepath
        files = []
        folders = []
        try:
            # UnicodeDecodeError
            for f in self.sftp.listdir_attr(remotepath):
                if S_ISDIR(f.st_mode):
                    folders.append(f.filename)
                else:
                    files.append(f.filename)
        except:
            logger.error('sftp walk error: %s' % remotepath)
            logger.error(traceback.format_exc())

        yield path, folders, files

        for folder in folders:
            new_path = self._path_join(remotepath, folder)
            for x in self._sftp_walk(new_path):
                yield x

    def crawling(self):
        home = os.path.split(self.remote_root)[0]
        self.sftp.chdir(home)
        parent = os.path.split(self.remote_root)[1]
        try:
            for path, _, files in self._sftp_walk(parent):
                for filename in files:
                    self.metric.crawl_total += 1
                    self.metric.crawl_success += 1
                    if self.metric.crawl_success % 100 == 0:
                        self._filepath_archive.flush()
                    remote_filepath = self._path_join(home, path, filename)
                    self._filepath_archive.write(remote_filepath + '\n')
                    # ??????????????????????????????????????????
                    if img.match(remote_filepath) or video.match(remote_filepath) or executable.match(remote_filepath):
                        self.metric.crawl_ignored += 1
                        logger.debug('Ignore: %s' % remote_filepath)
                        continue
                    self.files.append(remote_filepath)
        except:
            self.metric.crawl_total += 1
            self.metric.crawl_failed += 1
            logger.error('sftp traverse error: %s' % self.remote_root)
            logger.info(traceback.format_exc())
        logger.info('SFTP??????????????????')
        logger.info('SFTP Metric??????: %s' % self.metric)
        self._filepath_archive.close()

    def downloads(self):
        suffix = list()
        self.metric.file_ignored = self.metric.crawl_ignored
        #
        for remote_filepath in self.files:
            # ???????????????
            if remote_filepath in self._white_url_file:
                continue
            # ??????????????????
            local_filepath = os.path.join(self.out_dir, remote_filepath[1:])   # ??????: ??????????????????join?????????????????????????????????
            local_dir = os.path.dirname(local_filepath)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            # ??????
            self.metric.file_total += 1
            logger.info('Download: %s' % remote_filepath)
            try:
                self.sftp.get(remote_filepath, local_filepath)
                suffix.append(local_filepath.split('.')[-1].lower())
                self.metric.file_success += 1
                # ????????????????????????????????????????????????????????????
                self._put_path_queue((local_filepath, remote_filepath))
                record = {'origin': remote_filepath, 'resp_code': 0, 'desc': 'Success'}
                self._put_db_queue(TABLES.CrawlStat.value, record)
                # self.db_rows.append(record)
            except Exception as e:
                self.metric.file_failed += 1
                logger.error(traceback)
                logger.error('Download Error: %s' % remote_filepath)
                record = {'origin': remote_filepath, 'resp_code': -1, 'desc': str(e)}
                self._put_db_queue(TABLES.CrawlStat.value, record)
                # self.db_rows.append(record)
        # ????????????????????????
        self._put_path_queue(('END', None))
        file_types = dict(Counter(suffix).most_common())
        logger.info('??????????????????: %s' % json.dumps(file_types))

    def cleanup(self):
        self.t.close()
        self.ssh.close()
        if not self._filepath_archive.closed:
            self._filepath_archive.close()
        logger.info('SFTP????????????SSH Session???????????????')


if __name__ == '__main__':
    s = SSHSession(hostname='106.13.202.41', port=61001, password='', remote_root='/root/xdocker')
    s.run()
    print(s.metric)
    s.cleanup()
