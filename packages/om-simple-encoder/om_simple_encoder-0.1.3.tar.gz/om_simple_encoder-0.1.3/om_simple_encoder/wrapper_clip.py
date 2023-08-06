import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import numpy as np
import math
import yaml
import copy
from .model import CLIP

import clip

class CLIPWrapper(pl.LightningModule):
    def __init__(self,
                 model_name: str,
                 config: dict,
                 minibatch_size: int
                 ):
        """A lightning wrapper for a CLIP model as specified in the paper.

        Args:
            model_name (str): A case sensitive visual model name.
            config (dict): A dictionary containing the CLIP instantiation parameters.
        """
        super().__init__()

        self.model_name = model_name
        self.model = CLIP(**config)
        self.minibatch_size = minibatch_size
        self.isViT = 'ViT' in self.model_name

        self.automatic_optimization = False

    def forward(self, image, text):
        return self.model(image, text)

    # Training loss: https://github.com/openai/CLIP/issues/83
    # Mini-batching thanks to https://github.com/crowsonkb / https://twitter.com/RiversHaveWings
    # Multi-GPU support: https://github.com/MicPie/clasp
    def training_step(self, train_batch, idx):
        # get optimizers and scheduler
        optimizer = self.optimizers()

        image, text = train_batch
        n = math.ceil(len(image) // self.minibatch_size)
        image_mbs = torch.chunk(image, n)
        text_mbs = torch.chunk(text, n)

        # calculate original statistics
        with torch.no_grad():
            ims = [F.normalize(self.model.encode_image(im), dim=1) for im in image_mbs]
            txt = [F.normalize(self.model.encode_text(t), dim=1) for t in text_mbs]
            # gather from all GPUs
            ims = self.all_gather(torch.cat(ims))
            txt = self.all_gather(torch.cat(txt))

            if len(ims.shape) == 3:
                ims = list(ims)
                txt = list(txt)
            else:
                ims = [ims]
                txt = [txt]

            image_logits = torch.cat(ims) @ torch.cat(txt).t() * self.model.logit_scale.exp()
            ground_truth = torch.arange(len(image_logits)).type_as(image_logits).long()
            loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(image_logits.t(), ground_truth)).div(2)
            acc_i = (torch.argmax(image_logits, 1) == ground_truth).sum()
            acc_t = (torch.argmax(image_logits, 0) == ground_truth).sum()
            self.log_dict({'loss': loss / len(ims), 'acc': (acc_i + acc_t) / 2 / len(image) / len(ims)}, prog_bar=True)

        if isinstance(optimizer, list):
            optimizer = optimizer[0]
        optimizer.zero_grad()

        # image loss
        for j, mb in enumerate(image_mbs):
            images_tmp = copy.deepcopy(ims)
            images_tmp[self.global_rank][j*self.minibatch_size:(j+1)*self.minibatch_size] = F.normalize(self.model.encode_image(mb), dim=1)
            image_logits = torch.cat(images_tmp) @ torch.cat(txt).t() * self.model.logit_scale.exp()
            ground_truth = torch.arange(len(image_logits)).type_as(image_logits).long()
            loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(image_logits.t(), ground_truth))/2
            self.manual_backward(loss)

        # text loss
        for j, mb in enumerate(text_mbs):
            text_tmp = copy.deepcopy(txt)
            text_tmp[self.global_rank][j*self.minibatch_size:(j+1)*self.minibatch_size] = F.normalize(self.model.encode_text(mb), dim=1)
            image_logits = torch.cat(ims) @ torch.cat(text_tmp).t() * self.model.logit_scale.exp()
            loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(image_logits.t(), ground_truth))/2
            self.manual_backward(loss)

        optimizer.step()
        lr_scheduler = self.lr_schedulers()
        lr_scheduler.step()
        self.model.logit_scale.data.clamp_(-np.log(100), np.log(100))

    def validation_step(self, val_batch, idx):
        image, text = val_batch
        image_logits, text_logits = self.forward(image, text)
        ground_truth = torch.arange(len(image_logits))
        loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(text_logits, ground_truth)).div(2)
        self.log('val_loss', loss)

    def configure_optimizers(self):
        lr = {
            "RN50": 5e-4,
            "RN101": 5e-4,
            "RN50x4": 5e-4,
            "RN50x16": 4e-4,
            "RN50x64": 3.6e-4,
            "ViT-B/32": 5e-4,
            "ViT-B/16": 5e-4,
            "ViT-L/14": 4e-4,
            "ViT-L/14-336px": 2e-5
        }[self.model_name]

        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=lr,
            betas=(
                0.9,
                0.98 if self.isViT else 0.999
            ),
            eps=1e-6 if self.isViT else 1e-8,
            weight_decay=0.2
        )

        # TODO Watch: https://github.com/openai/CLIP/issues/107
        lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer,
            T_0=2000
        )

        return {'optimizer': optimizer, 'lr_scheduler': lr_scheduler}


class CustomCLIPWrapper(CLIPWrapper):
    def __init__(self,
                 image_encoder,
                 minibatch_size,
                 learning_rate=3e-3,
                 kl_coeff=1.0,
                 avg_word_embs=False
                 ):
        with open('om_simple_encoder/configs/RN.yaml') as fin:
            config = yaml.safe_load(fin)['RN50']
        super().__init__('RN50', config, minibatch_size)
        del self.model.visual
        del self.model.transformer
        self.model.visual = image_encoder
        self.sketch_encoder = image_encoder
        device = "cuda" if torch.cuda.is_available() else "cpu"
        with torch.no_grad():
            self.image_encoder,self.preprocess = clip.load("ViT-B-16", device=device)

        self.learning_rate = learning_rate
        self.avg_word_embs = avg_word_embs
        self.sink_temp = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
        self.fc_sketch = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
        )

        # init self-distillation model
        self.teacher = copy.deepcopy(self.model)
        self.kl_coeff = kl_coeff
        #clip.model.convert_weights(self.image_encoder)


    def training_step(self, train_batch, idx):
        # get optimizers and scheduler
        optimizer = self.optimizers()

        image, text = train_batch
        n = math.ceil(len(image) // self.minibatch_size)

        image_mbs = torch.chunk(image, n)
        n = math.ceil(len(image) // self.minibatch_size)
        text_mbs = torch.chunk(text, n)
        print (text_mbs)

        # calculate original statistics
        with torch.no_grad():
            ims = [F.normalize(self.image_encoder.encode_image(im), dim=1) for im in image_mbs]
            txt = [F.normalize(self.fc_sketch(torch.tensor(self.sketch_encoder.encode(im)).to('cuda')), dim=1) for im in text_mbs]
            # gather from all GPUs
            ims = self.all_gather(torch.cat(ims))
            txt = self.all_gather(torch.cat(txt))

            if len(ims.shape) == 3:
                ims = list(ims)
                txt = list(txt)
            else:
                ims = [ims]
                txt = [txt]

            image_logits_notemp = torch.cat(ims) @ torch.cat(txt).t()
            image_logits = image_logits_notemp * self.model.logit_scale.exp()
            ground_truth = torch.arange(len(image_logits)).type_as(image_logits).long()
            loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(image_logits.t(), ground_truth)).div(2)
            acc_i = (torch.argmax(image_logits, 1) == ground_truth).sum()
            acc_t = (torch.argmax(image_logits, 0) == ground_truth).sum()
            # calculate teacher
            teacher_ims = [F.normalize(self.image_encoder.encode_image(im), dim=1) for im in image_mbs]
            teacher_txt = [F.normalize(self.fc_sketch(torch.tensor(self.sketch_encoder.encode(t)).to('cuda')), dim=1) for t in text_mbs]
            teacher_ims = self.all_gather(torch.cat(teacher_ims))
            teacher_txt = self.all_gather(torch.cat(teacher_txt))

            if len(teacher_ims.shape) == 3:
                teacher_ims = list(teacher_ims)
                teacher_txt = list(teacher_txt)
            else:
                teacher_ims = [teacher_ims]
                teacher_txt = [teacher_txt]

            sim_ii, sim_tt, sim_it, sim_ti = self.compute_similarities(torch.cat(teacher_ims), torch.cat(teacher_txt))

            # optimal transport
            img_cost = - (sim_ii + sim_tt + sim_it)
            txt_cost = - (sim_ii + sim_tt + sim_ti)
            img_target = self.sinkhorn(img_cost)
            txt_target = self.sinkhorn(txt_cost)
            loss += (F.kl_div(image_logits_notemp * self.sink_temp, img_target) + F.kl_div(image_logits_notemp.t() * self.sink_temp, txt_target)) / 2 * self.kl_coeff
            self.log_dict({'loss': loss / len(ims), 'acc': (acc_i + acc_t) / 2 / len(image) / len(ims)}, prog_bar=True)
            self.logger.log_metrics({"loss": float(loss) / len(ims), "acc": float(acc_i + acc_t) / 2 / len(image) / len(ims)})

        if isinstance(optimizer, list):
            optimizer = optimizer[0]
        optimizer.zero_grad()

        for param in self.image_encoder.parameters():
            param.requires_grad_(False)

        # text loss
        for j, mb in enumerate(text_mbs):
            text_tmp = copy.deepcopy(txt)
            text_tmp[self.global_rank][j*self.minibatch_size:(j+1)*self.minibatch_size] = F.normalize(self.fc_sketch(torch.tensor(self.sketch_encoder.encode(mb)).to('cuda')), dim=1)
            image_logits_notemp = torch.cat(ims) @ torch.cat(text_tmp).t()
            image_logits = image_logits_notemp * self.model.logit_scale.exp()
            loss = (F.cross_entropy(image_logits, ground_truth) + F.cross_entropy(image_logits.t(), ground_truth))/2
            loss += (F.kl_div(image_logits_notemp * self.sink_temp, img_target) + F.kl_div(image_logits_notemp.t() * self.sink_temp, txt_target)) / 2 * self.kl_coeff
            self.manual_backward(loss)
        optimizer.step()
        lr_scheduler = self.lr_schedulers()
        lr_scheduler.step()
        self.model.logit_scale.data.clamp_(-np.log(100), np.log(100))
        self.sink_temp.data.clamp_(-np.log(100), np.log(100))
        self.update_teacher()

    def encode_text(self, inputs, teacher=False):
        return self.teacher.transformer(**inputs)[1] if teacher else self.model.transformer(**inputs)[1]

    def compute_similarities(self, I_emb, T_emb):
        sim_ii, sim_tt = I_emb @ I_emb.t(), T_emb @ T_emb.t()
        sim_it, sim_ti = I_emb @ T_emb.t(), T_emb @ I_emb.t()
        return sim_ii, sim_tt, sim_it, sim_ti

    def update_teacher(self):
        for teacher, student in zip(self.teacher.parameters(), self.model.parameters()):
            teacher.data.copy_(self.ema(teacher.data, student.data))

    def ema(self, s, t):
        return s * (1 - 0.999) + t * 0.999

    def forward(self, images, text):
        logits = F.normalize(self.image_encoder.encode_image(images), dim=1) @ F.normalize(self.model.encode_text(text), dim=1).t() * self.model.logit_scale.exp()
        return logits, logits.t()

    # Sourced from: https://github.com/facebookresearch/swav/blob/5e073db0cc69dea22aa75e92bfdd75011e888f28/main_swav.py#L354
    def sinkhorn(self, out):
        Q = torch.exp(out / 0.05).t()  # Q is K-by-B for consistency with notations from our paper
        B = Q.shape[1]  # number of samples to assign
        K = Q.shape[0]  # how many prototypes

        # make the matrix sums to 1
        sum_Q = torch.sum(Q)
        Q /= sum_Q

        for it in range(3):
            # normalize each row: total weight per prototype must be 1/K
            sum_of_rows = torch.sum(Q, dim=1, keepdim=True)
            Q /= sum_of_rows
            Q /= K

            # normalize each column: total weight per sample must be 1/B
            Q /= torch.sum(Q, dim=0, keepdim=True)
            Q /= B

        Q *= B  # the colomns must sum to 1 so that Q is an assignment
        return Q.t()

    def configure_optimizers(self):
        lr = self.learning_rate

        optimizer = torch.optim.SGD(
            self.parameters(),
            lr=lr,
            momentum=0.9
        )

        # TODO Watch: https://github.com/openai/CLIP/issues/107
        lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer,
            T_0=2000
        )

        return {'optimizer': optimizer, 'lr_scheduler': lr_scheduler}
