# daemon-application

## 介绍

Python开发包，用于创建后台守护进程。

*注意：*

- *只有Linux下可以实现后台运行效果。Windows下降级为前台可执行程序。*


## 安装

```
pip install daemon-application
```

## 使用说明

### 底层函数的使用


```
import time
import threading
import signal
from daemon_application import daemon_start

stopflag = False

def main():
    def on_exit(*args, **kwargs):
        with open("backgroud.log", "a", encoding="utf-8") as fobj:
            print("process got exit signal...", file=fobj)
            print(args, file=fobj)
            print(kwargs, file=fobj)
        global stopflag
        stopflag = True
    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)
    while not stopflag:
        time.sleep(1)
        print(time.time())

if __name__ == "__main__":
    print("start background application...")
    daemon_start(main, "background.pid", True)
```


### DaemonApplication包装类的使用

```
import time
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):
    def main(self):
        while True:
            print("hello")
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()

```

### 继承DaemonApplication包装类，并添加自定义参数

```
import time
import click
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):

    def get_main_options(self):
        options = [
            click.option("-m", "--message", default="hello")
        ]
        return options + super().get_main_options()

    def main(self):
        while True:
            print(self.config["message"])
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()
```

*添加自定义参数后的帮助信息*

```
Usage: example.py [OPTIONS] COMMAND [ARGS]...

Options:
  --pidfile TEXT          pidfile file path.
  --workspace TEXT        Set running folder
  --daemon / --no-daemon  Run application in background or in foreground.
  -c, --config TEXT       Config file path. Application will search config
                          file if this option is missing. Use sub-command
                          show-config-fileapaths to get the searching tactics.

  -m, --message TEXT
  --help                  Show this message and exit.

Commands:
  restart                Restart Daemon application.
  show-config-filepaths  Print out the config searching paths.
  start                  Start daemon application.
  stop                   Stop daemon application.
```

## 配置项及默认值

### 基础配置项及默认值

- pidfile: app.pid
- stop-timeout: 30
- stop-signal: SIGINT
- daemon: True
- workspace: ""
- loglevel: INFO
- logfile: app.log
- logfmt: default

### srpcd配置项及默认值

- server.listen: 0.0.0.0
- server.port: 8381
- server.class: daemon_application.app.SimpleXmlRpcServer
- enable-debug-service: true
- services: []

### services字段

- class: class path string, e.g. zenutils.serviceutils.DebugService
- args: []
- kwargs: {}

## 注意

程序的logging机制默认是没有启用的。你可以在main函数的首行，通过`logutils.setup(**self.config)`来启用它。

## 版本记录

### v0.5.6

- 增加SimpleRpcServer类以及srpcd命令。

### v0.5.5

- DaemonApplication中的config设置为dictutils.Object类，以便后续使用的方便，同时保持兼容dict的所有操作。
- daemon_stop增加stop_timeout。如果关闭进程超时，则直接强制关闭进程树。

### v0.5.4

- 文档更新

### v0.5.3

- 添加DaemonApplication.load_config，以便直接使用DaemonApplication对象。

### v0.5.2

- 增加loglevel/logfile/logfmt等日志选项。
- default_config重载机制更新。

### v0.4.4

- 修正stop子命令中的错误。

### v0.4.3

- 添加pyyaml依赖包。

### v0.4.2

- 删除无效的print语句。

### v0.4.1

- 修正文档链接。

### v0.4.0

- 迁移fastutils的依赖。
- DaemonApplication包装类中添加`--config`全局参数。
- 为DaemonApplication子类提供重载全局参数的机制。
- DaemonApplication包装类的子命令`restart`在进程不存在时，进行启动，而不是报错。
- 使用gitee.com做源代码托管。

### v0.3.3

- 修正show-config-filepaths子命令中的错误。

### v0.3.2

- 完善依赖包信息。

### v0.3.1

- 添加DaemonApplication包装类。

### v0.3.0

- 重构底层函数。

### v0.2.1

- 旧版本导入。
