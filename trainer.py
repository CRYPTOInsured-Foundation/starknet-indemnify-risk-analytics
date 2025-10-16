# trainer.py
import os
import joblib
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import torchvision.models as models

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb
import pandas as pd
from preprocess import VisualDataset, train_transform, val_transform, DOWNLOAD_INDEX, LABELS_CSV
from features import build_features_for_item
from pathlib import Path

IMAGE_MODEL_PATH = "models/image_model.pth"
TABULAR_MODEL_PATH = "models/tabular_model.joblib"

def train_image_classifier(batch_size=16, epochs=5, device='cuda' if torch.cuda.is_available() else 'cpu'):
    ds = VisualDataset(DOWNLOAD_INDEX, LABELS_CSV, transform=train_transform, label_col='acceptable_risk')
    val_size = max(1, int(0.1*len(ds)))
    train_size = len(ds) - val_size
    train_ds, val_ds = random_split(ds, [train_size, val_size])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=2)

    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 1)  # binary
    model = model.to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for imgs, labels, _ in train_loader:
            imgs = imgs.to(device)
            labels = labels.float().unsqueeze(1).to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs} loss={running_loss/len(train_loader):.4f}")

        # validation
        model.eval()
        preds, labs = [], []
        with torch.no_grad():
            for imgs, labels, _ in val_loader:
                imgs = imgs.to(device)
                outputs = model(imgs)
                probs = torch.sigmoid(outputs).cpu().numpy().ravel()
                preds.extend(probs.tolist())
                labs.extend(labels.tolist())
        try:
            auc = roc_auc_score(labs, preds)
            print("Val AUC:", auc)
        except Exception:
            pass

    Path("models").mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), IMAGE_MODEL_PATH)
    print("Saved image model to", IMAGE_MODEL_PATH)

def collect_tabular_dataset(index_csv=DOWNLOAD_INDEX, labels_csv=LABELS_CSV, claims_csv="data/claims.csv"):
    idx = pd.read_csv(index_csv)
    labels = pd.read_csv(labels_csv).set_index('id')
    rows = []
    for i, rec in idx.iterrows():
        id_ = rec['id']
        # metadata (you can expand)
        meta = {'proposer_id': rec.get('id'), 'address': rec.get('url')}  # replace with real metadata if present
        feat = build_features_for_item(meta, claims_csv=claims_csv)
        label_row = labels.loc[id_] if id_ in labels.index else pd.Series({'fraudulent':0,'acceptable_risk':1})
        feat['id'] = id_
        feat['fraudulent'] = int(label_row.get('fraudulent', 0))
        feat['acceptable_risk'] = int(label_row.get('acceptable_risk', 1))
        rows.append(feat)
    df = pd.DataFrame(rows).set_index('id')
    return df

def train_tabular_model(df: pd.DataFrame, target_col='fraudulent'):
    X = df.drop(columns=['fraudulent','acceptable_risk'])
    y = df[target_col]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)
    model = xgb.XGBClassifier(n_estimators=200, max_depth=6, use_label_encoder=False, eval_metric='auc')
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_val)[:,1]
    print("Tabular val AUC:", roc_auc_score(y_val, preds))
    joblib.dump(model, TABULAR_MODEL_PATH)
    print("Saved tabular model to", TABULAR_MODEL_PATH)

if __name__ == "__main__":
    # Quick run
    train_image_classifier(epochs=3)
    df = collect_tabular_dataset()
    train_tabular_model(df)
