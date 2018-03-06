**该project是phone_demo的演示程序，有读入视频和摄像头两种方式**  
## 使用
将phone_model(可执行文件.bin)放入`./models/phone_models`中  
运行`python  phone_demo.py`  
通过修改脚本主程序中的`thres和input_type`来修改阈值和输入方式
##  注意
clone到本地后一定要修改子函数`get_phone_loc`中的 `cmd`，该函数是通过调用 alpha_det 预测库来进行预测结果，  
详细修改方式参见  http://gitlab.k8s.hobot.cc/car-algorithm/Tutorials/tree/alphaDet_Prediction/alpha-det-prediction