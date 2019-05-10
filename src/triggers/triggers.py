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
# import subprocess
from subprocess import Popen, PIPE
from vendor.mucca_logging.mucca_logging import logging
# from src.response.response import response


class triggers():
    """Triggers class."""

    def __init__(self, request):
        """Init."""
        self.env = request.getEnv()
        self.command = request.getUri()
        self.triggers_path = os.getenv('TRIGGERS_PATH')
        # self.path = r'./'
        self.path = r'../muccapp/mucca_install'
        self.wrlogs_path = os.getenv('WRLOGS_PATH')
        pass

    # def firstRes(self, queue):
    #     """Start response."""
    #     logging.log_info(
    #         '[Start] command',
    #         os.path.abspath(__file__),
    #         sys._getframe().f_lineno
    #         )
    #     # res = {"message": "wait"}
    #     # return res
    #     result = "START"
    #     queue.put(result)
    #
    # def lastRes(self, queue):
    #     """End response."""
    #     logging.log_info(
    #         '[End] command',
    #         os.path.abspath(__file__),
    #         sys._getframe().f_lineno
    #         )
    #     # res = {"message": "done"}
    #     # return res
    #     result = "END"
    #     queue.put(result)

    def trigger(self):
        """Trigger method."""
        print("****{}".format(self.command))
        que = queue.Queue()
        id = os.getppid()
        pid = str(object=id)
        day = datetime.datetime.today()
        func = getattr(self, self.command)
        t1 = threading.Thread(
            name='log writer',
            target=self.wrLogs(day, pid, que))
        t2 = threading.Thread(name='daemon', target=func(que, pid))
        print("parent id")
        print(id)
        t2.setDaemon(True)
        # t3 = threading.Thread(name='start server', target=self.lastRes(que))
        t2.start()
        t1.start()
        # t3.start()
        # t3.join()
        # while not que.empty():
        #     result = que.get()
        #     print("****** {} ****".format(result))
        return None

    def start(self):
        pass

    def stop(self):
        pass

    def run(self, queue, id):
        logging.log_info(
            'Run command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        try:
            pop = Popen(
                ['./mucca', '--run', self.env],
                cwd=self.path,
                stdin=PIPE)
            outs, errs = pop.communicate(input=b'\n')
            queue.put(outs)
            date = datetime.datetime.today()
            y = date.year
            m = date.month
            d = date.day
            fname = "/" + str(y) + str(m) + str(d) + "_" + id + ".log"
            while not queue.empty():
                result = queue.get()
                with open(self.wrlogs_path + fname, "w") as log:
                    log.write(result)
            print("Qui avvio il ws server mandandogli")
        except Exception as e:
            logging.log_error(
                "Error in run:{}".format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def wrLogs(self, date, pid, queue):
        y = date.year
        m = date.month
        d = date.day
        print(type(pid))
        fname = "/" + str(y) + str(m) + str(d) + "_" + pid + ".log"
        with open(self.wrlogs_path + fname, "w") as log:
            while not queue.empty():
                result = queue.get()
                log.write(result)
        # if queue.empty():
        #     with open(self.wrlogs_path + fname, "a") as log:
        #         log.write("DONE.")
        #         log.close()

    def build(self):
        pass

    def logs(self):
        pass
