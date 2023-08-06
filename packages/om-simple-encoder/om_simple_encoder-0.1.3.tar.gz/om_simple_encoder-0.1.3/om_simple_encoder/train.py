import torch
from argparse import ArgumentParser
from pytorch_lightning import Trainer
from om_simple_encoder.text_image_dm import TextImageDataModule
from om_simple_encoder import CustomCLIPWrapper
from torchvision.models import resnet50,vit_b_16
from transformers import AutoTokenizer, AutoModel
from pytorch_lightning.loggers import MLFlowLogger
import timm


def start_train(model_type="resnet50", img_dir="/mnt/soco1/brands/", data="brands.json", batch_size=64):
    if "swin" in model_type:
        img_encoder = timm.create_model('swin_base_patch4_window7_224',pretrained=True)
    elif "resnet" in model_type:
        img_encoder = resnet50(pretrained=True)
        img_encoder.fc = torch.nn.Linear(2048, 1000)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CustomCLIPWrapper(img_encoder, minibatch_size=batch_size)
    dm = TextImageDataModule(img_dir, data, batch_size=batch_size, num_workers=16, image_size=224, resize_ratio=0.75, shuffle=True, mode="train_only") 
    trainer = Trainer(precision=16, max_epochs=5000,gpus=1)#,logger=mlf_logger)
    trainer.fit(model, dm)

if __name__ == '__main__':
    pass
