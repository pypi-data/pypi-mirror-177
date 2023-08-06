# Om Simple Encoder
Om Simple Encoder is to fintune the query encoder. Currently it includes only query image encoder. 

# Install
```
pip install om_simple_encoder
```

# How to start training
```
python train.py --img_dir {image_root_path} --data {data json} --num_workers=15 --gpus=1 --batch_size=64 
```

# Data Format
```json
[ {"key1": ["image1.jpg","image2.jpg"], "key2":  ["image1.jpg","image2.jpg"]},...]
```

# Demo prediction
```python
from om_simple_encoder.encoder import Encoder
h_enc = Encoder("brand_model_v1.ckpt")
encoded_embeddings = h_enc.images(["a.png"])
print (encoded_embeddings)
```
# Demo Train
```python
from om_simple_encoder import train 

if __name__ == '__main__':
    train.start_train(model_type="resnet50", img_dir="/mnt/soco1/brands", data="brands.json", batch_size=64)
```
