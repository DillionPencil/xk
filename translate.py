# translate.py
# python 2.7.6
__author__ = 'DillionWang'

# This file must be in the same dir with the svm library

from sys import path
import os
path.append(os.path.abspath('./libsvm-3.20/python/'))
from svmutil import *
from PIL import Image

charlist = ['2','3','4','5','6','7','8','b','c','d','e','f','g','m','n','p','w','x','y']

def not_blank(pixel):
    if pixel[0] < 128 or pixel[1] < 128 or pixel[2] < 128:
        return True
    return False

def pic2words(img):
    # l = 70
    # h = 24
    # os.remove(os.path.abspath('./svm_data'))
    # svm_f = open(os.path.abspath('./svm_data') , 'w')
    svm_f = open('./svm_data' , 'w')
    svm_f.close()
    svm_f = open('./svm_data' , 'a')
    # os.remove(os.path.abspath('./trans_data'))
    trans_f = open('./trans_data' , 'w')
    trans_f.close()
    trans_f = open('./trans_data' , 'a')
    for i in range(4):
        svm_f.write('0 ')
        # find the boundary
        l = 3 + i * 10
        top = 100
        bottom = -1
        for y in range(24):
            for x in range(l , l + 10):
                if not_blank(img.getpixel((x,y))):
                    if (top > y):
                        top = y
                    if (bottom < y):
                        bottom = y
        tmp = bottom - top - 12
        bottom -= tmp / 2
        top += tmp - tmp / 2
        # turn into svm format data
        z = 1
        for x in range(l , l + 10):
            for y in range(top , bottom):
                if not_blank(img.getpixel((x,y))):
                    svm_f.write('%d:%.3f ' % (z , 0.999))
                else:
                    svm_f.write('%d:%.3f ' % (z , 0.001))
                z += 1
        svm_f.write('\r\n')
    svm_f.close()
    model = svm_load_model('./xkdata.model')
    data = svm_read_problem('./svm_data')
    p = svm_predict(data[0] , data[1] , model)
    rand = []
    for i in range(4):
        rand.append(charlist[int(p[0][i])])
    # print rand
    return rand

# img = Image.open('./img.jpg')
# pic2words(img)
