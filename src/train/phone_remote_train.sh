#cd ./release/bin/
#source ./set_env.sh
source ./remote_env.sh
export MXNET_GPU_MEM_POOL_RESERVE=20
export CLASSPATH=$HADOOP_HOME/lib/classpath_hdfs.jar

python run.py --ref_w 40 \
          --ref_h 60 \
          --norm_method "height" \
          --norm_length 38 \
          --min_valid_norm_length 20 \
          --img_w 384 \
          --img_h 256 \
          --positive_scale_upper_bound 1.1 \
          --positive_scale_lower_bound 0.9 \
          --regression_scale_upper_bound 1.5 \
          --regression_scale_lower_bound 0.67 \
          --ignore_scale_upper_bound 2\
          --ignore_scale_lower_bound 0.5 \
          --max_rotate_angle 5 \
          --flip_hori \
          --positive_region_radius_ratio 0.1 \
          --regression_region_radius_ratio 0.2 \
          --ignore_region_radius_ratio 0.4 \
          --train_speed_profile standard \
          --model_shape_profile standard \
          --sample_reject_profile mild \
          --label_quality_profile standard \
          --bbox_reg_profile preciser \
          --constraint_mode fpga \
          --term_false_positive_rate 1E-7 \
          --ctx "0,1" \
          --model_max_layer_num 24 \
          --data_prefix hdfs://hobot-bigdata/user/dawei.yang/zhaoxu.li/phone_detect/crop_data_new/train_rec_data/0228_All_rec/ \
          --json_prefix hdfs://hobot-bigdata/user/dawei.yang/zhaoxu.li/phone_detect/crop_data_new/train_rec_data/0228_All_rec/ \
          --no_validation \
          --model_prefix hdfs://hobot-bigdata/user/dawei.yang/zhaoxu.li/phone_detect/test_0305_phone/

