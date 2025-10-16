# predict.py
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import joblib
import numpy as np
from pathlib import Path
from preprocess import val_transform
from features import build_features_for_item
import pandas as pd
from trainer import IMAGE_MODEL_PATH, TABULAR_MODEL_PATH

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_image_model(path=IMAGE_MODEL_PATH):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device).eval()
    return model

def image_predict(model, image_path):
    img = Image.open(image_path).convert('RGB')
    inp = val_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(inp)
        prob = torch.sigmoid(out).cpu().numpy().ravel()[0]
    return float(prob)

def tabular_predict(model, item_meta, claims_csv="data/claims.csv"):
    feat = build_features_for_item(item_meta, claims_csv=claims_csv)
    # model expects columns in training order - in production, persist vectorizer
    X = pd.DataFrame([feat.values], columns=feat.index)
    proba = model.predict_proba(X)[:,1][0]
    return float(proba)

def combined_score(image_p, tabular_p, w_image=0.4, w_tabular=0.6):
    return float(w_image*image_p + w_tabular*tabular_p)

if __name__ == "__main__":
    img_model = load_image_model()
    tab_model = joblib.load(TABULAR_MODEL_PATH)
    # sample item
    sample_image = "downloads/images/123.jpg"
    sample_meta = {'proposer_id': '123', 'address': 'Ikeja Lagos'}
    img_p = image_predict(img_model, sample_image)
    tab_p = tabular_predict(tab_model, sample_meta)
    final = combined_score(img_p, tab_p)
    print("image_p", img_p, "tab_p", tab_p, "final", final)
