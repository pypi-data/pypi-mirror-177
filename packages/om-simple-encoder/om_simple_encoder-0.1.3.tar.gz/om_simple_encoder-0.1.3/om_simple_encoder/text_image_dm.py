from pathlib import Path
from random import randint, choice
import json
import random

import PIL
import argparse
import om_simple_encoder.clip as clip
import torch
import os

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from pytorch_lightning import LightningDataModule
from timm.data.transforms_factory import create_transform


class TextImageDataset(Dataset):
    def __init__(self,
                 mode: str="train",
                 img_dir: str="",
                 data: str="",
                 image_size=224,
                 resize_ratio=0.75,
                 shuffle=False
                 ):
        super().__init__()
        self.shuffle = shuffle
        self.img_dir = img_dir        
        if data:
            self.data = json.load(open(data))
            if mode == "train_only":
                if not "train" in self.data:
                    self.keys = list(self.data.keys())
                elif "val" in self.data and "train" in self.data:
                    self.keys = list(self.data["train"].keys())+list(self.data["val"].keys())
            elif mode == "train":
                if "train" in self.data:
                    self.data = self.data["train"]
                    keys = self.data.keys()
                    self.keys = list(keys)
                else:
                    keys = list(self.data.keys())
                    self.keys = keys[:int(len(keys)*0.9)]
            else:
                if "val" in self.data:
                    self.data = self.data["val"]
                    keys = self.data.keys()
                    self.keys = list(keys)
                else:
                    keys = list(self.data.keys())
                    self.keys = keys[int(len(keys)*0.9):]
        self.resize_ratio = resize_ratio
        print (mode)
        if mode == "train" or mode == "train_only":
            #self.image_transform = create_transform(224, is_training=True,auto_augment="rand-m9-n3-mstd0.5")
            #print (self.image_transform)
            self.image_transform = T.Compose([
                T.Lambda(self.fix_img),
                T.RandomResizedCrop(image_size,
                                scale=(self.resize_ratio, 1.),
                                ratio=(1., 1.)),
                T.ToTensor(),
                T.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
            ])
        else:
            #self.image_transform = create_transform(224,)
            self.image_transform = T.Compose([
                T.Lambda(self.fix_img),
                T.Resize((image_size,image_size)),
                T.ToTensor(),
                T.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
            ])
 
    def __len__(self):
        return len(self.keys)
    
    def fix_img(self, img):
        return img.convert('RGB') if img.mode != 'RGB' else img

    def random_sample(self):
        return self.__getitem__(randint(0, self.__len__() - 1))

    def sequential_sample(self, ind):
        if ind >= self.__len__() - 1:
            return self.__getitem__(0)
        return self.__getitem__(ind + 1)

    def skip_sample(self, ind):
        if self.shuffle:
            return self.random_sample()
        return self.sequential_sample(ind=ind)

    def __getitem__(self, ind):
        key = self.keys[ind]
        if len(self.data[key]) == 1:
            image_file1 = self.data[key][0]
            image_file2 = self.data[key][0]
        elif len(self.data[key]) > 1:
            image_file1, image_file2 = random.sample(self.data[key], 2)
        else:
            return self.skip_sample(ind)
        try:
            image_tensor1 = self.image_transform(self.fix_img(PIL.Image.open(os.path.join(self.img_dir,image_file1))))
            #image_tensor1 = self.image_transform(PIL.Image.open(os.path.join(self.img_dir,image_file1)))
            image_tensor2 = self.image_transform(self.fix_img(PIL.Image.open(os.path.join(self.img_dir,image_file2))))
            #image_tensor2 = self.image_transform(PIL.Image.open(os.path.join(self.img_dir,image_file2)))
        except (PIL.UnidentifiedImageError, OSError) as corrupt_image_exceptions:
            #print(f"An exception occurred trying to load file {image_file1}.")
            #print(f"An exception occurred trying to load file {image_file2}.")
            #print(f"Skipping index {ind}")
            return self.skip_sample(ind)
        # Success
        return image_tensor1, image_tensor2

class TextImageDataModule(LightningDataModule):
    def __init__(self,
                 img_dir: str="",
                 data: str="",
                 batch_size: int=32,
                 num_workers=0,
                 image_size=224,
                 resize_ratio=0.75,
                 shuffle=False,
                 mode:str="train_only"
                 ):
        """Create a text image datamodule from directories with congruent text and image names.

        Args:
            img_dir (str): Folder containing images and text files matched by their paths' respective "stem"
            batch_size (int): The batch size of each dataloader.
            num_workers (int, optional): The number of workers in the DataLoader. Defaults to 0.
            image_size (int, optional): The size of outputted images. Defaults to 224.
            resize_ratio (float, optional): Minimum percentage of image contained by resize. Defaults to 0.75.
            shuffle (bool, optional): Whether or not to have shuffling behavior during sampling. Defaults to False.
        """
        super().__init__()
        self.img_dir =img_dir
        self.data = data
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.image_size = image_size
        self.resize_ratio = resize_ratio
        self.shuffle = shuffle
        self.mode = mode

    """ 
    @staticmethod
    def add_argparse_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--img_dir', type=str,  help='directory of your training img_dir')
        parser.add_argument('--data', type=str,  help='directory of your training img_dir')
        parser.add_argument('--batch_size', type=int, help='size of the batch')
        parser.add_argument('--num_workers', type=int, default=0, help='number of workers for the dataloaders')
        parser.add_argument('--image_size', type=int, default=224, help='size of the images')
        parser.add_argument('--resize_ratio', type=float, default=0.75, help='minimum size of images during random crop')
        parser.add_argument('--shuffle', type=bool, default=True, help='whether to use shuffling during sampling')
        return parser
    """
    
    def setup(self, stage=None):
        if self.mode == "train_only":
            self.dataset_train = TextImageDataset(mode="train_only", img_dir=self.img_dir, data=self.data, image_size=self.image_size, resize_ratio=self.resize_ratio, shuffle=self.shuffle)
            self.dataset_val = TextImageDataset(mode="val", img_dir=self.img_dir, data=self.data, image_size=self.image_size, resize_ratio=self.resize_ratio, shuffle=False)
        else:
            self.dataset_train = TextImageDataset(mode="train", img_dir=self.img_dir, data=self.data, image_size=self.image_size, resize_ratio=self.resize_ratio, shuffle=self.shuffle)
            self.dataset_val = TextImageDataset(mode="val", img_dir=self.img_dir, data=self.data, image_size=self.image_size, resize_ratio=self.resize_ratio, shuffle=False)
    
    def train_dataloader(self):
        return DataLoader(self.dataset_train, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers, drop_last=True , collate_fn=self.dl_collate_fn)
    
    def val_dataloader(self):
        return DataLoader(self.dataset_val, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, drop_last=True , collate_fn=self.dl_collate_fn)
    
    def dl_collate_fn(self, batch):
        return torch.stack([row[0] for row in batch]), torch.stack([row[1] for row in batch])
