import os
import cv2
import json

def  get_face_from_txt(ctx,key):
    dirct = {}
    num = 0
    while(num <len(ctx)):
        if ctx[num].find('.png') != -1:
            #print ctx[num][:-1]
            dirct[ctx[num][:-1]] = ctx[num+1][:-1]
        num = num +1
    result = dirct[key]
    try:
        x1 = int(float(result.split(' ')[0]))
        y1 = int(float(result.split(' ')[1]))
        x2 = int(float(result.split(' ')[2]))
        y2 = int(float(result.split(' ')[3]))
        face_point = [x1,y1,x2,y2]
    except:
        face_point = [0,0,0,0]

    xmin = int(face_point[0])
    ymin = int(face_point[1])
    xmax = int(face_point[2])
    ymax = int(face_point[3])
    width = int(0.5*(xmax -xmin ))
    height = int(0.1*(ymax - ymin))
    xmin_new = xmin - width
    xmax_new = xmax + width
    ymin_new = ymin -height
    ymax_new = ymax +height

    rec_points = [xmin_new,ymin_new,xmax_new,ymax_new]
    #return  face_point
    return rec_points

def cacul_new_points(rec_points,phone_points):
    r_xmin = int(rec_points[0])
    r_ymin = int(rec_points[1])
    r_xmax = int(rec_points[2])
    r_ymax = int(rec_points[3])
    #r_width = int(r_xmax - r_xmin )
    #r_height = int(r_ymax - r_ymin)
    #x_scale = float(r_width)
    #y_scale = float(r_height)
    #print r_width,r_height

    p_xmin = int(phone_points[0])
    p_ymin = int(phone_points[1])
    p_xmax = int(phone_points[2])
    p_ymax = int(phone_points[3])

    if p_xmin < r_xmin:
        p_xmin = r_xmin

    if p_xmin > r_xmax:
        p_xmin = r_xmin
        p_xmax = r_xmax

    if p_ymin < r_ymin:
        p_ymin = r_ymin

    if p_ymin > r_ymax:
        p_ymin = r_ymin
        p_ymax = r_ymin

    if p_xmax > r_xmax:
        p_xmax = r_xmax

    if p_xmax <r_xmin:
        p_xmax = r_xmin
        p_xmin = r_xmin

    if p_ymax <r_ymin:
        p_ymax = r_ymin
        p_ymin = r_ymin

    if p_ymax >r_ymax:
        p_ymax = r_ymax

    new_xmin = int((p_xmin - r_xmin))
    new_xmax = int((p_xmax  - r_xmin))
    new_ymin = int((p_ymin - r_ymin))
    new_ymax = int((p_ymax - r_ymin))

    new_points = new_xmin,new_ymin,new_xmax,new_ymax

    return  new_points


def show(img_url,points):
    xmin = int(points[0])
    ymin = int(points[1])
    xmax = int(points[2])
    ymax = int(points[3])

    src =cv2.imread(img_url)
    cv2.rectangle(src,(xmin,ymin),(xmax,ymax),(0,255,0),1)
    cv2.imshow('1',src)
    c = chr(255&cv2.waitKey(0))
    if c == 'q':
        return 1
    else:
        return  0

def get_img(tmp,rec_points,new_points,out_img):
    xmin = int(rec_points[0])
    ymin = int(rec_points[1])
    xmax = int(rec_points[2])
    ymax = int(rec_points[3])
    src = cv2.imread(tmp)


    dst = src[ymin:ymax,xmin:xmax]
    #sub = cv2.resize(dst,(800,800))
    p_xmin = int(new_points[0])
    p_ymin = int(new_points[1])
    p_xmax = int(new_points[2])
    p_ymax = int(new_points[3])

#    cv2.rectangle(dst,(p_xmin,p_ymin),(p_xmax,p_ymax),(0,255,0),1)
#    cv2.imshow('1',dst)
#    c = chr(255&cv2.waitKey(0))
#    if c == 'q':
#        return 1
#    else :
    cv2.imwrite(out_img,dst)
    return 0

def out_new_json(new_points,js_path,context,count,img_w_new,img_h_new):
    pyctx = json.loads(context[count])
    pyctx['height']=  img_h_new
    pyctx['width']=img_w_new
    try:
        pyctx['common_box'][0]['data'] = new_points
    except:
        print 'no phone'
    new_js = open(js_path,'w')
    new_js = open(js_path,'w')
    context[count] = json.dumps(pyctx)+'\n'
    for line in context:
        new_js.write(line)
    new_js.close
    return


if __name__ == '__main__':
    ctx= open('./Image.txt','r').readlines()
    #rec_point =[]
    #img_url = './Image/test_data/468.png'
    #img_key = 'test_data/468.png'
    #rec_point = get_face_from_txt(ctx,img_key)
    #show(img_url,rec_point)
    #print rec_point
    js_path = './Anno_1227'
    img_all  = './1213_data'
    files = os.listdir(js_path)
    for file in  files:
        if file.find('.json')!= -1:
            num = 0
            js_ctx = open(js_path+os.sep+file).readlines()
            while(int(num)<len(js_ctx)):
                ele  = js_ctx[num]
                ele  = json.loads(ele)
                key = ele['image_key']
                img_w = int(ele['width'])
                img_h = int(ele['height'])

                js_key = file.split('.')[0]
                img_url = img_all +os.sep+js_key+os.sep+key
                img_key = file.split('.')[0]+os.sep+key
                try:
                    rec_points =get_face_from_txt(ctx,img_key)


                    if sum(rec_points)!=0:
                        if ele.has_key('common_box'):
                            phone_points=ele['common_box'][0]['data']
                        else:
                            phone_points = [0,0,0,0]

                        new_points = cacul_new_points(rec_points,phone_points)
                        print new_points,img_key

                    img_out_path = './out_img'+os.sep+js_key
                    if os.path.exists(img_out_path):
                        print 'folder has been existed'
                    else:
                        os.makedirs(img_out_path)
                    #flag = show(img_url,rec_points)
                    out_img = img_out_path +os.sep+key
                    flag = get_img(img_url,rec_points,new_points,out_img)
                    #flag = show(out_img,new_points)
                    print flag
                    js_path = './out_json'+os.sep+js_key+'.json'
                    img_w_new = rec_points[2]- rec_points[1]
                    img_h_new = rec_points[3] - rec_points[0]

                    out_new_json(new_points,js_path,js_ctx,num,img_w_new,img_h_new)
                    if  flag == 1:
                        break
                except:
                    print 'false'
                num = num +1
























