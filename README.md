# 1. 环境变量设置
alpha_det 环境搭建参见教程
- gpu026.hogpu.cc: `source env_gpu026.sh` 

---
# 2. 数据准备，通过脚本生成，rec和json

数据准备 参见 [./data_path/readme.md](./data_path/readme.md)  
生成过程 参见   [./src/im2rec/README.md](./src/im2rec/README.md)

Run `python DenseboxRec_phone.py`

---
# 3. Train Alphadet
---
## 3.1. Choose local or cluster GPU
训练脚本含义及作用参数详见 ：[./src/train/readme.md](./src/train/readme.md)
### a. 本地GPU训练
```
sh ./src/alphadet/train/phone_train_crop_All_0302.sh
```

---
### b. 集群GPU训练
根据[./src/train/readme.md](./src/train/readme.md) 修改完参数后

执行`./submit.sh phone_remote_train.sh  phone_det_(which your changed)`
## 3.2. Evaluation
---
### 3.2.1 评测模型性能
---
#### a. 利用训练出来的模型生成"检测结果"
参见[./src/train/readme.md](./src/train/readme.md)检测部分  
`phone_detct.sh`为检测脚本，目的是生成模型在测试集上的输出结果。 
会在`/which_alpha/train2/release/bin/`下生成一个`test_result.txt`文本文件。  
* 设置好参数后在`train2`下执行`sh  phone_dete.sh`

---
#### b. 利用"检测结果"画出"评测曲线"
参见 [./src/evaluate/readme.md](./src/evaluate/readme.md)  
执行`python main_test_crop_All.py   ./which_test_result/test_result.txt    ./image_result/your_model_name/    all`

---
## 4. 常用工具
常用工具放在[./tools](tools)中
* phone_demo      [./tools/phone_demo/readme.md](./tools/phone_demo/readme.md)
* scrpits [./tools/scripts/readme.md](./tools/scripts/readme.md)

---