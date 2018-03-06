import cv2
import os
import json
import copy

js_path = '/mnt/hgfs/work/Phone_data/Net_data/Anno_new/11444.json'

def read_info(js_path ):
    tag = 'norm'
    num = 0
    tmp_path,tmp = os.path.split(js_path)
    data_path = os.path.dirname(tmp_path)
    print data_path
    if js_path[-4:] == 'json':
        name = js_path.split(os.sep)[-1][0:-5]
    else:
        print js_path  ,'is  uncertain'
        return
    img_path = data_path +os.sep +name
    context = open(js_path,'r').readlines()
    context_var = copy.deepcopy(context)
    count = 0
    print '[images num:]',len(context)
    while(count<= len(context)):
        ele = context[count]
        ele = json.loads(ele)
        if ele.has_key('common_box'):
            key = ele["image_key"]
            points = ele["common_box"][0]['data']
            xmin = int(points[0])
            ymin = int(points[1])
            xmax = int(points[2])
            ymax = int(points[3])
            img_url = img_path +os.sep+key
            count,tag,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
        if tag == 'del':
            count_new = count -num-1
            del context_var[count_new]
            num = num +1
            print 'len context_var',len(context_var)
            tag = 'norm'
            file = open(js_path,'w')
            for line in context_var:
                file.write(line)
            file.close()

        if tag == 'save':
            count_new = count -num -1
            print 'points_new:' ,points_new
            print 'points:',[xmin,ymin,xmax,ymax]
            if points_new != [xmin,ymin,xmax,ymax]:
                print 'saving the json...'
                pyctx_line = json.loads(context_var[count_new])
                pyctx_line["common_box"][0]['data'] = points_new
                print pyctx_line
                new_js = open(js_path,'w')
                context_var[count_new] = json.dumps(pyctx_line)+'\n'
                for line in context_var:
                    new_js.write(line)
                new_js.close
            else :
                print 'It is the same positon'
        print '__________finish one  operation__________'

def  show_rec(img_url,xmin,ymin,xmax,ymax,count,tag):
    print '[opreation:]',tag
    print '[init]',img_url,'           ','context_conut:',count
    points_new = [xmin,ymin,xmax,ymax]
    num = 3
    img =  cv2.imread(img_url)
    cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(0,255,0),1)
    cv2.imshow('1',img)
    c = chr(255&cv2.waitKey(0))
    if c == 'q':
        tag = 'norm'
        count = 99999
        return count,tag,points_new
    elif c == 'u':
        return count-1,tag,points_new
    elif c == 'l':
        if tag != 'bottom':
            xmin =xmin +3
            print img_url ,'Top  point   do      xmin+',num
            count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
            return count,tag,points_new
        elif tag == 'bottom':
            xmax =xmax +num
            print img_url ,'Bottom  point   do      xmax+',num
            count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
            return count,tag,points_new
    elif c == 'j':
        if tag != 'bottom':
             ymin =ymin +num
             print img_url ,'Top  point   do       ymin+',num
             count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
             return count,tag,points_new
        elif tag == 'bottom':
             ymax =ymax +num
             print img_url ,'Bottom  point   do        ymax+',num
             count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
             return count,tag,points_new
    elif c == 'h':
        if tag != 'bottom':
             xmin =xmin - num
             print img_url ,'Top  point   do        xmin-',num
             count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
             return count,tag,points_new
        elif tag == 'bottom':
             xmax =xmax -num
             print img_url ,' Bottom  point   do        xmax-',num
             count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
             return count,tag,points_new

    elif c == 'k':
        if tag != 'bottom':
             ymin =ymin -num
             print img_url ,' Top  point   do        ymin-',num
             count,tag ,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
             return count,tag,points_new
        elif tag == 'bottom':
            ymax =ymax -num
            print img_url ,' Bottom  point   do        ymax-',num
            count,tag,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
            return count,tag,points_new
    elif c == 'c':
        print tag
        if tag != 'bottom':
            print 'now  changing the <<bottom positon>>'
            tag = 'bottom'
            count,tag,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
            return count,tag,points_new
        if tag == 'bottom':
            print  'now changing the <<top  positon>>'
            tag = 'top'
            count,tag,points_new = show_rec(img_url,xmin,ymin,xmax,ymax,count,tag)
            return  count,tag,points_new
    elif c =='d':
        key =  img_url.split(os.sep)[-3]
        print key
        Trash_path =  img_url.split(key)[0] + os.sep +'Trash'+os.sep+ img_url.split(key)[1]
        path ,file = os.path.split(Trash_path)
        print '[mv image to:]',path
        if os.path.exists(path):
             a =0
        else :
             os.makedirs(path)
        cmd = 'mv '+ img_url + ' '+ path
        print cmd
        os.system(cmd)
        tag = 'del'
        return count+1 ,tag,points_new
    elif c == 's':
        tag = 'save'
        return  count+1,tag,points_new
    else:
        tag ='norm'
        return count+1,tag,points_new

read_info(js_path)

