# XWBOT

## 简介

一个自己手搓的 QQ BOT 项目，功能主要是一些实用的工具

~~早知道就用 Nonebot 了，何必自己造轮子~~

## 快速开始

### 使用 Docker 部署

运行以下命令，即可拉取镜像并运行，您需要拷贝 `config/config_example.yml` 到 `$PWD/xwbot/config/config.yml` 并修改配置

数据库可能需要额外安装并配置，初始化数据库请查看 `sql` 文件夹
```shell
docker run -itd -v $PWD/xwbot/config/config.yml:/app/config/config.yml --name=xwbot --pull=always --restart=always ghcr.io/xiwangly2/xwbot:main
```

`ghcr.io/xiwangly2/xwbot:main` 镜像同时安装了多种数据库的依赖支持，如果您想要更精简,可以自行构建镜像

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
# 选择数据库
select_database: 'postgresql' # 目前支持的选项有 mysql、postgresql、sqlite，mongo，您可以根据自己的需求选择

# 管理员列表
admin: # 这些列表决定了谁可以使用管理员命令和一些危险的命令，填写 QQ 号
  - '1000'
  - '1001'
```

我们建议将支持 OneBot 的机器人框架、数据库和本程序运行在同一个内网环境中，以减少网络延迟

### 更新/卸载

移除容器和镜像
`docker stop xwbot || docker rm xwbot || docker rmi ghcr.io/xiwangly2/xwbot:main`

要更新的话就再执行一遍安装步骤

## 手动部署

您需要自行安装 Python 环境，然后然后`pip install -r requirements.txt`，安装依赖


首次使用请将`config/config_example.yml`复制到`config/config.yml`
并编辑其中的设置，并且正确的配置 正向 websocket 通信

现在已适配 OneBot 11，目前我测试了 go-cqhttp 和 NapCat 都没问题

另外，还需要数据库的存储支持，自己看着办吧

别忘了导入数据库完成初始化，在`sql`文件夹里

自动化的部署脚本在写了……

> 如果 go-cqhttp 和数据库配置正常的话，您需要在分别在不同的群聊、私聊回复`/on`开启机器人（需要配置管理员QQ），这有效地避免了对一些无关的群聊的骚扰，~~这样可以有效地潜伏在正常的群里面~~