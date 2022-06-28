for i in $Dataria/FT3D/Subset/Frames_cleanpass/*/*/*/*/;
  do
    echo $i
    python3 batch_flow.py -i $i -od $Dataria/FT3D/Subset/OpticalFlowARFlow/
  done
