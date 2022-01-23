# myflask
Flask初学，NGINX+uwsgi部署
查看版本：
cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_CODENAME=focal
DISTRIB_DESCRIPTION="Ubuntu 20.04 LTS"

1、添加一个用户
新增用户：
sudo adduser yongzhen

添加sudo权限：
sudo usermod -a -G sudo yongzhen

环境准备：
安装Python，pip以及nginx：
sudo apt-get update
sudo apt-get install python-pip python-dev nginx



虚拟环境
# 安装virtualenv：
pip install virtualenv
# 创建目录：
mkdir ~/myflask
cd ~/myflask
# 创建虚拟环境目录：
virtualenv venv
# 激活新创建的虚拟环境：
source venv/bin/activate
# 确认虚拟环境
pip -V   
# 安装Python库：uwsgi和flask
pip install uwsgi flask

# 拉取代码：
git clone https://github.com/lyndonlv/myflask.git
运行 python run.py ，然后本地访问 http://127.0.0.1:5000 将会看到：服务启动返回数据

使用uwsgi部署Flask项目
使用uwsgi部署Flask项目只需要换一种命令来启动服务即可：
uwsgi --socket 0.0.0.0:5000 --protocol=http -p 3 -w run:app
我们来对uwsgi的参数进行分别讲解：

--socket 0.0.0.0:5000：指定暴露端口号为5000。
--protocol=http：说明使用 http 协议，即端口5000可以直接使用HTTP请求进行访问。
-p 3表示启动的服务占用3个进程。
-w run:app：-w 指明了要启动的模块，run 就是项目启动文件 run.py 去掉扩展名，app 是 run.py 文件中的变量 app，即 Flask 实例。
至此，我们已经正常使用uwsgi部署了Flask项目。

使用nginx + uwsgi部署Flask项目
既然我们已经可以好似用uwsgi来部署Flask项目了，那么我们为什么还要使用Nginx + uwsgi来部署呢？
使用Nginx有如下一些优点：

安全：不管什么请求都要经过代理服务器，这样就避免了外部程序直接攻击web服务器
负载均衡：根据请求情况和服务器负载情况，将请求分配给不同的web服务器，保证服务器性能
提高web服务器的IO性能：对于一些静态文件，可以直接由反向代理处理，不经过web服务器
那么，应该如何将Nginx与uwsgi结合来部署Flask项目呢？

在开始讲解Nginx之前，我们首先讲解如何将复杂的uwsgi命令参数保存在配置文件中，从而每次启动uwsgi时，无需添加繁琐的参数，只需要指定配置文件即可。
编辑/home/xiaoju/myflask/uwsgi.ini：

[uwsgi]
module = run:app
master = true
processes = 3
chdir1=/home/xiaoju/myflask
home=/home/xiaoju/myflask/venv
socket = 127.0.0.1:8000
chmod-socket = 660
vacuum = true
socket=%(chdir1)/uwsgi/uwsgi.sock
stats=%(chdir1)/uwsgi/uwsgi.status
pidfile=%(chdir1)/uwsgi/uwsgi.pid
logto=%(chdir1)/uwsgi/uwsgi.log

其中，文件参数说明如下：
- module相当于之前命令行中的-w参数；
- processes相当于之前的-p参数；
- socket此处包含两个，一个是指定了暴露的端口，另外指定了一个myproject.sock文件保存socker信息。
- chdir是项目路径地址。
- logto是日志输出地址。

可以看到，此处我们没有添加--protocol=http对应的配置信息。
即此时我们暴露的端口不能使用HTTP请求直接访问，当时需要经过Nginx进行反向代理。
此时，我们可以执行如下命令来通过配置文件启动uwsgi：

uwsgi --ini /home/xiaoju/myflask/uwsgi.ini
此时，我们已经正常启动了uWsgi服务，但是无法直接访问，需要继续部署Nginx服务。

下面，我们来编辑Nginx的配置文件/home/xiaoju/myflask/nginx.conf：

worker_processes 4;
events { worker_connections 1024; }
http {
    include       mime.types;
    default_type  application/octet-stream;
    server {
        listen 80;
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;
        }
    }
}
其中，如下两行指定反向代理的信息：
include uwsgi_params;
uwsgi_pass 127.0.0.1:8000;
两个分别指明了代理的解析方式是通过uwsgi解析以及uWsgi暴露的端口地址为127.0.0.1:8000。
下面，我们启动Nginx服务：

nginx -c /home/xiaoju/myflask/nginx.conf
nginx -s reload
启动完成后，由于nginx本身监听的端口是80端口，因此我们可以直接访问机器地址进行访问



参考文档：
使用Flask+uwsgi+Nginx部署Flask正式环境
https://www.missshi.cn/api/view/blog/5b1511a213d85b1251000000

更改pip源为国内镜像源
https://developer.aliyun.com/mirror/pypi





# flask  使用

# 常用过滤器
abs(value)：返回一个数值的绝对值。 例如：-1|abs。
default(value,default_value,boolean=false)：如果当前变量没有值，则会使用参数中的值来代替。name|default('xiaotuo')——如果name不存在，则会使用xiaotuo来替代。boolean=False默认是在只有这个变量为undefined的时候才会使用default中的值，如果想使用python的形式判断是否为false，则可以传递boolean=true。也可以使用or来替换。
escape(value)或e：转义字符，会将<、>等符号转义成HTML中的符号。例如：content|escape或content|e。
first(value)：返回一个序列的第一个元素。names|first。
format(value,*arags,**kwargs)：格式化字符串。例如以下代码：
        {{ "%s" - "%s"|format('Hello?',"Foo!") }}
        将输出：Helloo? - Foo!
last(value)：返回一个序列的最后一个元素。示例：names|last。
length(value)：返回一个序列或者字典的长度。示例：names|length。
join(value,d=u'')：将一个序列用d这个参数的值拼接成字符串。
safe(value)：如果开启了全局转义，那么safe过滤器会将变量关掉转义。示例：content_html|safe。
int(value)：将值转换为int类型。
float(value)：将值转换为float类型。
lower(value)：将字符串转换为小写。
upper(value)：将字符串转换为小写。
replace(value,old,new)： 替换将old替换为new的字符串。
truncate(value,length=255,killwords=False)：截取length长度的字符串。
striptags(value)：删除字符串中所有的HTML标签，如果出现多个空格，将替换成一个空格。
trim：截取字符串前面和后面的空白字符。
string(value)：将变量转换成字符串。
wordcount(s)：计算一个长字符串中单词的个数。

# 模板继承
父级页面为 base.html  
子级页面   about.html   index.html

# 静态文件配置
{% block head %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
{% endblock %}


