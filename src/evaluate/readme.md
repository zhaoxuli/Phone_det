该文件夹的作用是根据detect出的`tset_result.txt`去验证模型的性能，  
绘制`PR`,`fppi`,`thres&recall&precition` 的曲线   
运行方式为：  
`python main_test_crop_All.py   ./which_test_result/test_result.txt    ./image_result/crop_0304_All/    all`

第一个参数为`test_result.txt`路径  
第二个参数为性能曲线保存的位置  
第三个参数为曲线类型，分为'pr','fppi','thres','all'