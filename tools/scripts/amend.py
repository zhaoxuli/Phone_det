# -*- coding: utf-8 -*-
import os
import cv2
import json

#img_path = './test_data/'
#js_path = '../Anno/test_data.json'

def amend_js(js_path,img_path,new_js):
    js_ctx = open(js_path,'r').readlines()
    num = 0
    new_ctx = open(new_js,'w')
    while(num <len(js_ctx)):
        ele = js_ctx[num]
        ele = json.loads(ele)
        img_key = ele['image_key']
        img_url = img_path+os.sep+img_key
        img = cv2.imread(img_url)
        if img == None:
            print img_key
        else :
            w,h,c = img.shape
            ele['width'] = w
            ele['height'] = h
            js_ele = json.dumps(ele)+'\n'
            new_ctx.write(js_ele)
        num += 1
    new_ctx.close
    return

if __name__ == '__main__':
    img_all = './Image'
    js_path = './Anno_temp/'
    out_json_folder = './Anno_new_temp'
    js_list = os.listdir(js_path)
    for ele  in js_list:
        js_url = js_path+os.sep+ele
        js_key = ele[:-5]
        print js_key
        if os.path.exists(out_json_folder) ==False:
            os.makedirs(out_json_folder)
        new_js = out_json_folder+os.sep+js_key+'.json'
        img_path = img_all +os.sep+js_key
        amend_js(js_url,img_path,new_js)


















