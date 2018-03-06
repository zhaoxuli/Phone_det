cd release/bin
source ./set_env.sh
python det_alpha_new.py \
    --json ~/phone_alpha/data/crop_data_new/test_rec_data/0228_All_rec/train.json \
    --rec ~/phone_alpha/data/crop_data_new/test_rec_data/0228_All_rec/train.rec \
    --resize-canvas 0.7 \
    --layer-num -1 \
    --merge-ivu-thres 0.5 \
    --nms-max-overlap-ratio 0.7 \
    --nms-max-contain-ratio 0.7 \
    --nms-score-thres 0\
    --model  ~/phone_alpha/crop_0304_all_model/24_0128_R0256_F0050.mxa\
    --out_file  crop_0304_All_result.txt \
    #--gpu 0 \ 


#python det_alpha.py \
#--src-prefix ~/ \
#--image ~/det.anno \
#--merge-ivu-thres 0.6 --nms-max-overlap-ratio 0.8 --nms-max-contain-ratio 0.9 --nms-score-thres 1.0 \
#--scan-scale 1.0 0.01 0.8 --restrict-in-image  --max-height 4096 --pad-border 36 --gpu 0 \
#--resize-canvas 0.3 --layer-num -1 \
#--model \
#~/26_0128_R0128_F0050.mxa
