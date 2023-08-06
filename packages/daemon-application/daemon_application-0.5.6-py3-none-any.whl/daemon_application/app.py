#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

__all__ = [
    "DaemonApplication",
    "SimpleXmlRpcServer",
    "SimpleRpcServer",
    "simple_rpcd_controller",
]

import os
import sys
import time
import signal
import logging
from pprint import pprint
try:
    from socketserver import ThreadingMixIn
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
except ImportError:
    from SocketServer import ThreadingMixIn
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


import click
import yaml
import magic_import
from zenutils import dictutils
from zenutils import logutils
from zenutils import serviceutils

from .base import daemon_start
from .base import daemon_stop

_logger = logging.getLogger(__name__)


class DaemonApplication(object):
    config_name = "config"
    config_suffix = "yml"
    default_appname = None

    # default_config = {}

    def get_default_config_filepaths(self, appname, name=None, suffix=None):
        name = name or self.config_name
        suffix = suffix or self.config_suffix
        filepaths = []
        filenames = (
            "./{0}-{1}.{2}".format(appname, name, suffix),
            "./conf/{0}-{1}.{2}".format(appname, name, suffix),
            "./etc/{0}-{1}.{2}".format(appname, name, suffix),
            "~/.{0}/{1}.{2}".format(appname, name, suffix),
            "~/{0}/{1}.{2}".format(appname, name, suffix),
            "./{0}.{1}".format(name, suffix),
            "./conf/{0}.{1}".format(name, suffix),
            "./etc/{0}.{1}".format(name, suffix),
            "~/{0}.{1}".format(name, suffix),
            "~/.{0}.{1}".format(name, suffix),
            "{0}.{1}".format(name, suffix),
        )
        for filename in filenames:
            filepath = os.path.abspath(os.path.expandvars(os.path.expanduser(filename)))
            if not filepath in filepaths:
                filepaths.append(filepath)
        return filepaths

    def main(self):
        raise NotImplementedError()

    def get_appname(self):
        appname = getattr(self, "default_appname", None)
        if appname is None:
            appname = os.path.splitext(os.path.basename(os.sys.argv[0]))[0]
        return appname
    
    def get_config_file_path(self, config_file_path, appname):
        the_config_file_path = None
        for config_file_path in [config_file_path] + self.get_default_config_filepaths(appname):
            if config_file_path and os.path.exists(config_file_path):
                the_config_file_path = config_file_path
                break
        return the_config_file_path

    def get_default_config(self):
        config = {
            "pidfile": "app.pid",
            "stop-timeout": 30,
            "stop-signal": signal.SIGINT,
            "daemon": True,
            "workspace": os.getcwd(),
            "loglevel": "INFO",
            "logfile": "app.log",
            "logfmt": "default",
        }
        config.update(getattr(self, "default_config", {}))
        return config

    def load_config_from_config_file(self, config_file):
        if not config_file:
            return {}
        if not os.path.exists(config_file):
            return {}
        with open(config_file, "rb") as fobj:
            return yaml.safe_load(fobj)

    def update_config_item(self, config, item_name, item_value):
        if not item_value is None:
            config[item_name] = item_value
        return config

    def fix_config_items(self, config):
        if config.get("pidfile", None) is None:
            config["pidfile"] = self.appname + ".pid"

    def load_config(self, config, **kwargs):
        self.config = dictutils.Object({})
        self.appname = self.get_appname()
        self.config_file_path = self.get_config_file_path(config, self.appname)
        if self.config_file_path:
            print("Start application with config file: {}".format(self.config_file_path), file=sys.stderr)
        else:
            print("Start application without config file.", file=sys.stderr)
        self.config.update(self.get_default_config())
        self.config.update(self.load_config_from_config_file(self.config_file_path))
        for key, value in kwargs.items():
            self.update_config_item(self.config, key.replace("_", "-"), value)
        self.config["config-file-path"] = self.config_file_path
        self.fix_config_items(self.config)

    def get_main_options(self):
        option_pidfile = click.option("--pidfile", help="pidfile file path.")
        option_daemon = click.option("--daemon/--no-daemon", is_flag=True, default=None, help="Run application in background or in foreground.")
        option_workspace = click.option("--workspace", help="Set running folder")
        option_config = click.option("-c", "--config", help="Config file path. Application will search config file if this option is missing. Use sub-command show-config-fileapaths to get the searching tactics.")
        option_loglevel = click.option("--loglevel")
        option_logfile = click.option("--logfile")
        option_logfmt = click.option("--logfmt")
        return [option_config, option_daemon, option_workspace, option_pidfile, option_loglevel, option_logfile, option_logfmt]

    def get_controller(self):
        main_options = self.get_main_options()
        def _main(config, **kwargs):
            self.load_config(config, **kwargs)
        main = _main
        for option in main_options:
            main = option(main)
        main = click.group()(main)
    
        @main.command()
        def start():
            """Start daemon application.
            """
            pidfile = self.config["pidfile"]
            daemon = self.config["daemon"]
            workspace = self.config["workspace"]
            daemon_start(self.main, pidfile=pidfile, daemon=daemon, workspace=workspace)

        @main.command()
        def stop():
            """Stop daemon application.
            """
            pidfile = self.config["pidfile"]
            stop_signal = self.config["stop-signal"]
            stop_timeout = self.config["stop-timeout"]
            daemon_stop(pidfile, sig=stop_signal, stop_timeout=stop_timeout)

        @main.command()
        @click.option("--sleep-seconds", type=int, default=0, help="Wait some seconds after old application stopped and before new application started.")
        def restart(sleep_seconds):
            """Restart Daemon application.
            """
            pidfile = self.config["pidfile"]
            stop_signal = self.config["stop-signal"]
            stop_timeout = self.config["stop-timeout"]
            daemon_stop(pidfile, sig=stop_signal, stop_timeout=stop_timeout)
            if sleep_seconds:
                time.sleep(sleep_seconds)
            daemon = self.config["daemon"]
            workspace = self.config["workspace"]
            daemon_start(self.main, pidfile=pidfile, daemon=daemon, workspace=workspace)

        @main.command(name="show-config-filepaths")
        def show_config_filepaths():
            """Print out the config searching paths.
            """
            config_filepaths = self.get_default_config_filepaths(self.appname)
            print("Application will search config file from following paths. It will load the first exists file as the config file.")
            for filepath in config_filepaths:
                print("    ", filepath)

        @main.command(name="show-configs")
        def show_configs():
            """Print out the final config items.
            """
            pprint(self.config)

        return main


class SimpleXmlRpcServer(ThreadingMixIn, SimpleXMLRPCServer):

    def __init__(self, config):
        self.config = config
        xmlrpc_server_init_args = (
            (self.config.select("server.listen"), self.config.select("server.port")),
        )
        xmlrpc_server_init_kwargs = {
            "requestHandler": SimpleXMLRPCRequestHandler,
            "allow_none": self.config.select("server.allow_none", True),
            "encoding": self.config.select("server.encoding", "utf-8"),
        }
        SimpleXMLRPCServer.__init__(self, *xmlrpc_server_init_args, **xmlrpc_server_init_kwargs)
        self.register_introspection_functions()
        self.register_multicall_functions()


class SimpleRpcServer(DaemonApplication):

    def get_default_server_listen(self):
        return getattr(self, "default_server_listen", "0.0.0.0")

    def get_default_listen_port(self):
        return getattr(self, "default_server_port", 8381)

    def get_default_server_class(self):
        return getattr(self, "default_server_class", "daemon_application.app.SimpleXmlRpcServer")

    def get_default_config(self):
        default_config = {
            "server": {
                "listen": self.get_default_server_listen(),
                "port": self.get_default_listen_port(),
                "class": self.get_default_server_class(),
            }
        }
        more_default_config = DaemonApplication.get_default_config(self)
        dictutils.deep_merge(default_config, more_default_config)
        return default_config

    def main(self):
        logutils.setup(**self.config)
        # make server
        server_class = self.config.get("class", self.get_default_server_class())
        ServerClass = magic_import.import_from_string(server_class)
        if not ServerClass:
            _logger.fatal("SimpleRpcServer.make_server failed: server class {server_class} not found...".format(server_class=server_class))
            sys.exit(1)
        self.server = ServerClass(self.config)
        # load services
        self.services = {}
        # register debug service
        if self.config.select("enable-debug-service", True):
            self.debug_service = serviceutils.DebugService(self.config)
            self.debug_service.register_to(self.server)
        # load more services
        service_configs = self.config.select("services", [])
        for service_config in service_configs:
            service_class_name = service_config.select("class", None)
            if not service_class_name:
                msg = "Service config missing class field, service_config={service_config}...".format(
                    service_config=service_config,
                )
                _logger.warning(msg)
                continue
            Service = magic_import.import_from_string(service_class_name)
            if not Service:
                msg = "Service class {service_class_name} not found...".format(
                    service_class_name=service_class_name,
                )
                _logger.error(msg)
                continue
            msg = "Loading services from {service_class_name}...".format(
                service_class_name=service_class_name,
            )
            _logger.info(msg)
            service_args = service_config.select("args", [])
            service_kwargs = service_config.select("kwargs", {})
            self.services[service_class_name] = Service(self.config, *service_args, **service_kwargs)
            self.services[service_class_name].register_to(self.server)
        # start server
        try:
            _logger.info("Starting server on {listen}:{port}...".format(
                listen=self.config.select("server.listen", self.get_default_server_listen()),
                port=self.config.select("server.port", self.get_default_listen_port()),
                ))
            self.server.serve_forever()
        except KeyboardInterrupt:
            _logger.info("Got KeyboardInterrupt signal, stopping the service...")


simple_rpcd_controller = SimpleRpcServer().get_controller()

if __name__ == "__main__":
    simple_rpcd_controller()
