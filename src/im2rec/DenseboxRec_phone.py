# -*- coding:UTF-8 -*-
import os,sys
import json
import cv2
import numpy as np
import logging
#
# utils and tools
#

logging.basicConfig(level=logging.FATAL,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')

#判断该条记录Head数据的Ignore属性级别
def getIgnoreLevel(attrs):
    if not attrs.has_key('ignore'):
        logging.debug('the obj ignore has no ignore attrs.')
        return 0
    elif attrs['ignore'] == 'no':
        logging.debug('the obj ignore is no.')
        return 0
    elif attrs['ignore'] == 'yes':
        logging.debug('the obj ignore is yes.')
        return 1
    else:
        raise ValueError("Unexpected ingore type: {}".format(attrs['ignore']))
        return 1

#判断该条记录Head是否被遮挡
def getOcclusionLevel(attrs):
    if not attrs.has_key('occlusion'):
        logging.debug('the obj has no occlusion')
        return 0
    elif attrs['occlusion'] == 'full_visible':
        logging.debug('the obj occlusion  = full_visible')
        return 0
    elif attrs['occlusion'] == 'occluded':
        logging.debug('the obj occlusion = occluded')
        return 1
    elif attrs['occlusion'] == 'heavily_occluded':
        logging.debug('the obj occlusion = heavily_occluded')
        return 2
    elif attrs['occlusion'] == 'invisible':
        logging.debug('the obj occlusion = invisible')
        return 3
    else:
        raise ValueError("Unexpected occlusion type: {}".format(attrs['occlusion']))
        logging.debug('the obj cocclusion error')
        return 3

# get the json file
def getFileListBySuffix(path, suffix):
    name_list = []
    #suffix = suffix.lower()
    fnames = os.listdir(path)
    for fname in fnames:
        fname_suffix = fname.split('.')[-1].lower()
        if fname_suffix in suffix:
            name_list.append(fname)
    path_list = map(lambda x: os.path.join(path, x), name_list)
    return path_list


# create a direction
def newObj():
    obj = {}
    obj['img_w'] = 1280
    obj['img_h'] = 720
    obj['img_c'] = 1
    obj['img_url'] = ''
    obj['instances'] = []
    obj['ignore_regions'] = []
    return obj

# create a direction
def newInstance():
    instance = {}
    instance['class_id'] = []
    instance['attribute'] = []
    instance['ignore'] = []
    instance['points_data'] = []
    return instance

def newIgnoreRegion():
    ignore_region = {}
    ignore_region['class_id'] = []
    ignore_region['right_bottom'] = []
    ignore_region['left_top'] = []
    return ignore_region

def newClassInfo():
    class_info = {}
    class_info['class_name'] = ''
    class_info['bbox_border_id'] = []
    class_info['point_num'] = 0
    class_info['attribute_num'] = 0
    class_info['attribute_names'] = []
    return class_info




class alphaV2RecConvertor:
    def __init__(self, check_image=False):
        self.densebox_json = None
        self.check_image = check_image

    def __resetDenseboxJson__(self):
        bg_info = newClassInfo()
        bg_info['class_name'] = 'background'
        fg_info = newClassInfo()
        fg_info['class_name'] = object_type
        fg_info['bbox_border_id'].extend([0, 1, 2, 3])
        fg_info['point_num'] = 5
        self.densebox_json = dict()
        self.densebox_json['image_recs'] = []
        self.densebox_json['classes_info'] = []
        self.densebox_json['classes_info'].append(bg_info)
        self.densebox_json['classes_info'].append(fg_info)

    def __cvtJson2DenseboxJson__(self, data_list, object_type):
        self.__resetDenseboxJson__()

        for data_json in data_list:
            #path_prefix = data_json.split('/')[-1].split('.')[0]
            #print path_prefix
            if not os.path.exists(data_json):
                continue
            if data_json[-4:] =='json':
                print 'a',data_json
                path_prefix = data_json.split('/')[-1].split('.')[0]
                lines = open(data_json, 'r').readlines()
                count = 0
                key =0
                for line in lines:
                    if (line[0]!= '#'):
                        json_dict = json.loads(line)
                        img_w = json_dict['width']
                        img_h = json_dict['height']
                        img_c = 1
                        img_url = os.path.join(path_prefix, str(json_dict['image_key']))

                        if self.check_image:
                            img_path = os.path.join(data_json.replace('.json', ''), str(json_dict['image_key']))
                            if count == 1000 :
                                key =key+1
                                print  str(key)+'000        img_json  done'
                                count = 0
                            count =count+1
                            #print img_path
                            #print 'a'

#                            if img is None:
#                                continue
                            if json_dict.has_key(object_type):

                                objs = json_dict[object_type]

                                convert_obj = newObj()
                                convert_obj['img_w'] = img_w
                                convert_obj['img_h'] = img_h
                                convert_obj['img_c'] = img_c
                                convert_obj['img_url'] = img_url

                                logging.debug('the objs length is %d',objs.__len__())
                                logging.debug(objs)

                                rect = map(float, objs[0]['data'])
                                left = rect[0]
                                top = rect[1]
                                right = rect[2]
                                bottom = rect[3]
#                                img = cv2.imread(img_path)
#                                cv2.rectangle(img,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),(255,0,0),2)
#                                cv2.imshow("test", img)
#                                cv2.waitKey(0)

                                leftTop = [int(rect[0]),int(rect[1])]
                                rightTop = [int(rect[2]),int(rect[1])]
                                rightBottom = [int(rect[2]),int(rect[3])]
                                leftBottom = [int(rect[0]),int(rect[3])]
                                instance = newInstance()
                                instance['class_id'].append(1) # boosting just has only one class
                                instance['ignore'].append(0)
                                center = [int(0.5*(left+right)),int(0.5*(top+bottom))]
                                instance['points_data'].extend([leftTop, rightTop, rightBottom, leftBottom,center])

                                convert_obj['instances'].append(instance)

                                self.densebox_json['image_recs'].append(convert_obj)



    def __writeDenseboxJson2file__(self, path):
        f = open(path, 'w')
        f.write(json.dumps(self.densebox_json))
        f.close()

    def __cvtDenseboxFormat2Rec__(self, densebox_json, img_dir, output_rec, new_json, quality=100):
        #img_dir = img_dir  + "2410" + os.sep
        print img_dir
        print densebox_json
        cmd = './densebox_im2rec.bin {} {} {} {} preprocess_thread={} encoding=.png'.format(densebox_json, img_dir, output_rec, new_json,  8)
        print cmd
        f = os.popen(cmd)
        #os.system(cmd)
        print f.read()

    def __generateAllDenseboxJson__(self, data_path,json_path, object_type):
        if not os.path.exists(data_path):
            print '{} not exists!'.format(data_path)
            return
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        #data_json_list = getFileListBySuffix(data_path, ['json'])
        data_json_list = getFileListBySuffix(json_path, ['json'])
        # load all jsons and write to dict
        self.__cvtJson2DenseboxJson__(data_json_list, object_type)
        # write densebox dict to file
        densebox_json_path = os.path.join(data_path, 'all.densebox_json')
        self.__writeDenseboxJson2file__(densebox_json_path)




    def run(self, train_data_path, output_path, object_type):
        if not train_data_path[-1] == '/':
            train_data_path += '/'

        if True:
            self.__generateAllDenseboxJson__(train_data_path,json_path, object_type)
            # use densebox_im2rec.bin create train.json and train.rec
            train_densebox_json_path = os.path.join(train_data_path, 'all.densebox_json')
            train_output_rec = os.path.join(output_path, 'train.rec')
            train_new_json = os.path.join(output_path, 'train.json')
            self.__cvtDenseboxFormat2Rec__(train_densebox_json_path, train_data_path, train_output_rec, train_new_json)
#        if True:
#            self.__generateAllDenseboxJson__(val_data_path, object_type)
#           # use densebox_im2rec.bin create test.json and test.rec
#            val_densebox_json_path = os.path.join(val_data_path, 'all.densebox_json')
#            val_output_rec = os.path.join(output_path, 'val.rec')
#            val_new_json = os.path.join(output_path, 'val.json')
#            self.__cvtDenseboxFormat2Rec__(val_densebox_json_path, val_data_path, val_output_rec, val_new_json)

if __name__ == "__main__":
    data_path = \
    '/home/users/dawei.yang/phone_alpha/data/crop_data_new/train_data/Image/'
    json_path = \
    '/home/users/dawei.yang/phone_alpha/data/crop_data_new/train_data/Anno_Aug/'
    output_path = \
    '/home/users/dawei.yang/phone_alpha/data/crop_data_new/train_rec_data/0305_Aug_rec/'
    object_type = 'common_box'
    convertor = alphaV2RecConvertor(True)
    convertor.run(data_path, output_path, object_type)
