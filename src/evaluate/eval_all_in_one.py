import matplotlib
matplotlib.use('Agg')
import os, sys
import cv, cv2
#import glob
import numpy as np
#from time import time
sys.path.append('../')
sys.path.append('./')
#from util import GetPerturbedSamples
import pylab
#from smp import *
#from scipy.io import savemat, loadmat
import argparse

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('anno_file', help='Annotation file.')
  parser.add_argument('det_file', help='Detection results file.')
  parser.add_argument('--scale_gt', help='Groundtruth boundingbox scaling factor', default=0, type=float)
  parser.add_argument('--scale_det', help='Detection boundingbox scaling factor', default=0, type=float)
  parser.add_argument('--square_gt', help='Whether to make groundtruth box square.', default=False, type=bool)
  parser.add_argument('--with_cnn_results', help='CNN detection results in det_file.', default=False, type=bool)
  parser.add_argument('--graph_type', help='Type of the graph:pr/fppi/fp', default='pr', type=str)
  parser.add_argument('--ivu_thres', help='Intersection v.s. union ratio', default='0.5', type=float)
  parser.add_argument('--min_size', help='Minium detect window size', default=0, type=int)
  parser.add_argument('--max_size', help='Maxium detect window size', default=1024, type=int)
  args = parser.parse_args()
  return args

def calfp(fp, rec):
  ap = 0
  for i in xrange(len(fp)-1):
    ap += (fp[i+1]-fp[i])*rec[i]
    if fp[i+1] > 100:
      break
  return ap/100

def calap(recall, prec):
  mrec = [0] + list(recall.flatten()) + [1]
  mpre = [0] + list(prec.flatten()) + [0]
  for i in range(len(mpre)-2, 0, -1):
    mpre[i] = max(mpre[i], mpre[i+1])
  ap = 0
  for i in xrange(len(mpre)-1):
    if mpre[i+1] > 0.8: #0.9:
      ap += (mrec[i+1] - mrec[i])*mpre[i+1]
  return ap, mrec[1:-1], mpre[1:-1]

#---------------------------------------------------------------------------------------------------------
# This function modifed by zhangyi to evaluate the data lists which have a lot of "ignore" attributes.
#---------------------------------------------------------------------------------------------------------

#set all gts in ignore gt to "ignores"
def filter_gt_in_ignores(gt):
   for i in xrange(len(gt)):
     if not gt[i,4] == 2: continue
     for j in xrange(len(gt)):
       if i==j: continue
       gt_w = gt[j,2] - gt[j,0]
       gt_h = gt[j,3] - gt[j,1]
       if gt[j, 4] == 0: # normal rect
         bi = [max(gt[i,0], gt[j,0]), max(gt[i,1], gt[j,1]), min(gt[i,2], gt[j,2]), min(gt[i,3], gt[j,3])] #inner overlap bbox
         iw = bi[2] - bi[0] + 1
         ih = bi[3] - bi[1] + 1
         iv = iw * ih / (gt_w * gt_h + 1E-10)
         if iw > 0 and ih > 0 and iv > 0.8:
           gt[j,4] = 2
   return gt

#def evaluation(det_boxes, gt_boxes, ivu_thres):
def evaluation(det_boxes, gt_boxes):
  num_gt = 0
  tp_all = []
  fp_all = []
  tp_boxes_all = []
  all_conf = []
  num_image = len(det_boxes)
  diff_x = []
  for i, gt in enumerate(gt_boxes):
    #print gt
    #print gt_boxes[gt]
    num_gt += gt_boxes[gt].shape[0] #- gt_boxes[gt][:,4].sum()
    num_gt_i = gt_boxes[gt].shape[0]
    #print gt,det_boxes[gt]
    idx = np.argsort(-det_boxes[gt][:,-1])
    det_b = det_boxes[gt][idx]
    num_obj = len(det_boxes[gt])
    conf = det_boxes[gt][idx,-1].reshape(-1, 1)
    gt_detected = np.zeros((num_gt_i, 1))
    tp = np.zeros((num_obj, 1))
    fp = np.zeros((num_obj, 1))
    tp_boxes = np.zeros((num_obj, 1))
    for j in xrange(num_obj):
      b = det_b[j]
      kmax = -1
      ov_max = -1000000
      for k in xrange(gt_boxes[gt].shape[0]):
        if gt_detected[k] == 1:
          continue
        bbgt = gt_boxes[gt][k]
        bi = [max(b[0], bbgt[0]), max(b[1], bbgt[1]), min(b[2], bbgt[2]), min(b[3], bbgt[3])]
        iw = bi[2] - bi[0] + 1
        ih = bi[3] - bi[1] + 1
        if iw > 0 and ih > 0:
          ua = (b[2] - b[0] + 1) * (b[3] - b[1] + 1) + \
               (bbgt[2] - bbgt[0] + 1) * (bbgt[3] - bbgt[1] + 1) - \
               iw * ih
          ov = iw * ih / ua
          if ov > ov_max and ov > 0.5:
            diff_x.append((bbgt[2] + bbgt[1] - b[2] - b[1])/2.0)
            ov_max = ov
            kmax = k
          if ov > 0.5:
            tp_boxes[j] = 1
      if kmax >= 0:
        tp[j] = 1
#        if gt_boxes[gt][kmax, 4] < 1:
#          tp[j] = 1
        gt_detected[kmax] = 1
      else:
        fp[j] = 1;

    tp_all.append(tp)
    fp_all.append(fp)
    tp_boxes_all.append(zip(det_b, tp_boxes))
    all_conf.append(conf)
  diff_x = np.hstack(diff_x)
  #print diff_x.mean(), diff_x.std()
  tp = np.vstack(tp_all)
  fp = np.vstack(fp_all)
  num_pos = tp.sum()
  conf = np.vstack(all_conf)
  idx = np.argsort(-conf, axis=0)
  conf = conf[idx]
  tp = np.require(tp[idx], dtype=np.float)
  fp = fp[idx]
  tp = np.cumsum(tp)
  fp = np.cumsum(fp)
  recall = tp/(num_gt)
  prec = tp/(tp + fp + 1E-10)
  fppi = fp/float(num_image)
  ap, recall, prec = calap(recall, prec)

  return ap, recall, prec, list(fppi.flatten()), list(fp.flatten()), list(conf.flatten()), tp_boxes_all
  #return ap, recall, prec, list(fppi.flatten()), list(fp.flatten()), tp_boxes_all, gt_detections, det_ignores
#---------------------------------------------------------------------------------------------------------
def eval_detection(gt, det,img_name,curve,img_path):


  gt_boxes = dict()
  for anno in gt.keys():
     box = gt [anno]
     if (box == []) :
         box = [[0,0,0,0,0]]
     box = np.array(box)
     gt_boxes[anno] = box
  det_boxes = dict()
  #files = []
  for anno in det.keys():
    #files.append(anno)
    box = det[anno]
    if (box == []) :
        box = [[0,0,0,0,0]]
    box = np.array(box)
    det_boxes[anno] = box
  #print det_boxes["2410/3309.png"]
  #files.sort()
  ap, rec, pre, fppi, fp,conf, tp_boxes = evaluation(det_boxes, gt_boxes)
  kinds = ['pr','fppi','thres' ]

  pr = curve
  if pr == 'pr':
    print ap, rec[-1]
    pylab.plot(rec, pre)
    pylab.xlabel('recall')
    pylab.ylabel('precision')
    pylab.xlim([0, 1])
    pylab.ylim([0, 1])
    #pylab.text(rec[100],pre[100])
    pylab.xticks(np.arange(0.,1,0.05), fontsize = 8)
    pylab.yticks(np.arange(0.,1,0.05), fontsize = 8)
    pylab.title('ap = {}'.format(ap))
    pylab.grid()
  elif pr == 'fppi':
    print 'start  fppi '
    pylab.semilogx(fppi, np.array(rec))

    pylab.xlabel('fppi')
    pylab.ylabel('recall')
    pylab.ylim([0, 1])
    pylab.xlim([0.001,1])
    pylab.xticks(np.power(10, np.arange(-3,0.1,0.1)), fontsize = 8)
    pylab.yticks(np.arange(0.,1.0,0.05), fontsize = 8)
    pylab.title('fppi vs recall')
    pylab.grid()

  elif  pr == 'thres':
    a=pylab.plot(conf, np.array(rec),label='rec')
    b=pylab.plot(conf, pre,label='pre')
    pylab.xlabel('threshold')
    pylab.ylabel('recall & precision')
    pylab.ylim([0, 1])
    pylab.xlim([0, 100])
    pylab.xticks(np.arange(0, 100, 5), fontsize = 8)
    pylab.yticks(np.arange(0.,1.0,0.05), fontsize = 8)
    pylab.title('thr vs recall & precision')
    pylab.legend(loc = 'upper right')

  else  :
      pylab.figure(1,figsize=(25,7))
      print 'AP:',ap,'Recall:', rec[-1]
      pylab.subplot(1,3,1)
      pylab.plot(rec, pre, label = 'ap'+ ': {:0.2f}'.format(ap))
      pylab.plot(rec, pre, label = 'rec'+ ': {:0.2f}'.format(rec[-1]))
      pylab.xlabel('recall')
      pylab.ylabel('precision')
      pylab.xlim([0, 1])
      pylab.ylim([0, 1])
      pylab.xticks(np.arange(0.,1,0.05), fontsize = 8)
      pylab.yticks(np.arange(0.,1,0.05), fontsize = 8)
      pylab.title('recall vs precision')
      pylab.legend(loc=4, borderaxespad=0.)
    #elif pr == 'fppi':
      pylab.subplot(1,3,2)
      pylab.semilogx(fppi, np.array(rec))
      pylab.xlabel('fppi')
      pylab.ylabel('recall')
      pylab.ylim([0, 1])
      pylab.xlim([0.001,1])
      pylab.xticks(np.power(10, np.arange(-3,0.1,0.1)), fontsize = 8)
      pylab.yticks(np.arange(0.,1.0,0.05), fontsize = 8)
      pylab.title('fppi vs recall')
    #else:
      pylab.subplot(1,3,3)
      #afp = calfp(fp, rec)
      #print afp
      pylab.plot(conf, np.array(rec),label='rec')
      pylab.plot(conf, pre,label='pre')
      pylab.xlabel('threshold')
      pylab.ylabel('recall & precision')
      pylab.ylim([0, 1])
      pylab.xlim([0, 100])
      pylab.xticks(np.arange(0, 100, 5), fontsize = 8)
      pylab.yticks(np.arange(0.,1.0,0.05), fontsize = 8)
      pylab.title('thr vs recall & precision')
      pylab.legend(loc=4, borderaxespad=0.)

      pylab.subplot(1,3,1)
      pylab.grid()
      pylab.subplot(1,3,2)
      pylab.grid()
      pylab.subplot(1,3,3)
      pylab.grid()

      pylab.savefig(img_path + os.sep + 'aphadet_' + img_name + '_' + 'all.png')
      quit()








#  for gt in (gt_boxes.keys()):
#   #print pack_fpath + dir_name + '/' + dir_name + '_0' + '.jpg'
#
#   image = cv2.imread('/mnt/hgfs/Share/dfms/' + gt)
#   img_box = gt_boxes[gt]
#   det_box = det_boxes[gt]
#   #print det
#   for i in range(0,len(img_box)):
#       #if (img_box[i,4] == 0):
#         cv2.rectangle(image,(int(img_box[i,0]),int(img_box[i,1])),(int(img_box[i,2]),int(img_box[i,3])),(0,0,255),2)
#       #else:
#         #cv2.rectangle(image, (int(img_box[i, 0]), int(img_box[i, 1])), (int(img_box[i, 2]), int(img_box[i, 3])),(0, 255, 0), 2)
#
#   for j in range(0,len(det_box)):   #if tp_all[j][k] == 1:
#       cv2.rectangle(image,(int(det_box[j,0]),int(det_box[j,1])),(int(det_box[j,2]),int(det_box[j,3])),(0,255,0),2)
#
#
#   cv2.imwrite(img_name +'/'+ gt.split('/')[0] + '_' + gt.split('/')[-1], image)
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  args = parse_args()
  eval_detection(args)
