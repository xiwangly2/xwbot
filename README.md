# XWBOT

## 简介

一个自己手搓的 QQ BOT 项目，功能主要是一些实用的工具

~~早知道就用 Nonebot 了，何必自己造轮子~~

## 快速开始

### 使用 Docker 部署

运行以下命令，即可拉取镜像并运行，您需要拷贝 `config/config_example.yml` 到 `$PWD/xwbot/config/config.yml` 并修改配置

数据库可能需要额外安装并配置，如果您使用的是 sqlite3，那么无需额外配置

```shell
mkdir -p $PWD/xwbot/config
curl -o $PWD/xwbot/config/config.yml https://raw.githubusercontent.com/xiwangly2/xwbot/refs/heads/main/config/config_example.yml
docker run -itd -v $PWD/xwbot/config/config.yml:/app/config/config.yml --name=xwbot --pull=always --restart=always ghcr.io/xiwangly2/xwbot:main
```

您可能需要自行映射端口和配置网络，或者使用`--network host`参数，以便让程序能够访问到 OneBot WebSocket 服务器

`ghcr.io/xiwangly2/xwbot:main` 镜像同时安装了多种数据库的依赖支持，如果您想要更精简，可以自行构建镜像

目前 amd64 和 arm64 架构的 docker 镜像安装了完整的依赖，其它的架构由于适配问题暂时未安装完整依赖

## 配置说明

配置文件在`config/config_example.yml`，您需要将`config/config_example.yml`复制到`config/config.yml`并编辑其中的设置

```yaml
# 使用正向 Websocket
# OneBot WebSocket 服务器地址
host: '127.0.0.1' # 如果支持 OneBot 的机器人框架运行同在一台 1Panel 服务器上且均使用 Docker部署，可以使用 172.18.0.1
# OneBot WebSocket 服务器端口
port: '6700'
# 访问令牌
access_token: '' # 这个配置默认为空，如果您的 OneBot WebSocket 服务器自行配置了访问令牌，请填写
# 调试模式
debug: false # 这个配置默认为 false，如果您需要调试，请设置为 true，这将会输出详尽的日志信息
# 写日志
write_log: true # 这个配置默认为 true，如果您不需要写日志，请设置为 false，写日志会将所有对话记录写入到数据库中
# 遇到错误自动重启
auto_reconnect: false # 这个配置默认为 false，如果 Docker 容器的重启策略是 自动重启，建议保持设置为 false，这对于独立部署的程序且没有守护进程的情况下，可以保证程序不会因为错误而终止

# 管理员列表
admin: # 这些列表决定了谁可以使用管理员命令和一些危险的命令，填写 QQ 号
  - '1000'
  - '1001'

sql: # 数据库配置，多选一
  type: "sqlite3" # 数据库类型，目前支持 sqlite3，mysql，postgres, dsn（其它的需要自行解决依赖）
```

```yaml
# 一些可选的配置示例，具体的配置请参考 sqlalchemy 的文档
sql:
#    ...
    <sql_type>:
      connect_args: {
        ssl: "true", # 是否使用 ssl 连接数据库
        ssl_ca: '/path/to/ca.pem', # ssl ca 证书路径
        ssl_cert: '/path/to/client-cert.pem', # ssl client 证书路径
        ssl_key: '/path/to/client-key.pem', # ssl client key 证书路径
        ssl_verify: "true", # 是否验证 ssl 证书
      }
```

以上配置文件可能会有所变动而没来得及更新，以最新提交的示例配置文件为准

我们建议将支持 OneBot 的机器人框架、数据库和本程序运行在同一个内网环境中，以减少网络延迟

### 更新/卸载

移除容器和镜像

```shell
docker stop xwbot
docker rm xwbot
docker rmi ghcr.io/xiwangly2/xwbot:main
```

要更新的话就再执行一遍安装步骤

## 手动部署

您需要自行安装 Python 环境，然后然后`pip install -r requirements.txt`，安装依赖

首次使用请将`config/config_example.yml`复制到`config/config.yml`
并编辑其中的设置，并且正确的配置 正向 websocket 通信

现在已适配 OneBot 11，目前我测试了 go-cqhttp 和 NapCat 都没问题

自动化的部署脚本在写了……

> 如果 go-cqhttp 和数据库配置正常的话，您需要在分别在不同的群聊、私聊回复`/on`开启机器人（需要配置管理员QQ），这有效地避免了对一些无关的群聊的骚扰，
~~这样可以有效地潜伏在正常的群里面~~


> [!WARNING]
> 请注意，在 s390x 架构上，可能会出现一些问题，这是因为某些依赖库（如 psycopg2 ）不支持这些架构，如果您遇到了这些问题，请自行解决
