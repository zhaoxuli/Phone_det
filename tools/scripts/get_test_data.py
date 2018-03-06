# -*- coding: utf-8 -*-
import os
import json  as js

def save_js(ctx,new_js,num):
    file = open(new_js,'a')
    ctx = js.loads(ctx)
    ctx['image_key'] = num
    jsctx = js.dumps(ctx)+'\n'
    file.write(jsctx)
    file.close

def run(js_path,new_js,out_file,num):
    count =0
    ctx = open(js_path,'r').readlines()
    while (int(count)<int(len(ctx)-1)):
        ele =ctx[count]
        save_js(ele,new_js,num)
        ele = js.loads(ele)
        img_key = ele['image_key']
        #img_path = './Anno1213'+os.sep+js_path.split(os.sep)[-1][0:-5]+os.sep+img_key
        img_path = js_path.split(os.sep)[-1][0:-5]+os.sep+img_key
        cmd ='mv '+img_path+' '+out_file+os.sep+str(num)+'.png'
        print cmd
        os.system(cmd)
 #  #     #print img_path
 #  #     #change new_js
        del ctx[count]
        count = count +5
        num = num +1
 #  #     #print count
    file  = open(js_path,'w')
    for line in ctx:
        file.write(line)
    file.close
    return num

img_path = './crop_Net_data/Image'
js_path = './crop_Net_data/Anno'
new_js = './crop_Net_data/test_Net/test_Net_data.json'
out_file = './crop_Net_data/test_Net/test_Net_data'
if  os.path.exists(out_file) == False:
    os.makedirs(out_file)

js_lst = os.listdir(js_path)
num = 0
for ele  in js_lst:
    js_file = js_path+os.sep+ele
    num = run(img_path,js_file,new_js,out_file,num)
