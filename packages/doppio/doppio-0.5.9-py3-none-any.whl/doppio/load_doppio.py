
from albumentations.pytorch import ToTensorV2
import torch
import albumentations as A
from doppio.doppio_dataset import DoppioDataset


def load_doppio(dataset=None, split_dir=None, task_info=None, augmentation = None, valid_classes = None):

    if augmentation == None:
        augmentation =  [A.Resize(width=1000, height=1000), ToTensorV2(transpose_mask=True)]


    custom_dataset = DoppioDataset(dataset=dataset, split_dir=split_dir, task_info=task_info, augmentation=augmentation, valid_classes=valid_classes)# [A.Resize(width=512, height=512),ToTensorV2(transpose_mask=True)])
    my_dataset_loader = torch.utils.data.DataLoader(dataset=custom_dataset,
                                                    batch_size=2,
                                                    shuffle=True,  num_workers=0, collate_fn=collate)

    return my_dataset_loader
