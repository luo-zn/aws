# AWS

在aws平台上使用相关服务时所需要的工具

## 安装基于docker镜像的aws-cli命令

1. wget  <https://github.com/luo-zn/aws/releases/download/1.0/aws-cli.sh> -O /usr/local/bin/aws-cli
2. chmod +x /usr/local/bin/aws-cli
3. aws-cli --help 查看更多帮助

## elb-check

elb-check用于响应AWS的ELB服务心跳检查

### 使用方式

1. 在运行http服务的EC2虚拟机执行: docker run -d -p 9999:9999 --restart unless-stopped jenner/elb-http-check
2. 在运行tcp或udp服务的EC2虚拟机执行: docker run -d -p 9999:9999 --restart unless-stopped jenner/elb-tcp-check
3. 配置负载均衡器(ELB)目标组的运行状况检查，如图所示
![elb-http-check](/elb-check/imgs/http-check.PNG "elb-http-check") ![elb-tcp-check](/elb-check/imgs/tcp-check.PNG "elb-tcp-check")
