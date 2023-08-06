#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import six
from io import open
import os
import time
import signal
from multiprocessing import Process
import unittest
from .base import load_pid
from .base import daemon_start
from .base import daemon_stop
from .base import get_process
from .base import is_running
from .base import write_pidfile
from .base import process_kill
from .base import clean_pid_file

def example_process():
    global stopflag
    stopflag = False

    def log(msg):
        with open("daemon-application.log", "a", encoding="utf-8") as fobj:
            six.print_(six.u(str(msg)), file=fobj)

    def on_exit(sig, frame):
        log(time.time())
        log("got term signal...")
        log(sig)
        log(frame)
        global stopflag
        stopflag = True
    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)

    log("example_process start pid={pid}.".format(pid=os.getpid()))
    while not stopflag:
        log(time.time())
        time.sleep(1)
    log("example_process end.")

def main03():
    daemon_start(example_process, "test03.pid", False)

def main04():
    daemon_start(example_process, "test04.pid", True)

class TestDaemonApplication(unittest.TestCase):

    def test01(self):
        p = Process(target=example_process)
        p.start()

        assert is_running(p.pid)

        p2 = get_process(p.pid)
        assert p2.pid == p.pid

        process_kill(p.pid)
        time.sleep(2)
        assert not p.is_alive()
        assert not is_running(p.pid)

    def test02(self):
        pidfile = "test02.pid"

        write_pidfile(pidfile)
        assert load_pid(pidfile) == os.getpid()

        clean_pid_file(pidfile)
        assert load_pid(pidfile) == 0

    def test03(self):
        pidfile = "test03.pid"

        p = Process(target=main03)
        p.start()

        time.sleep(1) # child process may not start yet
        pid = load_pid(pidfile)
        assert pid == p.pid
        assert is_running(pid)
        assert pid != os.getpid()

        six.print_("killing pid={pid}".format(pid=pid))
        daemon_stop(pidfile)
        time.sleep(2)
        p = get_process(pid)
        if p:
            six.print_(p)
            six.print_(p.status())
        assert not is_running(pid)

    def test04(self):
        pidfile = "test04.pid"

        p = Process(target=main04)
        p.start()

        time.sleep(5) # child process may not start yet
        pid = load_pid(pidfile)

        if os.name == "nt":
            assert pid == p.pid # in os nt, daemon flag not working, so the process is not forked, so the the pids are the same.
        else:
            assert pid != p.pid # in other os, daemon flag is working, so the process is forked, so the pids are different.
        assert pid != os.getpid()
        assert is_running(pid)

        print("killing pid={pid}".format(pid=pid))
        daemon_stop(pidfile)
        time.sleep(2)
        p = get_process(pid)
        if p:
            print(p)
            print(p.status())
        assert not is_running(pid)
