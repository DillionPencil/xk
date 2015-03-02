import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re

hosturl = 'http://xk.fudan.edu.cn/xk'
imgurl = 'http://xk.fudan.edu.cn/xk/image.do'
posturl = hosturl + '/loginServlet'
print posturl

def get_img(imgurl , headers):
    img = urllib2.urlopen(imgurl)
    with open('/home/dillion/bin/img.jpg' , 'wb') as f:
        f.write(img.read())
        f.close()
        rand = raw_input()
        return rand

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support , urllib2.HTTPHandler)
urllib2.install_opener(opener)

h = urllib2.urlopen(hosturl)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer':'http://xk.fudan.edu.cn/xk'
}

tmp_rand = get_img(imgurl , headers)

postData = {'studentId':13307130109,
            'password':'3223232a',
            'rand':tmp_rand,
            'Submit2':'Submit'
}
postData = urllib.urlencode(postData)

request = urllib2.Request(posturl , postData , headers)
print request
response = urllib2.urlopen(request)
text = response.read()
with open('/home/dillion/bin/test.html' , 'wb') as f:
    f.write(text)
    f.close()

hosturl = 'http://xk.fudan.edu.cn/xk/input.jsp'
posturl = 'http://xk.fudan.edu.cn/xk/doSelectServlet'

h = urllib2.urlopen(hosturl)

# with open('/home/dillion/bin/test1.html' , 'wb') as f:
#     f.write(h.read())
#     f.close()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer':'http://xk.fudan.edu.cn/input.jsp'
}

text = h.read()
img_pos = text.find('image.do')
token_number = text[img_pos+15:img_pos+19]
imgurl = 'http://xk.fudan.edu.cn/xk/image.do?token=' + token_number
tmp_rand = get_img(imgurl , headers)
postData = {'token':token_number,
            'selectionId':'COMP130007.01',
            'xklb':'ss',
            'rand':tmp_rand
}
postData = urllib.urlencode(postData)

request = urllib2.Request(posturl , postData , headers)
print request
response = urllib2.urlopen(request)
text = response.read()
with open('/home/dillion/bin/test2.html' , 'wb') as f:
    f.write(text)
    f.close()


