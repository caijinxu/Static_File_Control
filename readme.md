### Static_File_Control



一个用于WEB集群的WEB静态文件操作项目。项目采用C/S架构，控制节点部署完成后，操作节点部署方便快捷。



[相应操作节点项目]: https://github.com/caijinxu/img_worker

![readme](.\readme.png)

## 功能

1. WEB页面静态文件、图片移出或者恢复回原有目录
2. 后台白名单管理
3. 操作节点配置下发、健康检查
4. 自动分析页面链接中图片链接，然后做移出和恢复操作
5. 网宿CDN缓存刷新
6. 百度死链处理
7. 支持操作华为OBS
8. 根据日志批量恢复操作
9. Elasticsearch文章全文搜索



### 项目架构



## 部署

### 安装虚拟环境

conda create -n imagedelete python=3
进入虚拟环境
conda activate imagedelete

### ETCD 安装

export HostIP="10.3.1.92"
docker run -d  -p 4001:4001 -p 2380:2380 -p 2379:2379 \
--name etcd quay.io/coreos/etcd\
 /usr/local/bin/etcd \
 --name etcd \
 --auto-compaction-retention=1 \
 --advertise-client-urls http://${HostIP}:2379,http://${HostIP}:4001 \
 --listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
 --initial-advertise-peer-urls http://${HostIP}:2380 \
 --listen-peer-urls http://0.0.0.0:2380 \
 --initial-cluster-token etcd-cluster-1 \
 --initial-cluster etcd=http://${HostIP}:2380 \
 --initial-cluster-state new

#### ETCD 操作

进入etcd：
    docker exec -it etcd /bin/sh

查看版本：
    ETCDCTL_API=3 /usr/local/bin/etcdctl version
设置etcdctlban版本为V3 # etcd v2/v3版本不兼容，数据不互通
    export ETCDCTL_API=3
权限设置：
    创建root用户：
        etcdctl --endpoints=http://10.3.1.92:2379 user add root  #密码：cnsys123!

开启认证：
    etcdctl --endpoints http://10.3.1.92:2379  auth enable

创建普通用户：
    etcdctl --endpoints=http://10.3.1.92:2379 --user=root:cnsys123! user add workeruser # 密码：123456

创建普通角色：
    etcdctl --endpoints http://10.3.1.92:2379 --user=root:cnsys123! role add normal

普通用户添加授权：
    etcdctl --endpoints http://10.3.1.92:2379  --user=root:cnsys123!  role  grant-permission normal --prefix=true  read  /
    etcdctl --endpoints http://10.3.1.92:2379  --user=root:cnsys123!  role grant-permission normal  --prefix=true  readwrite /online_work/

用户绑定角色：
    etcdctl --endpoints http://10.3.1.92:2379 --user=root:cnsys123! user  grant-role workeruser normal



### MYSQL docker执行

docker run --name mysql -p3306:3306 -v /mysqldata/data:/var/lib/mysql -v /mysqldata/my.cnf:/etc/mysql/my.cnf -e TZ=Asia/Shanghai -d mysql:5.7

### MONGODB docker启动执行

docker run --name mongo -p27017:27017 -v /mongodata/data:/data/db   -d mongo:latest

MongoDB 设置
    设置验证登录
        use admin
        db.createUser({user: 'root',pwd: 'admin',roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]});
    创建项目用户
        use task
        db.createUser({user: 'article_search',pwd: 'zbemcL05Tl',roles: [ { role: "readWrite", db: "task" } ] });





