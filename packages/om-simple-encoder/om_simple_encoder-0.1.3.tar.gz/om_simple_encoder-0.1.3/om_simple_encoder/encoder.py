import math
import torch
from om_simple_encoder import CustomCLIPWrapper
from om_simple_encoder.text_image_dm import TextImageDataset
import torch.nn.functional as F
#from sentence_transformers import SentenceTransformer, util
#import PIL
from PIL import Image, ImageFile
from torchvision.models import resnet50
import om_simple_encoder.clip as clip
import timm
import requests
import io

class Encoder(object):
    def __init__(self, PATH="best.ckpt"):
        #img_encoder = SentenceTransformer('clip-ViT-B-32')
        if "swin" in PATH:
            img_encoder = timm.create_model('swin_base_patch4_window7_224',pretrained=True)
        else:
            img_encoder = resnet50(pretrained=True) 
            img_encoder.fc = torch.nn.Linear(2048, 1000)
 
        self.model = CustomCLIPWrapper.load_from_checkpoint(checkpoint_path=PATH, image_encoder=img_encoder, minibatch_size=64)
        self.data_loader = TextImageDataset(mode="val")
        #self.data_loader = TextImageDataset()
        self.model.eval()

    def images(self, urls):
        images = []
        for url in urls:
            if "http" in url:
                #r = requests.get(url, stream=True)
                #aux_im = Image.open(io.BytesIO(r.content))
                #image = self.data_loader.image_transform(aux_im)
                response = requests.get(url)
                if response.history:
                    print("Request was redirected")
                    for resp in response.history:
                        print(resp.status_code, resp.url)
                    print("Final destination:")
                    print(response.status_code, response.url)
                else:
                    print("Request was not redirected")
                image = self.data_loader.image_transform(Image.open(requests.get(url, stream=True, timeout=50).raw).convert('RGB'))
            elif type(url) == str:
                image = self.data_loader.image_transform(Image.open(url).convert('RGB'))
            else:
                image = self.data_loader.image_transform(url)
            images.append(image)
        image = torch.stack([row for row in images])
        with torch.no_grad():
            ims = F.normalize(self.model.project(self.model.model.encode_image(image)), dim=1)
        return ims


if __name__ == "__main__":
    import glob
    X = Encoder()
    temp = []
    x = X.images(["a.png"])
    print (x)
    exit()
