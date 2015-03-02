# -*- coding=utf-8 -*-
# xk.py
# python 2.6.7
__author__ = 'DillionWang'

import StringIO
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import time
from PIL import Image
import translate


print 'Welcome to DillionWang\'s xk system (version:1.0 , 15.2.21)'
print ' ---*--- 猫猫抓课机 ---*--- '

ID = '13307130109'
PW = '3223232a'
class_code = 'COMP130007.01'

cj = cookielib.LWPCookieJar()
cookie_suppert = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_suppert , urllib2.HTTPHandler)
urllib2.install_opener(opener)

def get_img(imgurl):
    img = urllib2.urlopen(imgurl)
    text = img.read()

    time.sleep(3)

    with open('./img.jpg' , 'wb') as f:
        f.write(text)
        f.close()
    image = Image.open(StringIO.StringIO(text))
    rand = translate.pic2words(image)
    return rand[0] + rand[1] + rand[2] + rand[3]

while True:
    login_url = 'http://xk.fudan.edu.cn/xk'
    login_img_url = 'http://xk.fudan.edu.cn/xk/image.do'
    login_post_url = login_url + '/loginServlet'
    
    response = urllib2.urlopen(login_url)
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer':'http://xk.fudan.edu.cn/xk'
           }
    
    login_rand = get_img(login_img_url)
    print 'login_rand:' + login_rand
    
    login_post_data = {'studentId':ID,
                       'password':PW,
                       'rand':login_rand,
                       'Submit2':'Submit'
                   }
    login_post_data = urllib.urlencode(login_post_data)
    
    request = urllib2.Request(login_post_url , login_post_data , headers)
    response = urllib2.urlopen(request)
    
    text = response.read()
    
    alert_begin_pos = 1134
    alert_end_pos = text.find(')' , 1134)
    alert = text[alert_begin_pos : alert_end_pos-1]
    print alert
    if alert == 'Log-in failed. Username does not exsit or wrong password.':
        print 'please check your data'
        print 'exiting the program'
        exit()
    if alert == 'Input student ID number in appropriate digits':
        print 'please check your data'
        print 'exiting the program'
        exit()
    if alert == '验证码不正确!':
        print 'trying again'
        continue
    with open('./login_response.html','wb') as f:
         f.write(text)
         f.close()
    break

# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

print 'login successfully'

while True:
    xk_url = 'http://xk.fudan.edu.cn/xk/input.jsp'
    xk_post_url = 'http://xk.fudan.edu.cn/xk/doSelectServlet'
    
    response = urllib2.urlopen(xk_url)
    
    text = response.read()
    img_pos = 2671
    token_number = text[2686:2690]
    xk_img_url = 'http://xk.fudan.edu.cn/xk/image.do?token=' + token_number
    xk_rand = get_img(xk_img_url)
    print 'xk_rand:' + xk_rand
    
    xk_post_data = {'token':token_number,
                    'selectionId':str(class_code),
                    'xklb':'ss',
                    'rand':xk_rand
    }
    xk_post_data = urllib.urlencode(xk_post_data)
    
    request = urllib2.Request(xk_post_url , xk_post_data , headers)
    response = urllib2.urlopen(request)
    
    text = response.read()
    with open('./result.html' , 'wb') as f:
        f.write(text)
        f.close()
    alert_begin_pos = 298
    alert_end_pos = text.find(')' , 298)
    alert = text[alert_begin_pos : alert_end_pos-1]
    print alert
    if alert == 'Course added' :
        print 'exiting the program'
        exit()
    if alert == 'You have already selected the course.' :
        print 'exiting the program'
        exit()
    if alert == 'The course is not available this semester or your input course code is wrong.' :
        print 'Please check your course code'
        print 'exiting the program'
        exit()
