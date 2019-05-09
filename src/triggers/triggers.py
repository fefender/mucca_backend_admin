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
import queue
# import subprocess
from subprocess import Popen, PIPE
from vendor.mucca_logging.mucca_logging import logging
from src.response.response import response


class triggers():
    """Triggers class."""

    def __init__(self, command):
        self.triggers_path = os.getenv('TRIGGERS_PATH')
        self.path = r'../muccapp/mucca_install'
        self.command = command
        # self.env = env
        pass

    def firstRes(self, queue):
        """Start response."""
        logging.log_info(
            '[Start] command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        # res = {"message": "wait"}
        # return res
        result = "START"
        queue.put(result)

    def lastRes(self, queue):
        """End response."""
        logging.log_info(
            '[End] command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        # res = {"message": "done"}
        # return res
        result = "END"
        queue.put(result)

    def trigger(self):
        """Trigger method."""
        print("****{}".format(self.command))
        que = queue.Queue()
        func = getattr(self, self.command)
        t1 = threading.Thread(name='first response', target=self.firstRes(que))
        t2 = threading.Thread(name='daemon', target=func(que))
        t2.setDaemon(True)
        t3 = threading.Thread(name='last response', target=self.lastRes(que))
        t1.start()
        t2.start()
        t3.start()
        t3.join()
        while not que.empty():
            result = que.get()
            print("****** {} ****".format(result))
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def run(self, queue):
        logging.log_info(
            'Run command',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        # pop = Popen(
        #     ['./mucca', '--run'],
        #     cwd=self.path,
        #     stdin=PIPE)
        # print(pop)
        # outs, errs = pop.communicate(input=b'\n')
        # return outs
        result = "OUTPUT"
        queue.put(result)

    def build(self):
        pass

    def logs(self):
        pass
