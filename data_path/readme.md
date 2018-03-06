## phone_data 说明介绍
### 1.  数据类型简介 
phone的数据从  
**源头**来分暂时可以分为`NET_DATA` 和 `Org_data`,即网络图片和公司自录图片。  
**类型**来分可分为`crop_data`和`No_crop_data` , 即crop后图片和原始图片。（crop目的是为了更好收敛）  
phone数据详情可以参见：  http://wiki.hobot.cc/pages/viewpage.action?pageId=30852043

### 2.训练数据存放位置
**026服务器本地数据存放于**:`/home/users/dawei.yang/phone_alpha/data`  
其中有两个子文件夹 `crop_data_new  Org_data`对应于crop和未crop的数据,文件夹内结构均为:  
```
├── test_data
│   ├── Anno
│   ├── Anno_2test
│   └── Image
├── test_rec_data
├── train_data
│   ├── Anno
│   ├── Anno_2train
│   └── Image
└── train_rec_data
```
其中`Anno`用于存放json文件，`Image`用于存放原始图片，通过调整`Anno_2*`内的json文件来生成不同的rec文件存放于`*rec_data`中   

如何生成rec文件参见  [../src/im2rec/README.md](../src/im2rec/README.md)

**集群训练所用数据位于**：`/opt/hdfs/user/dawei.yang/zhaoxu.li/phone_detect/crop_data_new`