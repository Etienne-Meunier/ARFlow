for i in $Dataria/DAVIS/JPEGImages/480p/*;
  do
    trap <command> SIGINT
    echo $i
    python3 batch_flow.py -i $i -od $Dataria/DAVIS/OpticalFlowARFlowKitti1/\
                          --model checkpoints/KITTI15/pwclite_ar.tar\
                          -s 448 1024
  done
