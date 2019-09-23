import torch
from nets import vgg_module
import cv2 as cv
import numpy as np
import time
from penguin import getsingleimg

x, show = getsingleimg()
vgg_test = vgg_module()
# print(vgg_test)

vgg_test.load_weights('./models/ssd300_mAP_77.43_v2.pth')
vgg_test.eval()
vgg_test = vgg_test.cuda()
torch.backends.cudnn.benchmark = True
a = time.time()
r = vgg_test(x).data#.numpy()[0]
print(time.time()-a)
for j in range(1, r.size(1)):
    dets = r[0, j, :]
    mask = dets[:, 0].gt(0.).expand(5, dets.size(0)).t()
    dets = torch.masked_select(dets, mask).view(-1, 5)
    if dets.size(0) == 0:
        continue
    boxes = dets[:, 1:].numpy()[0]
    boxes *= 300
    boxes = boxes.astype(int)
    cv.rectangle(show, (boxes[0],boxes[1]), 
    (boxes[2], 
     boxes[3]), 255)
print(boxes)    
cv.imshow('sdf', show)
cv.waitKey()