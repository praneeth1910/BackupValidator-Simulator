import os
import json
import hashlib
import argparse
from datetime import datetime

def calculate_file_metadata(path):
    try:
        stat = os.stat(path)
        with open(path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return {
            'path': path,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'checksum': file_hash,
            'inode': stat.st_ino,
        }
    except Exception as e:
        return {
            'path': path,
            'error': str(e)
        }

def scan_directory(directory):
    file_metadata = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            meta = calculate_file_metadata(full_path)
            file_metadata.append(meta)
    return file_metadata

def save_snapshot(snapshot, output_path="snapshot.json"):
    with open(output_path, 'w') as f:
        json.dump(snapshot, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Backup Simulator Validator Agent")
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('--upload', action='store_true', help='Upload snapshot to API')
    parser.add_argument('--compare', action='store_true', help='Compare snapshot with previous one')
    parser.add_argument('--output', default="snapshot.json", type=str, help='Path to save snapshot JSON')

    args = parser.parse_args()

    dirs = args.directory
    timestamp = datetime.now().isoformat()
    files = scan_directory(dirs)


    snapshot = {
        "timestamp": timestamp,
        "directory": dirs,
        "files": files,
        }
    
    save_snapshot(snapshot, args.output)
    print(f"Snapshot saved to {args.output}")

    if args.upload:
        print("Uploading snapshot to API...")
        
    if args.compare:
        print("Comparing snapshot with previous one...")

    print(f"Scanning directory: {args.directory}")
    print("Starting Backup Simulator Validator Agent...")

if __name__ == "__main__":
    main()