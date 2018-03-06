import cv2
import os
import  json
#js_path ='/mnt/hgfs/work/Phone_data/Phone_crop_face_rec/Anno_1227/11526.json'
#img_path = '/mnt/hgfs/work/Phone_data/Phone_crop_face_rec/1213_data/11526/'


#resize  800*800

def get_img(tmp,rec_points,new_points,out_img):
    xmin = int(rec_points[0])
    ymin = int(rec_points[1])
    xmax = int(rec_points[2])
    ymax = int(rec_points[3])
    src = cv2.imread(tmp)


    dst = src[ymin:ymax,xmin:xmax]
    p_xmin = int(new_points[0])
    p_ymin = int(new_points[1])
    p_xmax = int(new_points[2])
    p_ymax = int(new_points[3])

  #  cv2.rectangle(dst,(p_xmin,p_ymin),(p_xmax,p_ymax),(0,255,0),1)
  #  cv2.imshow('1',dst)
  #  c = chr(255&cv2.waitKey(0))
    #cv2.imwrite(out_path,dst)
  #  if c == 'q':
  #      return 1
  #  else :
    cv2.imwrite(out_img,dst)
    return 0

def out_new_json(new_points,js_path,context,count):
    pyctx = json.loads(context[count])
    pyctx['common_box'][0]['data'] = new_points
    pyctx['height']='800'
    pyctx['width']='800'
    new_js = open(js_path,'w')
    new_js = open(js_path,'w')
    context[count] = json.dumps(pyctx)+'\n'
    for line in context:
        new_js.write(line)
    new_js.close
    return


def cacul_new_points(rec_points,phone_points):
    r_xmin = int(rec_points[0])
    r_ymin = int(rec_points[1])
    r_xmax = int(rec_points[2])
    r_ymax = int(rec_points[3])

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
def show_rec(img_path,key,points):
    xmin = int(points[0])
    ymin = int(points[1])
    xmax = int(points[2])
    ymax = int(points[3])
    width = int(0.25*(xmax -xmin ))
    height = int(0.25*(ymax - ymin))
    xmin_new = xmin - width
    xmax_new = xmax + width
    ymin_new = ymin -height
    ymax_new = ymax +height

    rec_points = [xmin_new,ymin_new,xmax_new,ymax_new]

    return rec_points
    #src =cv2.imread(img_path+os.sep+key)
    #cv2.rectangle(src,(xmin_new,ymin_new),(xmax_new,ymax_new),(0,255,0),1)
    #cv2.imshow('1',src)
    #c = chr(255&cv2.waitKey(0))
    #if c == 'q':
    #    return rec_points,1
    #else :
    #    return rec_points,0


if __name__ == '__main__':
    js_dir = './Anno_1227'
    img_all = './1213_data'

    js_list = os.listdir(js_dir)
    for each  in js_list:
        js_path = js_dir +os.sep +each
        js_key = each[:5]
        img_dir = img_all +os.sep+js_key

        count = 0
        rec_points=[]
        new_points = []
        context = open(js_path,'r').readlines()

        while(int(count)<(int(len(context)))):
            ele = context[count]
            ele = json.loads(ele)
            if ele.has_key('head'):
                key = ele['image_key']
                head_points = ele["head"][0]['data']
                #rec_points,flag = show_rec(img_path,key,head_points)

                img_url= img_dir+os.sep+key
                print  img_url
                rec_points= show_rec(img_url,key,head_points)

                if ele.has_key('common_box'):
                    phone_points=ele['common_box'][0]['data']
                else:
                    phone_points = [0,0,0,0]
                new_points = cacul_new_points(rec_points,phone_points)

                #print  new_points
                img_out_path = './out_img'+os.sep+js_key
                if os.path.exists(img_out_path):
                    print 'folder has been existed'
                else:
                    os.makedirs(img_out_path)
                out_img = img_out_path +os.sep+key
                flag = get_img(img_url,rec_points,new_points,out_img)
                print flag
                js_path = './out_json'+os.sep+js_key+'.json'

                out_new_json(new_points,js_path,context,count)
                if  flag == 1:
                    break
                #print key ,head_points
            count =count+1
