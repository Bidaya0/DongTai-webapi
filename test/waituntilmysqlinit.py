######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : waituntilmysqlfinish
# @created     : 星期五 10月 15, 2021 15:43:54 CST
#
# @description : 
######################################################################


import requests

res = requests.get('http://localhost:8000/api/v1/captcha')
while True:
    res = requests.get('http://localhost:8000/api/v1/captcha/refresh')
    if res.status_code == 200:
        break
