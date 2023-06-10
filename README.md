# XWBOT

手捏项目中……

~~早知道就用Nonebot了，何必自己造轮子~~

首次使用请将`config/config_example.yml`复制到`config/config.yml`
并编辑其中的设置，并且正确的配置[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)的正向websocket通信

Python依赖别忘了安装，cd到目录，然后`pip install -r requirements.txt`，一键安装依赖

另外，还需要MySQL的存储支持

别忘了导入数据库完成初始化

自动化的部署脚本在写了……

## 使用Docker

docker build -t xiwangly/xwbot .

docker run -itd -v /www/wwwroot/xwbot/config/config.yml:/app/config/config.yml --name=xwbot --net=host --restart=always xiwangly/xwbot