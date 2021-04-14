---
layout: post
title:  "Popular models for object detection - a brief study"
date:   2021-04-14
image:  images/blog5/cover.jpg
tags:  AI object detection rcnn yolo anchor boxes fcn cnn deep learning
---
*On the cover: Yolov5 applied on an Avengers endgame poster; also Rocket wouldn't like being called a dog huehue

Object detection is one of the classical problems in deep learning for computer vision next to image classification. The goal of object detection is to localize the objects present in an image in addition to classifying it. Typically, one predicts **bounding boxes** for localization and **confidence scores** for classification of all the objects present in the image. If the outputs are **segmentations** instead of bounding boxes, then it's called an instance segmentation task. 

There is a lot of research done in this area and it can be overwhelming to remember all the details. If only I had a dollar for everytime I forgot what YOLO or Faster RCNN does internally and had to read the paper again. Hence, this blog post strives to quickly summarize the popular architectures that gave shape to this field. This blog post is not a tutorial, rather a post to jog your memory of these architectures. Relevant links are provided for reference. Most of these architectures are tested on the [PASCAL VOC dataset (2007, 2012)](http://host.robots.ox.ac.uk/pascal/VOC/#:~:text=The%20PASCAL%20VOC%20project%3A,and%20comparison%20of%20different%20methods) and recently on [COCO dataset](https://cocodataset.org/#detection-2020) as well 

## R-CNN: [paper](https://arxiv.org/pdf/1311.2524.pdf)
![alt](/images/blog5/rcnn.png)
*R-CNN architecture*
1. Selective search algorithm to propose candidate regions (of ~2000 boxes)
2. Warp the candidate regions to fixed size
3. Train a CNN (eg. VGG16) to extract features
4. Train n SVMs (one for each class) for object classification 

## Fast R-CNN: [paper](https://arxiv.org/pdf/1504.08083.pdf)
![alt](/images/blog5/fast-rcnn.png)
*Fast R-CNN architecture*
1. Use any algorithm to propose candidate regions (of ~2000 boxes)
2. Produce a conv feature map of the input image using a CNN (eg. VGG net)
3. Extract projected region proposals on the conv feature map from the reduction ratio (eg. input: 256x256; feature map: 32x32; reduction ratio: 1/8; proposal: 40x16; extracted projection: (40x16)/8 = 5x2 on the feature map)
4. Use an [RoI pooling](https://stackoverflow.com/questions/43430056/what-is-the-purpose-of-the-roi-layer-in-a-fast-r-cnn) layer on these feature maps to produce a fixed size smaller feature map (7x7 in this paper)
4. Feed each fixed length feature vector into a sequence of FC layers
5. Feed the output of FC layers into two sibling layers: softmax layer for object classification (output: prob p<sub>k</sub>) and a class specific bbox regressor (output: offsets t<sub>k</sub><sup>x</sup>, t<sub>k</sub><sup>y</sup>, t<sub>k</sub><sup>h</sup>, t<sub>k</sub><sup>w</sup> for every k)

## Faster R-CNN: [paper](https://arxiv.org/pdf/1506.01497.pdf)
![alt](/images/blog5/faster-rcnn.png)
*Faster R-CNN architecture*
1. Pass the image into a CNN to extract a feature map (say conv5 of VGG) which is common to two parts of this network: a Region proposal network (RPN) and a Fast R-CNN
2. The RPN uses a sliding window of fixed size (3x3 in this paper) to extract a 512-d output (conv5 of VGG has 512 as the third dimension) at **each wxh** of the feature map
![alt](/images/blog5/RPN.png)
*RPN architecture*
3. This is then connected to two sibling FC layers that output objectness scores and bounding box proposals through 9 anchor boxes (a predetermined set of boxes with various dimensions and aspect sizes)
3. Label all these proposed boxes as positive (iou>0.7), negative (iou<0.3) or ignore (ow) where iou is wrt to the ground truths and train the RPN using SGD
4. Pass the proposals into a RoI pooling layer and subsequently regress bboxes and predictions like in Fast-RCNN
5. In the paper RPN and detection networks are trained separately; RPN serves as an attention mechanism

## YOLO: [paper](https://arxiv.org/pdf/1506.02640.pdf)
![alt](/images/blog5/yolo_explained.png)
*YOLO data flow*
![alt](/images/blog5/yolo.png)
*Yolo architecture; YOLO reaches 45 fps (mAP 63.4 on 07 VOC) compared to Faster RCNN which reaches only 7 fps (mAP 73.2 on 07 VOC)*
1. Single unified end-to-end architecture (Darknet instead of VGG16 as feature extractor) predicting bounding boxes and class scores
2. Divide the input image into grids of SxS (S=7 in the paper)
3. For each grid, predict B (B=2 in the paper) bounding boxes (each bounding box has 5 predictions: 2 center coordinates (Xc, Yc), 2 dimensions (H,W) and 1 objectness score) and C (C=20 in VOC) class probabilities. Hence the output would be SxSx(5*B + C) tensor, ie., 7x7x30 tensor
4. The predictions Xc, Yc are assumed to be offset wrt the Grid cell location and H,W are also offset wrt to the size of the image 

## YOLO v2: [paper](https://arxiv.org/pdf/1612.08242.pdf)
![alt](/images/blog5/yolov2-bb.png)
*YOLOv2 dimension priors and offsets*
YOLO makes a significant number of localization errors. Yolov2 tries to fix this. Similar to YOLO with following changes:
1. Higher resolution Darknet 19: base model pre-trained at image size of 448x448 instead of 224x224 (during object detection changed to 416 to get odd number of locations in the feature map (13x13) and there is a single center cell)
2. Add Batch Normalization to all the conv layers 
3. Remove fc layers in YOLO and use anchors for prediction; cluster anchor box dimensions (using k-means; k=5 in this paper) on VOC and COCO instead of handpicked dimensions (3 aspect ratios and 3 sizes)
4. At each cell in feature map 13x13, predict 5 (number of clustered anchors) bounding boxes and for each bounding box predict 5 values (2 coordinates, 2 dimensions and 1 confidence)
5. Direct and stable bounding box location prediction using sigmoids and exponentials (in the image above)
6. Use a skip connection for fine-grained feature learning; to skip and concatenate a higher dimension layer of size 26x26x512, convert and stack it into 13x13x2048 for concatenation with the last layer 
7. Multi-scale training of sizes (288, 320, 352, 384, 416, .., 544, .., 608) (multiples of 32 as that is the reduction size) for robustness to different image sizes (although yolov2 is independent of input image size)

## YOLO v3: [paper](https://arxiv.org/pdf/1804.02767.pdf)
Incremental improvements over YOLOv2:
1. Use DarkNet53; Each bounding box predicts exactly one ground truth; assign the ground truth box to bounding box if the corresponding anchor box has the highest overlap and more than 0.5 IOU 
2. Binary cross-entropy loss for each class (to predict overlapping classes eg., Woman, Person) instead of softmax and multi class cross entropy
2. Use [FPN](https://arxiv.org/pdf/1612.03144.pdf) (Feature Pyramid Network) like feature pyramid predictions at 3 scales (the 9 clustered anchor box sizes are split evenly across these scales); the output tensor for the scale of size NxN is N×N×[3 ∗ (4 + 1 + 80)]; 80 classes
3. There's also a Yolov3-tiny variant (has the highest fps) and a [Yolov3-SPP](https://stackoverflow.com/questions/54998225/yolov3-spp-and-yolov3-difference) variant (yields higher mAP score)

## RetinaNet: [paper](https://arxiv.org/pdf/1708.02002.pdf)
![alt](/images/blog5/retinanet.png)
*RetinaNet architecture*
1. Use Feature Pyramid Network as the backbone to extract rich multi-scale feature pyramids
2. Then pass this into a classification subnet and a bbox regression subnet (both FCNs without sharing parameters) with anchors to predict boxes and classes
3. This is a dense prediction where you predict these bboxes for every pixel of the feature map as opposed to sparse predictions in Faster R-CNN 
4. Use focal loss to account for object to background class imbalance in the data for single level detection

## Mask R-CNN: [paper](https://arxiv.org/pdf/1703.06870.pdf)
People have started to care more about segmentation masks than bounding boxes :)
1. Has the same architecture as that of Faster R-CNN
2. In addition to predicting bbox and class probabilities, it has an [FCN](https://towardsdatascience.com/implementing-a-fully-convolutional-network-fcn-in-tensorflow-2-3c46fb61de3b) (Fully Convolutional Network) attached at the end with deconvolution layers for predicting masks
3. Since there needs to be a one-to-one input image to feature map alignment, [RoI Align](https://towardsdatascience.com/understanding-region-of-interest-part-2-roi-align-and-roi-warp-f795196fc193)) is used instead of RoI Pooling (which does harsh quantizations); RoIAlign is the main ingredient of Mask R-CNN

## Feature Pyramid Network: [paper](https://arxiv.org/pdf/1612.03144.pdf)
![alt](/images/blog5/fpn.png)
*FPN architecture*
1. Provides a multi-scale rich feature pyramid
2. Contains a bottom-up pathway (normal ResNet feature extraction) and a top-down pathway (constructing pyramids). Top-down pathway is explained as follows for a 5 layer ResNet: (P satnds for pyramid)
- P5: Use the last layer outputs: C5, channel size N-d, and convert them to 256-d channels using 1x1 convolutions
- P4: Upsample P5 (x2) with the nearest neighbor upsampling to get the same spatial resolution of C4; convert C4 to 256-d by 1x1 convs; now merge these two: P4 = upsampled(P5) + 1x1convolved(C4)
- P3, P2 same procedure used for P4
5. Do a 3x3 convolution in order to avoid aliasing effects after each merge
6. P1 is not constructed as it is too large for computations https://jonathan-hui.medium.com/understanding-feature-pyramid-networks-for-object-detection-fpn-45b227b9106c


## Question: How do the models handle different image sizes?
One typically asks this question while studying all these models. This is answered [here](https://ai.stackexchange.com/questions/6274/how-can-i-deal-with-images-of-variable-dimensions-when-doing-image-segmentation) nicely. R-CNN and YOLO cannot handle various image sizes, since they have fully connected layers as part of the feature extraction network. Fast R-CNN (thus also Faster R-CNN; RPN is a FCN) allows different input image sizes beacuse of RoI pooling that outputs fixed size smaller feature maps for further steps. These days most architectures allow variable input image sizes as input because of these modules in them: 
### FCN and SPP:
![alt](/images/blog5/spp.png)
*SPP architecture; 256 is the filter number of the conv5 layer, and conv5 is the last convolutional layer*
1. Both these techniques allow one to use varied size input images unlike traditional Imagenet models that consume only fixed size inputs 
2. Fully Convolutional Networks (FCN): Use 1x1 convolutions instead of dense connections and finally use Global pooling at the end
3. Spatial Pyramid Pooling (SPP): This maintains spatial information in local spatial bins. Effectively, define three bin sizes (1, 4, 16) for pooling the last feature map of arbitrary size (HxWx256 dimensions). For each of these bin sizes pool the feature map. Concatenate these fixed size pooled features then use dense connections at the end.
