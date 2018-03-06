import re
import os
import cv2
import json

def get_det(txt_path):
    det_list = []
    with open(txt_path,'r') as  ctx:
        for ele in ctx:
            ele = ele[:-1]
            if ('.png')  in ele:
                if ']['  in ele:
                     det_list.append(ele.split('['))
                else:
                    #print ele
                    try:
                        det_list.append(ele.split('['))
                    except:
                        det_list.append(ele)

    return det_list



def write_img(img_url,str_points,out_path):
    img_key = img_url.split(os.sep)[-1]
    points = []
    #points.replace(' ','')
    if str_points != 'false':
        test = str_points.split(' ')
        for ele in test:
            try:
                a = float(ele)
                points.append(a)
            except:
                a = 0
        lx = int(points[0])
        ly = int(points[1])
        rx = int(points[2])
        ry = int(points[3])
    else:
        lx,ly,rx,ry = [0,0,0,0]
    img = cv2.imread(img_url)
    print img_url
    cv2.rectangle(img,(int(lx),int(ly)),(int(rx),int(ry)),(0,255,0),1)
    cv2.imwrite(out_path +os.sep+'rec'+img_key,img)
    return

def get_fp_img(img_url,dt_points,out_path):
    #print  'saving'
    if dt_points:
        pass
    else:
        dt_points = [0,0,0,0]
    try:
        img_key = img_url.split(os.sep)[-1]
        img = cv2.imread(img_url)
        lx = int(dt_points[0])
        ly = int(dt_points[1])
        rx = int(dt_points[2])
        ry = int(dt_points[3])
        cv2.rectangle(img,(int(lx),int(ly)),(int(rx),int(ry)),(0,255,0),1)
        print out_path
        cv2.imwrite(out_path,img)
    except:
        print "false image:  ",img_url
    return



def get_gt_list(prefix_path):
    gt_json = os.listdir(prefix_path)
    gt_dict = {}
    for  ele in gt_json:
        if ele[-4:] == 'json':
            pre_img = ele[:-5]
            js_path = prefix_path +os.sep+ ele
            js_lines = open(js_path,'r').readlines()
            for ele in js_lines:
                ele  = json.loads(ele)
                #print ele
                img_key =pre_img+os.sep+ ele["image_key"]
                try:
                    points = ele["common_box"][0]['data']
                except:
                    points = [0,0,0,0]
                #image_key  heigt   wideth  type  x1,y1,x2,y2  left top right  bottom
                gt_dict[img_key] = points

    return gt_dict

def cacul(gt_dict,img_key,str_points):
    gt_points = gt_dict[img_key]
    gt_lx  =int(gt_points[0])
    gt_ly  =int(gt_points[1])
    gt_rx  =int(gt_points[2])
    gt_ry  =int(gt_points[3])
    #print 'gt_points',gt_points

    points = []
    #points.replace(' ','')
    if str_points != 'false':
        test = str_points.split(' ')
        for ele in test:
            try:
                a = float(ele)
                points.append(a)
            except:
                a = 0
        dt_lx = int(points[0])
        dt_ly = int(points[1])
        dt_rx = int(points[2])
        dt_ry = int(points[3])
    else:
        dt_lx,dt_ly,dt_rx,dt_ry = [0,0,0,0]

   # print 'dt_points',dt_lx,dt_ly,dt_rx,dt_ry

    W = min(dt_rx,gt_rx) -max(dt_lx,gt_lx)+1
    H = min(dt_ry,gt_ry) -max(dt_ly,gt_ly)+1

  #  print 'w,h:',W,H
    if W<=0 or H<=0:
        IOU = 0
    else:
        gt_area = (gt_rx - gt_lx + 1)*(gt_ry - gt_ly + 1)
        dt_area = (dt_rx - dt_lx + 1)*(dt_ry - dt_ly + 1)
        cross = W*H
 #       print 'cross,gt_area,dt_area',cross,gt_area,dt_area
        IOU = float(cross/float((gt_area + dt_area -cross)))

#    print IOU
    if 0< IOU < 0.4:
        print 'IOU:',IOU
        return img_key,points
    else:
        return 0,0

if __name__ == '__main__':
    #txt_path = '../crop_result/crop_0224_heigh_result.txt'
    txt_path = '../crop_result_All/crop_0229_All_result.txt'
    test_path = '/mnt/hgfs/work/Phone_data/Crop_data/crop_test/'
    out_path = '/mnt/hgfs/work/Phone_data/Crop_data/out_fp_0229'
    #js_path = '../crop_result/test_data.json'
    js_path = '../crop_result_All/'
    det_list = []
    det_list = get_det(txt_path)
    gt_dict = {}
    gt_dict  = get_gt_list(js_path)
    for ele in det_list:
        img_key = ele[0][:-1]
        try:
            points = ele[1]
        except:
            points = 'false'
        #print img_key
        fp_key,fp_points = cacul(gt_dict,img_key,points)
        if  fp_key!=0:
            print fp_key,fp_points
            folder_key = fp_key.split(os.sep)[0]
            fp_img_key = fp_key.split(os.sep)[1]
            out_folder = out_path +os.sep + folder_key
            if os.path.exists(out_folder) == False:
                os.makedirs(out_folder)
            out_img = out_folder+ os.sep +fp_img_key
            #print out_img
            #print img_key,points
            img_url = test_path + os.sep +fp_key
            #print img_url
            get_fp_img(img_url,fp_points,out_img)
        #write_img (img_url,points,out_path)
