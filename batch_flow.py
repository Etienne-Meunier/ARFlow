from glob import glob
import os, sys
from natsort import natsorted
from ipdb import set_trace
from inference import TestHelper
import imageio
import argparse
import numpy as np
from tqdm import tqdm
from pathlib import Path

from utils.flow_utils import resize_flow, writeFlow

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', default='checkpoints/KITTI15/pwclite_ar.tar')
parser.add_argument('-s', '--test_shape', default=[384, 640], type=int, nargs=2)
parser.add_argument('-i', '--folder', required=True)
parser.add_argument('-bd', '--base_dir', default=os.environ['Dataria'])
parser.add_argument('-od', '--output_dir', required=True)

args = parser.parse_args()

cfg = {
    'model': {
        'upsample': True,
        'n_frames': 2,
        'reduce_dense': True
    },
    'pretrained_model': args.model,
    'test_shape': args.test_shape,
}
ts = TestHelper(cfg)


file_list = natsorted(glob(args.folder+'/*.png')) + natsorted(glob(args.folder+'/*.jpg'))
frames = [imageio.imread(img).astype(np.float32) for img in file_list]
h, w = frames[0].shape[:2]
pbar = tqdm(range(len(frames)-1), total=len(frames)-1)

for i in pbar :
    pbar.set_description(f"{'/'.join(file_list[i].split('/')[-2:])} -> {'/'.join(file_list[i+1].split('/')[-2:])}")
    flow_12 = ts.run([frames[i], frames[i+1]])['flows_fw'][0]
    h, w = frames[i].shape[:2]
    flow_12 = resize_flow(flow_12, (h, w))
    np_flow_12 = flow_12[0].detach().cpu().numpy().transpose([1, 2, 0])
    path = Path(file_list[i].replace(args.base_dir, args.output_dir))
    path.parent.mkdir(parents=True, exist_ok=True)
    writeFlow(path.with_suffix('.flo'), np_flow_12)
