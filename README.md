# XWBOT

## 简介

一个自己手搓的 QQ BOT 项目，功能主要是一些实用的工具

~~早知道就用 Nonebot 了，何必自己造轮子~~

## 开始

您可以使用 [Docker](#使用docker) 安装，安装前请配置 go-cqhttp 和 MySQL 的连接信息（MySQL 可能需要自己部署）

目前在 dev 更多数据库的支持，……咕咕咕

或者是自己手动部署

下面的内容请根据使用的实际情况修改，不建议直接照抄

## 使用Docker

以下方法多选一

### (一)自己 Build

先克隆本仓库

`docker build -t xiwangly/xwbot .`

### (二)从 ghcr 拉取镜像

（推荐使用，ghcr会实时根据更改构建镜像）
```sh
docker run -itd -v $PWD/xwbot/config:/app/config --name=xwbot --net=host --restart=always ghcr.io/xiwangly2/xwbot:main
```

其实你可用不用 host 网络，但是我懒得改了，自己映射要用的端口

### (三)从 DockerHub 拉取镜像

```sh
docker run -itd -v $PWD/xwbot/config:/app/config --name=xwbot --net=host --restart=always xiwangly/xwbot
```

### 更新/卸载

移除容器和镜像
`docker stop xwbot || docker rm xwbot || docker rmi ghcr.io/xiwangly2/xwbot:main`

要更新的话就再执行一遍安装步骤

##手动部署

您需要自己安装 Python 环境，然后然后`pip install -r requirements.txt`，安装依赖


首次使用请将`config/config_example.yml`复制到`config/config.yml`
并编辑其中的设置，并且正确的配置 正向 websocket 通信

现在已适配 OneBot 11，目前我测试了 go-cqhttp 和 NapCat 都没问题

另外，还需要MySQL的存储支持，自己看着办吧

别忘了导入数据库完成初始化，在`sql`文件夹里

自动化的部署脚本在写了……

> 如果 go-cqhttp 和数据库配置正常的话，您需要在分别在不同的群聊、私聊回复`/on`开启机器人（需要配置管理员QQ），这有效的避免了对一些无关的群聊的骚扰，~~这样可以有效的潜伏在正常的群里面~~