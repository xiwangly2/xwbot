# XWBOT

手捏项目中……

~~早知道就用 Nonebot 了，何必自己造轮子~~

首次使用请将`config/config_example.yml`复制到`config/config.yml`
并编辑其中的设置，并且正确的配置 [Go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的正向 websocket 通信

Python 依赖别忘了安装， cd 到目录，然后`pip install -r requirements.txt`，一键安装依赖

另外，还需要MySQL的存储支持

别忘了导入数据库完成初始化

自动化的部署脚本在写了……

## 使用Docker

`docker build -t xiwangly/xwbot .`

### 从 ghcr 拉取镜像
```sh
docker run -itd -v /www/wwwroot/go-cqhttp:/data --name=xwbot --net=host --restart=always ghcr.io/xiwangly2/xwbot:main
```

### 从 DockerHub 拉取镜像

```sh
docker run -itd -v /www/wwwroot/go-cqhttp:/data --name=xwbot --net=host --restart=always xiwangly/xwbot
```

## 更新/卸载

移除容器和镜像
`docker stop xwbot && docker rm xwbot && docker rmi ghcr.io/xiwangly2/xwbot:main`

移除配置文件
`rm -r /www/wwwroot/go-cqhttp`

要更新的话就再执行一遍安装步骤

## 如何开始

如果 go-cqhttp 和数据库配置正常的话，您需要在分别在不同的群聊、私聊回复`/on`开启机器人（需要配置管理员QQ），这有效的避免了对一些无关的群聊的骚扰