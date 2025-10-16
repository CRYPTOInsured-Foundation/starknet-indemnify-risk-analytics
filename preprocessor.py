# preprocess.py
import os
import csv
from pathlib import Path
from PIL import Image
from torchvision import transforms
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd

DOWNLOAD_INDEX = Path("downloads/download_index.csv")
LABELS_CSV = Path("data/labels.csv")  # You maintain this: id, acceptable_risk(0/1), fraudulent(0/1), other metadata...
PROCESSED_DIR = Path("downloads/processed_images")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# transforms
train_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

class VisualDataset(Dataset):
    def __init__(self, index_csv, labels_csv, transform=None, label_col="acceptable_risk"):
        self.index = pd.read_csv(index_csv)
        self.labels = pd.read_csv(labels_csv).set_index('id')
        self.transform = transform
        self.label_col = label_col

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        rec = self.index.iloc[idx]
        local_path = rec['local_path']
        id_ = rec['id']
        img = Image.open(local_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        # label may not exist -> default 0
        label = int(self.labels.loc[id_][self.label_col]) if id_ in self.labels.index else 0
        return img, label, id_

def build_simple_image_dataset(index_csv=DOWNLOAD_INDEX, labels_csv=LABELS_CSV):
    # just a helper to verify and create processed copies if needed
    idx = pd.read_csv(index_csv)
    labels = pd.read_csv(labels_csv).set_index('id')
    for i, row in idx.iterrows():
        p = Path(row['local_path'])
        if not p.exists():
            continue
        out_p = PROCESSED_DIR / p.name
        if out_p.exists(): continue
        img = Image.open(p).convert('RGB')
        img = img.resize((224,224))
        img.save(out_p, quality=85)
