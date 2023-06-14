_base_ = 'mask-rcnn_r50-caffe_fpn_ms-poly-3x_coco.py'

dataset_type = 'CocoDataset'
classes = ('apple', 'backpack', 'bag, handbag, pocketbook, purse', 'banana', 'bed', 'book', 'bowl', 'box', 'cabinet', 'chair', 'chocolate candy', 'coffee maker', 'coffee table, cocktail table', 'cookie sheet', 'dishwasher', 'dog house', 'floor lamp', 'fork', 'globe', 'hairbrush', 'headphone', 'jug', 'kitchen utensil', 'knife', 'laptop, laptop computer', 'microwave', 'painting', 'pan', 'pen', 'pencil', 'pepper mill, pepper grinder', 'picture', 'printer', 'refrigerator', 'sculpture', 'sofa', 'spoon', 'suitcase', 'table', 'table lamp', 'teakettle', 'television set', 'throw pillow', 'toaster', 'toothbrush', 'toy', 'trunk', 'vase', 'wineglass')
data_root='/home/zfchen/csl/test/tdw_rcnn/data_rcnn'

# train_dataloader = dict(
#     batch_size=4,
#     num_workers=1,
#     dataset=dict(
#         type=dataset_type,
#         # 将类别名字添加至 `metainfo` 字段中
#         metainfo=dict(classes=classes),
#         data_root=data_root,
#         ann_file='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/coco_train.json',
#         data_prefix=dict(img='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/')
#     )
# )

# val_dataloader = dict(
#     batch_size=4,
#     num_workers=1,
#     dataset=dict(
#         type=dataset_type,
#         test_mode=True,
#         # 将类别名字添加至 `metainfo` 字段中
#         metainfo=dict(classes=classes),
#         data_root=data_root,
#         ann_file='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/coco_val.json',
#         data_prefix=dict(img='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/')
#     )
# )

# test_dataloader = dict(
#     batch_size=4,
#     num_workers=1,
#     dataset=dict(
#         type=dataset_type,
#         test_mode=True,
#         # 将类别名字添加至 `metainfo` 字段中
#         metainfo=dict(classes=classes),
#         data_root=data_root,
#         ann_file='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/coco_test.json',
#         data_prefix=dict(img='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/')
#     )
# )

# val_evaluator = dict(
#     type='CocoMetric',
#     ann_file='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/coco_val.json',
#     metric=['bbox', 'segm'],
#     format_only=False,
#     backend_args=None)

# test_evaluator = dict(
#     type='CocoMetric',
#     ann_file='/home/zfchen/csl/test/tdw_rcnn/data_rcnn/coco_test.json',
#     metric=['bbox', 'segm'],
#     format_only=False,
#     backend_args=None)


# 2. 模型设置

# 将所有的 `num_classes` 默认值修改为 5（原来为80）
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=49),
        mask_head=dict(num_classes=49)))

vis_backends = [
    dict(type='LocalVisBackend'),
    dict(type='WandbVisBackend',
         init_kwargs={
            'project': 'mmdetection',
            'group': 'maskrcnn-r50-fpn-1x-coco'
         })
]
visualizer = dict(
    type='DetLocalVisualizer',
    vis_backends=vis_backends,
    name='visualizer')

visualization = _base_.default_hooks.visualization
# enable visualization
visualization.update(dict(draw=True, show=False))

# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = 'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
