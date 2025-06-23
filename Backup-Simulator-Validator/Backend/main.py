from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Tuple, List

from models import BackupsetInDB, SnapshotInDB

app = FastAPI(
    title="Backup Validator API",
    description="API backend for managing backupsets and snapshots",
    version="0.1.0",
)

# In-memory registry for backupset validation only (temporary mock)
backupsets_registry: dict[Tuple[str, str], BackupsetInDB] = {}
snapshots_registry: dict[Tuple[str, str, str], SnapshotInDB] = {}

@app.get("/")
async def root():
    return {"message": "Backup Validator API is running"}

@app.post("/machines/{machine_id}/backupsets/{backupset_name}/validate", status_code=200)
async def validate_backupset(machine_id: str, backupset_name: str) -> dict:
    key = (machine_id, backupset_name)
    if key in backupsets_registry:
        raise HTTPException(
            status_code=409,
            detail=f"Backupset '{backupset_name}' already exists for machine '{machine_id}'."
        )
    new_backupset = BackupsetInDB(
        machine_id=machine_id,
        backupset_name=backupset_name,
        created_at=datetime.utcnow(),
        id=len(backupsets_registry) + 1
    )
    backupsets_registry[key] = new_backupset
    return {"message": "Backupset name validated and registered."}


@app.get("/machines/{machine_id}/backupsets")
async def list_backupsets(machine_id: str) -> List[BackupsetInDB]:
    result = [
        backupset for (mid, _), backupset in backupsets_registry.items() if mid == machine_id
    ]
    return result

@app.get("/machines/{machine_id}/backupsets/{backupset_name}")
async def list_snapshots(machine_id: str, backupset_name: str) -> list[SnapshotInDB]:
    result = [
        snap for (mid, bname, _), snap in snapshots_registry.items() if mid == machine_id and bname == backupset_name
    ]
    
    result.sort(key = lambda s: s.timestamp, reverse=True)
    return result

@app.get("/machines/{machine_id}/backupsets/{backupset_name}/latest")
async def get_latest_snapshot(machine_id: str, backupset_name: str) -> SnapshotInDB:
    filtered = [
        s for (mid, bname, _), s in snapshots_registry.items()
        if mid == machine_id and bname == backupset_name
    ]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No snapshots found for backupset '{backupset_name}' on machine '{machine_id}'."
        )
    latest = max(filtered, key=lambda s: s.timestamp)
    
    return latest

@app.get("/machines/{machine_id}/backupsets/{backupset_name}/{snapshot_id}")
async def get_snapshot_by_id(machine_id: str, backupset_name: str, snapshot_id: str) -> SnapshotInDB:
    snap_key = (machine_id, backupset_name, snapshot_id)

    if snap_key not in snapshots_registry:
        raise HTTPException(
            status_code=404,
            detail=f"Snapshot with ID '{snapshot_id}' not found for backupset '{backupset_name}'."
        )
    
    return snapshots_registry[snap_key]

@app.get("/machines/{machine_id}/backupsets/{backupset_name}/query")
async def query_snapshots(machine_id: str, backupset_name: str, from_ts: Optional[datetime] = None, to_ts: Optional[datetime] = None):
    """
    Perform time-based or checksum-based filtering of snapshots.
    """
    # TODO: Add query parameters and logic
    return {"message": "Filtered snapshot results"}

@app.post("/machines/{machine_id}/backupsets/{backupset_name}")
async def upload_snapshot(machine_id: str, backupset_name: str, snapshot: SnapshotInDB) -> dict:
    key = (machine_id, backupset_name)
    snap_key = (machine_id, backupset_name, snapshot.snapshot_id)

    if key not in backupsets_registry:
        raise HTTPException(
            status_code=404,
            detail=f"Backupset '{backupset_name}' not found for machine '{machine_id}'."
        )

    if snap_key in snapshots_registry:
        raise HTTPException(
            status_code=409,
            detail=f"Snapshot with ID '{snapshot.snapshot_id}' already exists for backupset '{backupset_name}'."
        )

    snapshots_registry[snap_key] = snapshot
    return {"message": "Snapshot uploaded successfully"}
