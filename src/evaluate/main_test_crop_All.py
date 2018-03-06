# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 12:06:16 2017

@author: root
"""

import os,sys
import eval_all_in_one as evl
import  json
import pylab
import numpy as np

def generate_det(data_txt):
    f = open(data_txt,'r')
    lines = f.readlines()
    det_list = dict()
    for line in lines:
        temp = line.split()
        #temp = re.findall(r"\d+\.?\d*",line)
        rects = []
        #print line
        for i in range(1,(len(temp)-1),):
            if (temp[i] == '[') or (temp[i] == ']['):
                #print temp[i+1],temp[i+2],temp[i+3],temp[i+4],temp[i+5]
                try:
                    rects.append([float(temp[i+1]),float(temp[i+2]),float(temp[i+3]),float(temp[i+4]),float(temp[i+5])])
                except:
                    print  temp[0]
        det_list[temp[0]] = rects
    det_list.pop('None')
    return det_list



def json2list(prefix_path):
        js_list = os.listdir(prefix_path)
        gt = dict()
        for  data_json in js_list:
            #js_key = data_json[:,-5]
            if  data_json.split('.')[-1] == 'json':
                print 'a',data_json
                folder_name = data_json.split(os.sep)[-1].split('.')[0]
                lines = open(prefix_path+os.sep+data_json, 'r').readlines()
                object_type='common_box'
                for line in lines:
                    if (line[0]!= '#'):
                        json_dict = json.loads(line)
                        img_url = os.path.join(folder_name + os.sep + str(json_dict['image_key']))

                        rect = []
                        if json_dict.has_key(object_type):
                            objs = json_dict[object_type]
                            rect.append(map(float, objs[0]['data']))
                            gt[img_url]=rect
        return gt



print' python  main.py    dt_path   img_path  tag'


gt_list = json2list('../crop_result_All/')

det_path=  sys.argv[1]
dt_list = generate_det(det_path)

img_path = sys.argv[2]

tag = sys.argv[3]
if not os.path.exists(img_path):
    os.makedirs(img_path)
evl.eval_detection(gt_list,dt_list,det_path.split('/')[-1].split('.')[0],tag, img_path)




