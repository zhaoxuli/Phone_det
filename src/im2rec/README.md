
`DenseboxRec_phone.py`  
**作用：** 主要是将训练的原始图片和anno（json/txt）转换成alpha_det可用的rec和json文件  
**使用：** 主函数中
* `data_path` 为原始图片存储位置
* `json_path` 为原始Anno的位置
*  `output_path` 为输出rec和json的位置
*  `object_type` 是检测模型中Anno信息中的关键字，phone为`'common_box'`
 
 此外，运行该脚本需要执行`densebox_im2rec.bin`二进制文件，会需要一些alpha_det的库
