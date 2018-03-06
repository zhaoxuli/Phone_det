## train
该文件夹用于存放训练参数脚本的文件，一般情况下，训练脚本存放于，alpha_det,的`train2`下。   
从功能上区分为**本地训练脚本**和**集群训练脚本** 

各个参数的意义/功能详见  http://wiki.hobot.cc/pages/viewpage.action?pageId=12747891  
`data_prefix` 是alpha_det生成rec数据的父级目录，即为训练样本生成的rec  
`json_prefix` 是alpha_det生成json的父级目录，即为训练样本生成的json  
`model_prefix`是alpha_det输出模型的文件夹，需要不存在的路径，如果该路径存在则会报错 

在`shell`文件中选择环境设置即可
```
#cd ./release/bin/     //本地端训练所需要的环境                   
#source ./set_env.sh   //本地端训练所需要的环境

export MXNET_GPU_MEM_POOL_RESERVE=20      //集群训练所需环境
export CLASSPATH=$HADOOP_HOME/lib/classpath_hdfs.jar   //集群训练所需环境
```
另外集群训练的操作流程可以参考    http://wiki.hobot.cc/pages/viewpage.action?pageId=23726906

##  detect
`phone_detct.sh`为检测脚本，目的是生成模型在测试集上的输出结果。会在`/which_alpha/train2/release/bin/`下生成一个`test_result.txt`文本文件  

参数详见 上面的alpha_det参数详解  
`--json`为验证集的json路径  
`--rec`为验证集rec所在路径  
`--model`为模型所在路径