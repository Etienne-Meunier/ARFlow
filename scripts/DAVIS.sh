for i in $Dataria/DAVIS/JPEGImages/480p/*;
  do
    trap <command> SIGINT
    echo $i
    python3 batch_flow.py -i $i -od $Dataria/DAVIS/OpticalFlowARFlow/
  done
