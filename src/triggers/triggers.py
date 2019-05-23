# Copyright 2019 Federica Cricchio
# fefender@gmail.com
#
# This file is part of mucca_backend_admin.
#
# mucca_backend_admin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mucca_backend_admin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mucca_backend_admin.  If not, see <http://www.gnu.org/licenses/>.
"""Triggers."""
import os
import sys
import threading
import time
import datetime
import queue
import json
import re
from subprocess import Popen, PIPE
from vendor.mucca_logging.mucca_logging import logging
# from src.triggers.wsserver import wsserver
from src.response.response import response


class triggers():
    """Triggers class."""

    def __init__(self, request):
        """Init."""
        self.env = request.getEnv()
        self.query = request.getQuery()
        self.command = request.getUri()
        self.triggers_path = os.getenv('TRIGGERS_PATH')
        # self.path = r'./'
        self.path = r'../muccapp/mucca_install'
        self.wrlogs_path = os.getenv('WRLOGS_PATH')

    def __getWssPort(self):
        if self.env == "develop":
            return os.getenv('WSS_PORT_D')
        if self.env == "production":
            return os.getenv('WSS_PORT_P')
        if self.env == "stage":
            return os.getenv('WSS_PORT_S')

    def startWss(self):
        """Start websocket server."""
        ws_port = self.__getWssPort()
        # path = "src/triggers"
        path = "./"
        try:
            pop = Popen(
                ['python3.7', 'wsserver.py', ws_port],
                cwd=path)
        except Exception as e:
            logging.log_error(
                "Error in list:{}".format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )

    def trigger(self):
        """Trigger method."""
        print("****{}".format(self.command))
        que = queue.Queue()
        id = os.getppid()
        pid = str(object=id)
        day = datetime.datetime.today()
        y = day.year
        m = day.month
        d = day.day
        hh = day.hour
        mm = day.minute
        ss = day.second
        fdate = str(y) + str(m) + str(d) + "_" + str(hh) + str(mm) + str(ss)
        fname = "/" + fdate + "_" + pid + ".log"
        if self.command == "status":
            return self.triggStatus(fname)
        func = getattr(self, self.command)
        ws_port = self.__getWssPort()
        t2 = threading.Thread(
            name='command',
            target=func(fname, que),
            daemon=True)
        t2.start()
        if not que.empty():
            resp = {'port': ws_port,
                    'action': self.command,
                    'fname': fname}
            return response.respond(200, json.dumps(resp))
        return response.respond(400, None)

    def list(self, fname, que):
        """Start."""
        logging.log_info(
            'List command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        t1 = threading.Thread(
            name='websocket server',
            target=self.startWss,
            daemon=True)
        with open(self.wrlogs_path + fname, "w") as log:
            try:
                pop = Popen(
                    ['./mucca', '--list', self.env],
                    cwd=self.path,
                    stdout=log)
            except Exception as e:
                logging.log_error(
                    "Error in list:{}".format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return None
            if pop.poll() is None:
                que.put("polling")
                t1.start()
            log.close()

    def stop(self, fname, que):
        """Stop."""
        logging.log_info(
            'Stop command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        t1 = threading.Thread(
            name='websocket server',
            target=self.startWss,
            daemon=True)
        with open(self.wrlogs_path + fname, "w") as log:
            try:
                command = ['./mucca', '--stop', self.env]
                if self.query is not None:
                    command = ['./mucca', '--stop', self.env,
                               '--only', self.query[1]]
                pop = Popen(
                    command,
                    cwd=self.path,
                    stdout=log)
            except Exception as e:
                logging.log_error(
                    "Error in stop:{}".format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return None
            if pop.poll() is None:
                que.put("polling")
                t1.start()
            log.close()

    def run(self, fname, que):
        """Run."""
        logging.log_info(
            'Run command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        t1 = threading.Thread(
            name='websocket server',
            target=self.startWss,
            daemon=True)
        with open(self.wrlogs_path + fname, "w") as log:
            try:
                command = ['./mucca', '--run', self.env]
                if self.query is not None:
                    command = ['./mucca', '--run', self.env,
                               '--only', self.query[1]]
                pop = Popen(
                    command,
                    cwd=self.path,
                    stdout=log)
            except Exception as e:
                logging.log_error(
                    "Error in run:{}".format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return None
            if pop.poll() is None:
                que.put("polling")
                t1.start()
            log.close()

    def build(self, fname, que):
        """Build."""
        logging.log_info(
            'Build command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        t1 = threading.Thread(
            name='websocket server',
            target=self.startWss,
            daemon=True)
        with open(self.wrlogs_path + fname, "w") as log:
            try:
                command = ['./mucca', '--build', self.env]
                if self.query is not None:
                    command = ['./mucca', '--build', self.env,
                               '--only', self.query[1]]
                pop = Popen(
                    command,
                    cwd=self.path,
                    stdout=log)
            except Exception as e:
                logging.log_error(
                    "Error in build:{}".format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return None
            if pop.poll() is None:
                que.put("polling")
                t1.start()
            log.close()

    def triggStatus(self, fname):
        """Trigg status command."""
        que = queue.Queue()
        t2 = threading.Thread(
            name='status command',
            target=self.status(fname, que),
            daemon=False)
        t2.start()
        t2.join()
        if not que.empty():
            ext = que.get()
            # print(ext)
            print("before open")
            self.getStatusResponse(fname)
            # with open(self.wrlogs_path + fname) as log:
            #     print("after open")
            #     txt = log.readlines()
            #     print(txt)
            # return response.respond(200, None)
        return response.respond(400, None)

    def getStatusResponse(self, fname):
        """Get status response."""
        with open(self.wrlogs_path + fname) as log:
            print("after open")
            txt = log.read()
            print(txt)
            pattern = r'ENV(.*)STATUS'
            repl = "::"
            subb = re.sub(pattern, repl, txt)
            pro = re.findall(r'\n(.*)\n', subb)
            print(pro)
            # sub = re.sub('\n', ' ', subb)
            # print(sub)
            # spl = sub.split("::")
            # print(type(spl))
            # print(" type and len")
            # print(len(spl))
            # print("list is")
            # print(spl)
            # for n in range(len(spl)):
            #     print("!!!")
            #     group = spl[n]
            #     print(group)
            #     line = group.split('   ')
            #     for l in range(len(line)):
            #         print("???")
            #         print(line[l])
                # string = array[n]
                # start = "\x1b" + "[" + "1m"
                # end = "\x1b" + "[" + "0m"
                # find = string.split((start))
                # find = re.search(r'\\x1b\[1m[.*?]\\x1b\[0m', string)
                # print("find")
                # print(find)
                # if find[0] == "- ":
                #     last = find[1].split(end)
                #     print("last")
                #     print(last)
        if self.query is not None:
            regex = "nel caso sia gruppo o ms"
        regex = "nel caso sia status dell'intera app"

    def status(self, fname, que):
        """Status."""
        logging.log_info(
            'Status command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        with open(self.wrlogs_path + fname, "w") as log:
            try:
                command = ['./mucca', '--status', self.env]
                if self.query is not None:
                    command = ['./mucca', '--status', self.env,
                               '--only', self.query[1]]
                pop = Popen(
                    command,
                    cwd=self.path,
                    stdout=PIPE, text=True)
            except Exception as e:
                logging.log_error(
                    "Error in status:{}".format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return None
            while pop.poll() is None:
                out, err = pop.communicate()
                log.write(out)
                # print(out)
                que.put(out)
            log.close()

    def logs(self):
        """Logs."""
        #     pop = subprocess.Popen(
        #         ['tail', '-f', '2019521_5112.log'],
        #         cwd="logs/",
        #         stdout=subprocess.PIPE)
        pass
