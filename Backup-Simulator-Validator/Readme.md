# 📘 Project Documentation: Smart Backup Validator & Simulator

## Overview

This project is a robust backup snapshot tracking system that operates via a CLI agent and a cloud-based FastAPI backend. It supports:

* Real-time or scheduled scanning of backupsets
* Snapshot generation, storage, and upload
* Backupset validation and history tracking
* Designed for extensibility with databases, cloud auth, and efficient diffing

---

## 🔧 CLI Agent

### Key Features:

* Scans files/directories defined in a user-provided **backupset file**
* Generates metadata-rich snapshot JSON files
* Stores them under `Snapshots/<machine_id>/<backupset_name>/<timestamp>.json`
* Posts snapshots to the server (optionally)

### Snapshot Structure (JSON)

```json
{
  "snapshot_id": "<optional-sha256>",
  "timestamp": "2025-06-23T10:33:21",
  "machine_id": "devbox-001",
  "backupset_name": "project-data",
  "summary": {
    "file_count": 1243,
    "total_size": 89072342,
    "error_count": 2
  },
  "files": [
    {
      "path": "/home/user/foo.txt",
      "size": 1024,
      "mtime": 1729493434.33,
      "inode": 123456,
      "checksum": "abc123...",
      "error": null
    }
  ]
}
```

---

## 🌐 API Backend (FastAPI)

### RESTful Endpoints

| Method | Endpoint                                                     | Purpose                           |
| ------ | ------------------------------------------------------------ | --------------------------------- |
| GET    | `/machines/{machine_id}/backupsets`                          | List backupsets on machine        |
| GET    | `/machines/{machine_id}/backupsets/{set_name}`               | List snapshots in that backupset  |
| GET    | `/machines/{machine_id}/backupsets/{set_name}/latest`        | Get latest snapshot               |
| GET    | `/machines/{machine_id}/backupsets/{set_name}/{snapshot_id}` | Get specific snapshot             |
| GET    | `/machines/{machine_id}/backupsets/{set_name}/query?...`     | Filter snapshots by time/hash/etc |
| POST   | `/machines/{machine_id}/backupsets/{set_name}/validate`      | Validate/reserve backupset name   |
| POST   | `/machines/{machine_id}/backupsets/{set_name}`               | Upload a new snapshot             |

### DB Schema Sketch

#### `backupsets`

```sql
machine_id TEXT,
backupset_name TEXT,
created_at TIMESTAMP,
description TEXT,
PRIMARY KEY (machine_id, backupset_name)
```

#### `snapshots`

```sql
snapshot_id TEXT,
timestamp TIMESTAMP,
machine_id TEXT,
backupset_name TEXT,
summary JSONB,
files JSONB
```

---

## 🔐 Auth (Future)

* Add user management (username + API key)
* Restrict machines to owner user
* Protect endpoints with header auth (`X-API-Key` or JWT)

---

## 📌 Future Enhancements

* Snapshot ID hashing
* Efficient diffing with historical snapshots
* Duplicate file detection by hash
* Time-range querying & version rollback
* Web dashboard integration

---

## 🚀 Next Milestone

* [ ] Add backupset validation API
* [ ] Create registry tables/models
* [ ] Modify CLI agent to validate before snapshot upload
* [ ] Unit tests for snapshot structure and endpoint behavior
