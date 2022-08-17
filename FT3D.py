from glob import glob
import os
from pathlib import Path
ld = glob(f'{os.environ["Dataria"]}/FT3D/Subset/Frames_cleanpass/*/*/*/*/')

for i in ld  :
    print(i)
    out_path = f"os.environ['Dataria']/FT3D/Subset/OpticalFlowARFlow/" + i.replace(os.environ['Dataria'], '')
    print(f'Out : {out_path}')
    if Path(out_path).exists() :
        print('Already Processed')
    else :
        os.system(f'python3 batch_flow.py -i {i} -od $Dataria/FT3D/Subset/OpticalFlowARFlow/')
