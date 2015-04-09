# -*- coding:utf-8 -*-
# xk.py
# python 2.7.6
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
from bs4 import BeautifulSoup
from datetime import datetime


print 'Welcome to DillionWang\'s xk system (version:2.0 , 15.2.21)'
print ' ---*--- 猫猫抓课机 ---*--- '

login_url = 'http://xk.fudan.edu.cn/xk'
login_img_url = 'http://xk.fudan.edu.cn/xk/image.do'
login_post_url = login_url + '/loginServlet'

xk_url = 'http://xk.fudan.edu.cn/xk/input.jsp'
xk_post_url = 'http://xk.fudan.edu.cn/xk/doSelectServlet'

search_url = 'http://xk.fudan.edu.cn/xk/sekcoursepeos.jsp'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
}

with open('./login_data.txt' , 'rb') as f:
    ID = f.readline()[0:11]
    PW = f.readline()
    PW = PW[0:len(PW) - 1]
    class_code = f.readline()[0:13]

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support , urllib2.HTTPHandler)
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


# ****************** login *******************

while True:
    response = urllib2.urlopen(login_url)
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'
    }
    
    try:
        login_rand = get_img(login_img_url)
        print 'login_rand:' + login_rand
    except:
        print '** bad_image'
        continue
    
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
    if alert == 'Log-in failed. Username does not exsit or wrong password.':
        print alert
        print 'please check your data'
        print 'exiting the program'
        exit()
    if alert == 'Input student ID number in appropriate digits':
        print alert
        print 'please check your data'
        print 'exiting the program'
        exit()
    if alert == '验证码不正确!':
        print alert
        print 'trying again'
        continue
    with open('./login_response.html','wb') as f:
         f.write(text)
         f.close()
    break

print '* login successfully *'

# ********* get the image ***********

while True:
    img_pos = 2671
    response = urllib2.urlopen(xk_url)
    
    text = response.read()
    token_number = text[2686:2690]
    xk_img_url = 'http://xk.fudan.edu.cn/xk/image.do?token=' + token_number
    try:
        xk_rand = get_img(xk_img_url)
        print 'xk_rand:' + xk_rand
        xk_post_data = {'token':token_number,
                        'selectionId':str(class_code),
                        'xklb':'ss',
                        'rand':xk_rand
        }
        xk_post_data = urllib.urlencode(xk_post_data)
        break
    except:
        print '* bad image *'
        print '* get the image again *'


        
#********** wait for the beginning time ************

search_post_data = {'xkh':str(class_code),
                    'submit':'Inquiry',
                    'model':'空余人数查询'
}
search_post_data = urllib.urlencode(search_post_data)

request = urllib2.Request(search_url , search_post_data , headers)

i = 0

while True:
    
    print '%d : waiting for the beginning' % i
    
    print datetime.now().strftime('%c')

    time.sleep(0.3)

    i += 1

    response = urllib2.urlopen(request)

    text = response.read()

    '''
    with open('./search_response.html' , 'wb') as f:
        f.write(text)
        f.close()
    '''

    soup = BeautifulSoup(text)

    soup = soup.find_all('span')
    if len(soup) < 14 :
        print '* no avaliable course *'
        print '* exiting the program *'
        exit()
    avaliable_num = int(soup[11].string)
    restore_num = int(soup[12].string)
    #print avaliable_num
    #print restore_num
    if (avaliable_num > restore_num):
        break

#*************** start *****************

print '* start!!!!! *'

while True:
    request = urllib2.Request(xk_post_url , xk_post_data , headers)
    response = urllib2.urlopen(request)
    
    text = response.read()

    alert_begin_pos = 298
    alert_end_pos = text.find('");' , 298)
    alert = text[alert_begin_pos : alert_end_pos]
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
    if alert.find(str(class_code)) != -1 :
        print 'exiting the program'
        exit()
    print '* try again *'    
    
    response = urllib2.urlopen(xk_url)
    
    text = response.read()
    token_number = text[2686:2690]
    xk_img_url = 'http://xk.fudan.edu.cn/xk/image.do?token=' + token_number
    try:
        xk_rand = get_img(xk_img_url)
        print 'xk_rand:' + xk_rand
        xk_post_data = {'token':token_number,
                        'selectionId':str(class_code),
                        'xklb':'ss',
                        'rand':xk_rand
        }
        xk_post_data = urllib.urlencode(xk_post_data)
        break
    except:
        print '* bad image *'
        print '* get the image again *'
