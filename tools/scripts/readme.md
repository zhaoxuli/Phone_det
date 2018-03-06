该文件夹下为处理phone数据的常用脚本： 
 
`crop_img_from_json_no_resize.py`  根据json里面的head点,将头部附近的区域截取出来，做成crop_data  

`crop_img_from_txt_no_resize.py` 根据txt里面的head点,将头部附近的区域截取出来，做成crop_data  

`get_test_data.py` 将Image中的图片，按一定比例提取出测试集，生成新的Anno文件  

`phone_Augmentation_gray.py`对数据集做扰动，生成单通道的灰度图  

`get_fp_all.py` 根据`test_result.txt`/ `ground_truth.json`以及`Image`生成fp图像  

`amend.py`当im2rec 不成功时，用它，一般情况下都是有无效图片或者图片的尺寸和anno的信息不符合。  

`out_gt.py` 将gt打在图片上  

`show_phone_gt.py`  参考  http://njdrive01.hobot.cc/zhaoxu/zhaoxu_scripts  将Anno信息打在图片上，可以通过按键进行微调，gt位置