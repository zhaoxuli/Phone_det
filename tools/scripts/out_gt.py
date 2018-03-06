# -*- coding: utf-8 -*-
import cv2
import os
import  json



def write_img(img_url,str_points,out_path):
    img_key = img_url.split(os.sep)[-1]
    points = []
    #points.replace(' ','')
    if str_points != 'false':
        lx = int(str_points[0])
        ly = int(str_points[1])
        rx = int(str_points[2])
        ry = int(str_points[3])
    else:
        lx,ly,rx,ry = [0,0,0,0]
    img = cv2.imread(img_url)
    print img_url
    cv2.rectangle(img,(int(lx),int(ly)),(int(rx),int(ry)),(0,255,0),1)
    cv2.imwrite(out_path +os.sep+'rec'+img_key,img)
    print out_path +os.sep+'rec'+img_key
    return

def get_gt_list(js_path):
    pre_img = js_path.split(os.sep)[-1][:-5]
    #print pre_img
    gt_dict = {}
    js_lines = open(js_path,'r').readlines()
    for ele in js_lines:
        ele  = json.loads(ele)
        #print ele
        img_key =pre_img+os.sep+ str(ele["image_key"])
        try:
            points = ele["common_box"][0]['data']
        except:
            points = [0,0,0,0]
        #image_key  heigt   wideth  type  x1,y1,x2,y2  left top right  bottom
        gt_dict[img_key] = points

    return gt_dict

if  __name__ == '__main__':
    js_path ='/mnt/hgfs/work/Phone_data/Work/Aug_data/Anno/'
    img_path = '/mnt/hgfs/work/Phone_data/Work/Aug_data/Image'
    js_list = os.listdir(js_path)
    for ele in  js_list:
        folder_key = ele[:-5]
        out_path = './out_gt'+os.sep+ folder_key
        #out_path = '/mnt/hgfs/work/Phone_data/Phone_crop_face_rec/crop_Net_data/out_gt'+os.sep+ folder_key
        if os.path.exists(out_path) == False:
            os.makedirs(out_path)
        js_file = js_path + os.sep + ele
        #img_folder = img_path + os.sep +key
        gt_dict = get_gt_list(js_file)
        for key in gt_dict:
            #print key  ,gt_dict[key]
            points = gt_dict[key]
            img_url = img_path +os.sep+ key
#            print out_path
            write_img(img_url,points,out_path)



























