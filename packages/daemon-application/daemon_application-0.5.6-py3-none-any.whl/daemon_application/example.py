#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

import time
import click
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):

    def get_main_options(self):
        options = [
            click.option("-m", "--message", default="hello")
        ]
        return options + DaemonApplication.get_main_options(self)

    def main(self):
        while True:
            print(self.config["message"])
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()
