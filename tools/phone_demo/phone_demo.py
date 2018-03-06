# -*- coding: utf-8 -*-
import cv2
import logging
import numpy as np
import sys
import os
from time import clock

def get_face_loc(img):
    loc = []
    cmd='./alphaDet_prediect/AlphaDet_test  '+img
    #print cmd
    output  = os.popen(cmd)
    messege = output.readlines()
    info = messege[4]
    if  info.split()[0] !='left':
        print messege
        return None,None
    else:
        loc.append(float(info.split()[1]))
        loc.append(float(info.split()[3]))
        loc.append(float(info.split()[5]))
        loc.append(float(info.split()[7]))
        conf = info.split()[9]
        return loc,conf

def get_roi(loc,img):
    src = cv2.imread(img,0)
    h,w = src.shape
    if src is None:
        print 'False  image'
        roi_ary = [0,0,0,0]
    else :
        xmin = int(loc[0])
        ymin = int(loc[1])
        xmax = int(loc[2])
        ymax = int(loc[3])
        width = int(0.5*(xmax -xmin ))
        height = int(0.3*(ymax - ymin))
        xmin_new = xmin - width
        xmax_new = xmax + width
        ymin_new = ymin -height
        ymax_new = ymax +height
        if xmin_new < 0:
            xmin_new = 0
        if ymin_new < 0:
            ymin_new = 0
        if xmax_new > w:
            xmax_new = w
        if ymax_new > h:
            ymax_new =h
        roi_ary = [xmin_new , ymin_new, xmax_new ,ymax_new]
        #cv2.rectangle(src,(int(loc[0]),int(loc[1])),(int(loc[2]),int(loc[3])),(255,0,0),2)
        #cv2.rectangle(img,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),(255,0,0),2)
        pad_face = src[roi_ary[1]:roi_ary[3],roi_ary[0]:roi_ary[2]]
        cv2.imwrite('./predict.png',pad_face)
    return roi_ary

def get_phone_loc(roi_ary,thresh=5):
    loc = []
    cmd ='/home/zhaoxu/Phone_demo/alphaDet_prediect/detect \
        /home/zhaoxu/Phone_demo/alphaDet_prediect/settings.ini.phone.example \
        /home/zhaoxu/Phone_demo/alphaDet_prediect/img.txt     /home/../'
    output = os.popen(cmd)
    msg = output.readlines()[0]
    #print msg[:-1]
    if  msg[-4:-1] != 'png':
        data = msg.split('png')[-1][:-1]
        out_list = data.split()
        score_num = 4
        max_score = 0
        while(score_num < len(out_list)):
            if max_score < float(out_list[score_num]):
                max_score = float(out_list[score_num])
                max_num = score_num
            score_num = score_num +5
        #print max_score, max_num
        if int(max_score) >= int(thresh):
            loc.append(float(roi_ary[0]) + float(out_list[max_num-4]))
            loc.append(float(roi_ary[1]) + float(out_list[max_num-3]))
            loc.append(float(roi_ary[0]) + float(out_list[max_num-2]))
            loc.append(float(roi_ary[1]) + float(out_list[max_num-1]))
            loc.append(float(out_list[max_num]))
        else:
            loc = [0,0,0,0,0]
            print 'phone_score: ', max_score
        print loc[-1]
    else:
        loc =[0,0,0,0,0]
    return loc

def Read_video(video_path,thresh):
    videoCap = cv2.VideoCapture(video_path)
    frame_count = int(videoCap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    print frame_count
    count = 0
    while(int(count)<frame_count):
        count  = count + 3
        videoCap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,count)
        videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
        videoCap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
        ret,frame = videoCap.read()
        src = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imwrite('./temp.jpg',src)
        img_path = './temp.jpg'
        loc,conf = get_face_loc(img_path)
        if  loc is None:
            print 'non face'
            cv2.putText(frame,'NONE_FACE',(10,30),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,255,255))
        else:
            roi_ary = get_roi(loc,img_path)
            cv2.rectangle(frame,(int(roi_ary[0]),int(roi_ary[1])),(int(roi_ary[2]),int(roi_ary[3])),(0,0,255),1)
        #do predict
            try:
                loc = get_phone_loc(roi_ary,thresh)
                if sum(loc) !=0:
                    cv2.rectangle(frame,(int(loc[0]),int(loc[1])),(int(loc[2]),int(loc[3])),(0,255,0),1)
                    cv2.putText(frame,str(loc[-1]),(int(loc[0]),int(loc[1])),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,0,0))
            except:
                print 'predict_erro'
        cv2.imshow('main',frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            count = frame_count
    videoCap.release()
    cv2.destroyWindows()


def Video_cap(thresh):
    #fourcc = cv2.cv.CV_FOURCC(*'XVID')
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
    #out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))#保存视频
    while True:
        #print 'loop'
        ret,frame = cap.read()
        #print ret
        #print frame.shape
        src = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imwrite('./temp.jpg',src)
        img_path = './temp.jpg'
        loc,conf = get_face_loc(img_path)
        if  loc is None:
            print 'non face'
            cv2.putText(frame,'NONE_FACE',(10,30),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,255,255))
        else:
            roi_ary = get_roi(loc,img_path)
            cv2.rectangle(frame,(int(roi_ary[0]),int(roi_ary[1])),(int(roi_ary[2]),int(roi_ary[3])),(0,0,255),1)
        #do predict
            try:
                loc = get_phone_loc(roi_ary,thresh)
                if sum(loc) !=0:
                    cv2.rectangle(frame,(int(loc[0]),int(loc[1])),(int(loc[2]),int(loc[3])),(0,255,0),1)
                    cv2.putText(frame,str(loc[-1]),(int(loc[0]),int(loc[1])),cv2.FONT_HERSHEY_TRIPLEX,0.6,(255,0,0))
            except:
                print 'predict_erro'
        cv2.imshow('main',frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
           break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #input_type = sys.argv[1]
    thresh =  30 #0227
    #thresh = 15 #1228
    #thresh =10
    input_type = 'capture'
    if  input_type != 'capture':
        video_path = '/mnt/hgfs/work/phone_test/phone_test.mp4'
        Read_video(video_path,thresh)
    else:
        print 1
        Video_cap(thresh)













