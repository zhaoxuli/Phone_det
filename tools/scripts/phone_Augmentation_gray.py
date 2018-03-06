# -*- coding: utf-8 -*-
import os
import  cv2
import copy as cp
import numpy as np
import json
#from skimage  import exposure

def Contrast(img,k=0.7):
    dst = cp.deepcopy(img)
    Avg = dst.mean()
    dst = (img-Avg)*k + img
    print 'finish constrat'
    return dst

def EquHist(img):
    w,h,c = img.shape
    dst = cp.deepcopy(img)
    for i in range(c):
        img[:,:,i] = cv2.equalizeHist(img[:,:,i])
    return img

def  Illuminate(img):
    gamma1 = float(np.random.randint(1,19))/10
    illu_img= exposure.adjust_gamma(img_data, gamma1)
    return  illu_img

def local_high(img,alpha=1.2,b=10,k1=0.2,k2=0.3):
    #k1,k2 is the range of img_size  defalut 0.2-0.3
   # bias = np.random.randint(0,b)
   # value = img[w,h,c]*alpha +bias
    #mask = zeros(img.shape)
    img_w,img_h= img.shape
    dst = cp.deepcopy(img)
    x_loc = np.random.randint(1,img_w)
    y_loc = np.random.randint(1,img_h)
    width = np.random.randint(img_w*k1,img_w*k2)
    height  = np.random.randint(img_h*k1,img_h*k2)
    if x_loc < int(img_w/2):
        x_loc_end = x_loc + width
    else :
        x_loc_end = x_loc
        x_loc = x_loc - width
    if y_loc < int(img_h/2):
        y_loc_end = y_loc + height
    else :
        y_loc_end = y_loc
        y_loc = y_loc - height
   # print x_loc,x_loc_end,'       ',y_loc,y_loc_end
    for w in range(x_loc,x_loc_end):
        for h in range(y_loc,y_loc_end):
                if b >0:
                    bias = np.random.randint(0,b)
                else :
                    bias = np.random.randint(b,0)

                value = img[w,h]*alpha +bias
                if value > 255:
                    value = 255
                if value < 0:
                    value = 0
                dst[w,h] = value
    return dst

def get_new_points(old_points,center_points,angle,scale):
    angle = (angle*np.pi)/180

    old_left_x =  old_points[0]
    old_left_y =  old_points[1]
    old_right_x = old_points[2]
    old_right_y = old_points[3]

    center_x = center_points[0]
    center_y = center_points[1]

    loc_left_x  =  old_left_x - center_x
    loc_right_x = old_right_x - center_x
    loc_left_y  =  old_left_y - center_y
    loc_right_y = old_right_y - center_y

    left_new_x = int(loc_left_x*np.cos(angle)*scale + loc_left_y*np.sin(angle)*scale + center_x)
    left_new_y = int(-loc_left_x*np.sin(angle)*scale + loc_left_y*np.cos(angle)*scale + center_y)
    right_new_x = int(loc_right_x*np.cos(angle)*scale + loc_right_y*np.sin(angle)*scale + center_x)
    right_new_y = int(-loc_right_x*np.sin(angle)*scale + loc_right_y*np.cos(angle)*scale + center_y)

    return [left_new_x,left_new_y,right_new_x,right_new_y]

def noise(img,type_noise,kernel_size=(5,5),sigma=0,slat_ratio=0.008,papper_radtio=0.01):
    img_w,img_h = img.shape
    if type_noise == 'gaussian':
        img = cv2.GaussianBlur(img,kernel_size,sigma)

    if type_noise == 'salt':
        count_all = img.shape[0] * img.shape[1]
        salt_num = int(count_all*slat_ratio)
        for n in range(salt_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            img[m,n] = 255

    if type_noise == 'papper':
        count_all = img.shape[0] * img.shape[1]
        papper_num = int(count_all*papper_ratio)
        for n in range(papper_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            img[m,n] = 0


    if type_noise == 'all':
        img = cv2.GaussianBlur(img,kernel_size,sigma)
        count_all = img.shape[0] * img.shape[1]
        salt_num = int(count_all*slat_ratio)
        for n in range(salt_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            rand_key = np.random.randint(0,2)
            if rand_key ==1:
                 img[m,n] = 255
            else:
                 img[m,n] = 0
    return img


def rotate_det(img,center,angle,scale,old_points):

    img_w,img_h = img.shape
    print img.shape
    if center == 'normal':
        center_points = (img_w/2,img_h/2)

    M = cv2.getRotationMatrix2D(center_points ,angle, scale)
    if sum(old_points) != 0:
        new_points = get_new_points(old_points,center_points,angle,scale)
    else:
        new_points = [0,0,0,0]
    rotated = cv2.warpAffine(img,M,(img_h,img_w))
    return rotated,new_points


def save_js(ctx,new_js,new_points):
    file = open(new_js,'a')
    ctx = json.loads(ctx)
    ctx['common_box'][0]['data'] = new_points
    jsctx = json.dumps(ctx)+'\n'
    file.write(jsctx)
    file.close


def do_distrub(img_url,new_img_url,input_points):
    print img_url
    img = cv2.imread(img_url,0)
    Rotate_angle = np.random.randint(-10,10)
    #if abs(Rotate_angle) < 5:
    #    Rotate_angle = Rotate_angle +10
    #Rotate_scale = np.random.randint(5,11)*0.1
    Rotate_scale = 1
    cst_k = np.random.randint(3,9)*0.1

    type_key = np.random.randint(0,4)
    if type_key == 0:
        img = Contrast(img,cst_k)
        img,out_points = rotate_det(img,'normal',Rotate_angle,Rotate_scale,input_points)

    if type_key == 1:
        img = EquHist(img)
        img,out_points = rotate_det(img,'normal',Rotate_angle,Rotate_scale,input_points)

    if type_key == 2:
        img = Contrast(img,cst_k)

    if type_key == 3:
        img = EquHist(img)
    cv2.imwrite(str(new_img_url),img)

    if type_key < 2:
        return  out_points
    if type_key >=2:
        return  input_points

    print 'finish write'


def show(img_url,pot,old_url,old_pot):
    img=cv2.imread(img_url)
    old_img=cv2.imread(old_url)
    print pot
    cv2.rectangle(img,(int(pot[0]),int(pot[1])),(int(pot[2]),int(pot[3])),(0,0,255),1)
    cv2.rectangle(old_img,(int(old_pot[0]),int(old_pot[1])),(int(old_pot[2]),int(old_pot[3])),(255,0,0),1)
    cv2.imshow('new',img)
    cv2.imshow('old',old_img)
    if cv2.waitKey(0)& 0xFF == ord('q'):
        return  'stop'
    else:
        return 1

if __name__ == '__main__':
    out_js_path = '../work/Aug_gray_data/Anno'
    out_img_path = '../work/Aug_gray_data/Image'

    if os.path.exists(out_js_path) == False:
        os.makedirs(out_js_path)
    if os.path.exists(out_img_path) == False:
        os.makedirs(out_img_path)

    input_path = '../Crop_data/crop_Net_data/train_Net'
    js_path = input_path +os.sep+ 'Anno'
    img_path = input_path +os.sep+ 'Image'

    js_list = os.listdir(js_path)
    for ele in js_list:
        js_key = ele[:-5]
        ##mkdir out_key_img
        out_img_folder = out_img_path + os.sep+js_key+"_Aug"
        if os.path.exists(out_img_folder) == False:
            os.makedirs(out_img_folder)
        new_js = out_js_path +os.sep+js_key+'_Aug.json'

        #Processing  each img
        print js_key
        js_url = js_path+os.sep+ele
        #read_from json
        ctx = open(js_url,'r').readlines()
        num =0
        for line in ctx:
            if num == 3:
                txt_line = json.loads(line)
                img_key = txt_line['image_key']
                img_url = img_path + os.sep + js_key + os.sep +img_key
                #do_distrub
                new_img_url =  out_img_folder + os.sep + img_key
                try:
                    old_points = txt_line['common_box'][0]['data']
                except:
                    old_points = [0,0,0,0]
                try:
                    points = do_distrub(img_url,new_img_url,old_points)
                    save_js(line,new_js,points)
                    num = 0
                except:
                    num = 2
            #if show(new_img_url,points,img_url,old_points) =='stop':
               #quit()
            num = num +1




















