# fetcher.py
import os
import csv
import requests
from tqdm import tqdm
from pathlib import Path
import cv2
import shutil
from urllib.parse import urlparse

DOWNLOAD_DIR = Path("downloads")
IMAGES_DIR = DOWNLOAD_DIR / "images"
FRAMES_DIR = DOWNLOAD_DIR / "video_frames"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, dest_path, timeout=30):
    try:
        r = requests.get(url, stream=True, timeout=timeout)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return True
    except Exception as e:
        print(f"download error {url}: {e}")
        return False

def ext_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    if '.' in basename:
        return basename.split('.')[-1].lower()
    return ''

def is_video_ext(ext):
    return ext in ('mp4', 'mov', 'avi', 'mkv', 'webm')

def extract_frames(video_path: Path, out_dir: Path, step_seconds=2):
    """Extract frames every step_seconds seconds."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("Cannot open video:", video_path)
        return []
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration = total_frames / fps if fps else 0
    frames = []
    frame_idx = 0
    success, frame = cap.read()
    while success:
        time_sec = frame_idx / fps if fps else 0
        if int(time_sec) % step_seconds == 0:
            out_file = out_dir / f"{video_path.stem}_frame_{frame_idx}.jpg"
            cv2.imwrite(str(out_file), frame)
            frames.append(str(out_file))
        frame_idx += 1
        success, frame = cap.read()
    cap.release()
    return frames

def process_urls(input_csv="data/raw_urls.csv"):
    """
    expected CSV columns: id,url,type
    type in ("image","video") or guessed by extension
    """
    records = []
    with open(input_csv, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            records.append(row)

    results = []
    for r in tqdm(records):
        id_ = r.get('id') or r.get('url')
        url = r['url']
        typ = r.get('type')
        ext = ext_from_url(url)
        guessed_video = typ == 'video' or (not typ and is_video_ext(ext))
        if guessed_video:
            fname = f"{id_}.{ext or 'mp4'}"
            dest = FRAMES_DIR / fname
            ok = download_file(url, dest)
            if not ok:
                continue
            # extract frames
            out_sub = FRAMES_DIR / id_
            frames = extract_frames(dest, out_sub, step_seconds=2)
            for f in frames:
                results.append({'id': id_, 'url': url, 'local_path': f, 'type': 'frame'})
            # optionally remove video to save space
            try:
                dest.unlink()
            except Exception:
                pass
        else:
            # image
            fname = f"{id_}.{ext or 'jpg'}"
            dest = IMAGES_DIR / fname
            ok = download_file(url, dest)
            if not ok: continue
            results.append({'id': id_, 'url': url, 'local_path': str(dest), 'type': 'image'})

    # write a dataset CSV mapping id -> local_path
    out_csv = DOWNLOAD_DIR / "download_index.csv"
    keys = ['id','url','local_path','type']
    with open(out_csv, 'w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        for rec in results:
            writer.writerow(rec)
    print("done:", out_csv)

if __name__ == "__main__":
    process_urls()
