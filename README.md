# 🚀 Smart Backup Validator & Simulator for Linux Systems

A developer-focused system tool that helps simulate, validate, and track backup integrity for Linux file systems. This project empowers devs and sysadmins to build resilient backup workflows through file metadata analysis, API-driven validation, and system-aware infrastructure practices.

---

## 🔧 Project Goals

1. **Monitor System File State**
   - Traverse Linux directories and collect file metadata (size, mtime, inode, checksum)
   - Support filters and CLI arguments for flexible scanning

2. **Store & Version Backup Snapshots**
   - Upload snapshots to a FastAPI backend
   - Store in PostgreSQL with timestamped versioning

3. **On-Demand Access to Snapshots**
   - Expose REST APIs for:
     - Latest snapshot
     - Historical views
     - File-specific search

4. **Comparison & Drift Detection**
   - CLI agent compares local scan to last known snapshot
   - Highlights missing, added, or modified files
   - Optionally detects hash mismatch or corruption

5. **Deployment & Infra Optimizations**
   - Fully containerized via Docker & Compose
   - CI/CD pipeline for linting, tests, and builds
   - Cloud deployment guides for AWS/GCP (free-tier friendly)

6. **(Bonus) Failure Simulation**
   - Test backup failure modes (e.g., lost files, missed updates)
   - Helps validate alerting and client logic

7. **(Optional) Alerting & Monitoring**
   - Webhook or CLI alerts on drift or snapshot failure
   - Prometheus metrics for backup agent status

---

## 💡 Motivation

Backups silently fail more often than we realize — files drift, schedules break, integrity assumptions go unchecked. This project exists to build **developer tooling** around backup observability and make validation an active part of system health.

---

## 🧱 Tech Stack

| Component       | Tech Used                          |
|------------------|------------------------------------|
| CLI Agent        | Python (argparse, pathlib, hashlib)|
| Backend API      | FastAPI + PostgreSQL               |
| Containerization | Docker, Docker Compose             |
| CI/CD            | GitHub Actions                     |
| Deployment       | GCP / AWS Free Tier (VM or Docker) |
| Optional Metrics | Prometheus + Grafana               |

---

## 📁 Folder Structure (Planned)

smart-backup-validator/
├── agent/ # Python CLI backup simulator
│ └── simulator.py
├── backend/
│ ├── main.py # FastAPI app
│ ├── models.py
│ └── routes/
├── snapshots/ # Sample scan outputs / test fixtures
├── tests/ # Unit/integration tests
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.agent
└── README.md

---

## 🔄 Planned API Endpoints

| Method | Endpoint                     | Purpose                               |
|--------|------------------------------|---------------------------------------|
| GET    | `/backupsets/{id}`           | Get latest snapshot                   |
| POST   | `/backupsets/{id}`           | Upload new snapshot                   |
| GET    | `/backupsets/{id}/history`   | List past snapshots                   |
| GET    | `/backupsets/{id}/diff`      | Compare with previous snapshot        |

---

## ✅ How to Use (Eventually)

```bash
# Scan a folder and upload snapshot
$ python3 simulator.py /home/user/data --upload

# Compare current scan to last backup
$ python3 simulator.py /home/user/data --compare

# Get snapshot from API
$ curl http://localhost:8000/backupsets/my-machine


---
## 🏗️ Architecture Overview

          +--------------------+
          |   Linux System A   |
          | (User Workstation) |
          +--------------------+
                   |
                   | (1) Scan filesystem
                   |     & collect metadata
                   v
          +--------------------+
          |   CLI Agent        |  ← Python (simulator.py)
          | - Hashing          |
          | - Inode tracking   |
          | - Snapshot version |
          +--------------------+
                   |
                   | (2) Upload snapshot
                   v
        ┌─────────────────────────────┐
        │        Backend API          │  ← FastAPI
        │   - Receives snapshots      │
        │   - Provides diff/compare   │
        │   - Manages snapshot history│
        └────────────┬────────────────┘
                     |
                     | (3) Store data
                     v
            +-------------------+
            |   PostgreSQL DB   |
            | - snapshot table  |
            | - file meta table |
            +-------------------+
                     |
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
(4) Comparison API        (5) Alert/Drift Checks
   /backupsets/diff           (CLI or dashboard)

## Deployement
+----------------------------+
|        Docker Host         |
+----------------------------+
|                            |
|  [FastAPI Container]       |
|  [PostgreSQL Container]    |
|  [Optional: Prometheus]    |
|                            |
+----------------------------+

+----------------------------+
|  Linux Client Machines     |
+----------------------------+
|  CLI agent in user space   |
|  Runs via cron/systemd     |
+----------------------------+

[ All containers managed via Docker Compose ]
