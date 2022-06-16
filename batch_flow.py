from blob import blob
import os, sys
from natsort import natsorted
from ipdb import set_trace

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', default='checkpoints/KITTI15/pwclite_ar.tar')
parser.add_argument('-s', '--test_shape', default=[384, 640], type=int, nargs=2)
parser.add_argument('-i', '--folder_list', nargs='+',
                    default=['examples/img1.png', 'examples/img2.png'])
parser.add_argument('-bd', '--base_dir', default=os.environ['Dataria'])

args = parser.parse_args()

cfg = {
    'model': {
        'upsample': True,
        'n_frames': len(args.img_list),
        'reduce_dense': True
    },
    'pretrained_model': args.model,
    'test_shape': args.test_shape,
}

ts = TestHelper(cfg)

imgs = [imageio.imread(img).astype(np.float32) for img in args.img_list]
h, w = imgs[0].shape[:2]

flow_12 = ts.run(imgs)['flows_fw'][0]

flow_12 = resize_flow(flow_12, (h, w))
np_flow_12 = flow_12[0].detach().cpu().numpy().transpose([1, 2, 0])

vis_flow = flow_to_image(np_flow_12)

fig = plt.figure()
plt.imshow(vis_flow)
plt.show()


for folder in args.folder_list :
    print(f'Folder : {folder}')
    file_list = natsorted(glob(args.base_dir+folder+'*.png')) + natsorted(glob(args.base_dir+folder+'*.jpg'))
    imgs = [imageio.imread(img).astype(np.float32) for img in file_list]
    h, w = imgs[0].shape[:2]

    cfg = {
        'model': {
            'upsample': True,
            'n_frames': len(args.img_list),
            'reduce_dense': True
        },
        'pretrained_model': args.model,
        'test_shape': [h, w],
    }
    flow_12 = ts.run(imgs)['flows_fw'][0]
    np_flow_12 = flow_12[0].detach().cpu().numpy().transpose([1, 2, 0])
    
