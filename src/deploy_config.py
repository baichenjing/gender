import os
bind='0.0.0.0:10001' #绑定的端口
workers=1 #worker数量
backlog=2048
debug=True
proc_name='gunicorn_gender.pid'
pidfile='/home/ec2-user/xiaotao/gender-service/log/gunicorn-debug.log'
loglevel='debug'
