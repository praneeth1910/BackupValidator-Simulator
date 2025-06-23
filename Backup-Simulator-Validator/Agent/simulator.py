import os
import argparse
import hashlib
import json
import shutil
from datetime import datetime

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'Snapshots')
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def calculate_file_metadata(path):
    try:
        stat = os.stat(path)
        with open(path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return {
            'path': path,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'inode': stat.st_ino,
            'checksum': file_hash,
        }
    except Exception as e:
        return {
            'path': path,
            'error': str(e)
        }

def scan_directory(directory):
    file_metadata = []
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            meta = calculate_file_metadata(full_path)
            file_metadata.append(meta)
    return file_metadata

def save_snapshot(snapshot, output_path='snapshot.json'):
    with open(output_path, 'w') as f:
        json.dump(snapshot, f, indent=4)

    # Save a copy in the Snapshots/ directory
    base_filename = os.path.basename(output_path)
    tracked_path = os.path.join(SNAPSHOT_DIR, base_filename)
    if output_path != tracked_path:
        shutil.copy2(output_path, tracked_path)

def main():
    parser = argparse.ArgumentParser(description="Backup Validator CLI Agent")
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('--upload', action='store_true', help='Upload snapshot to API')
    parser.add_argument('--compare', action='store_true', help='Compare with previous snapshot')
    parser.add_argument('--output', default='snapshot.json', help='Path to save snapshot JSON')

    args = parser.parse_args()

    print(f"Scanning directory: {args.directory}")
    files = scan_directory(args.directory)

    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'directory': args.directory,
        'files': files
    }

    save_snapshot(snapshot, args.output)
    print(f"Snapshot saved to {args.output}")

    if args.upload:
        print("[TODO] Upload to API endpoint")

    if args.compare:
        print("[TODO] Compare with previous snapshot")

if __name__ == '__main__':
    main()
