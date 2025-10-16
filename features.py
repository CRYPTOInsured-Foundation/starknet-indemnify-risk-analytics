# features.py
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from sentence_transformers import SentenceTransformer
import feedparser
import os
from pathlib import Path
from typing import Dict

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_MODEL = SentenceTransformer(MODEL_NAME)

def load_claim_history(claims_csv):
    """claims_csv columns: claimant_id,claim_id,amount,status,date,location"""
    return pd.read_csv(claims_csv, parse_dates=['date'])

def claimant_features(claims_df: pd.DataFrame, claimant_id):
    df = claims_df[claims_df['claimant_id'] == claimant_id]
    return {
        "total_claims": int(len(df)),
        "sum_claim_amount": float(df['amount'].sum()) if not df.empty else 0.0,
        "avg_claim_amount": float(df['amount'].mean()) if not df.empty else 0.0,
        "num_approved": int((df['status']=='approved').sum()),
        "num_rejected": int((df['status']=='rejected').sum()),
    }

def geocode_location(lat=None, lon=None, address=None):
    # Use geopy Nominatim or your favourite API (rate-limited). For production use paid geocoding.
    geolocator = Nominatim(user_agent="risk-analytics")
    try:
        if address:
            loc = geolocator.geocode(address, timeout=10)
            return (loc.latitude, loc.longitude) if loc else (None,None)
        elif lat and lon:
            loc = geolocator.reverse((lat, lon), timeout=10)
            return (lat, lon)
    except Exception as e:
        print("geocode error:", e)
    return (None, None)

def news_embeddings_for_location(location_str, max_items=5):
    """
    Quick news fetch using feedparser from Google News RSS (no API key).
    location_str: e.g. 'Lagos' or 'Ikeja'
    """
    query = f"https://news.google.com/rss/search?q={location_str}"
    feed = feedparser.parse(query)
    texts = []
    for entry in feed.entries[:max_items]:
        summary = entry.get('summary') or entry.get('title') or ''
        texts.append(summary)
    if not texts:
        return np.zeros(EMBED_MODEL.get_sentence_embedding_dimension()).astype(float)
    emb = EMBED_MODEL.encode(texts, show_progress_bar=False)
    # average
    return np.mean(emb, axis=0)

def build_features_for_item(item_meta, claims_csv="data/claims.csv"):
    """
    item_meta: dict with keys e.g. claimant_id/proposer_address, lat, lon, address, id
    returns a pandas.Series of features
    """
    claims = load_claim_history(claims_csv)
    claimant_id = item_meta.get('claimant_id') or item_meta.get('proposer_id')
    cf = claimant_features(claims, claimant_id) if claimant_id else {"total_claims":0,"sum_claim_amount":0,"avg_claim_amount":0,"num_approved":0,"num_rejected":0}
    lat, lon = None, None
    if 'lat' in item_meta and 'lon' in item_meta:
        lat, lon = item_meta.get('lat'), item_meta.get('lon')
    elif 'address' in item_meta:
        lat, lon = geocode_location(address=item_meta.get('address'))
    # risk features from location (simple): distance to coast, population density etc would be better — placeholders
    location_embedding = news_embeddings_for_location(item_meta.get('address', ''))
    features = {
        **cf,
        "lat": lat or 0.0,
        "lon": lon or 0.0,
    }
    # append news emb vector as flattened feature names
    for i, v in enumerate(location_embedding):
        features[f"news_emb_{i}"] = float(v)
    return pd.Series(features)
