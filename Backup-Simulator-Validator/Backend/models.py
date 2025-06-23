from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class BackupsetBase(BaseModel):
    machine_id: str = Field(..., description="Identifier for the machine where the backupset is stored")
    backupset_name: str = Field(..., description="Name of the backup set")

class BackupsetCreate(BackupsetBase):
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the backup set was created")

class BackupsetInDB(BackupsetCreate):
    id: Optional[int] = Field(None, description="Database ID of the backup set")

class FileMetadata(BaseModel):
    path: str = Field(..., description="Path to the file")
    size: Optional[int] = Field(None, description="Size of the file in bytes")
    mtime: Optional[float] = Field(None, description="Last modified time of the file as a timestamp")
    checksum: Optional[str] = Field(None, description="Checksum of the file")
    inode: Optional[int] = Field(None, description="Inode number of the file")
    error: Optional[str] = Field(None, description="Error message if any occurred while processing the file")

class SnapshotSummary(BaseModel):
    file_count: int = Field(..., description="Total number of files in the snapshot")
    total_size: int = Field(..., description="Total size of all files in the snapshot in bytes")
    error_count: int = Field(..., description="Number of files that encountered errors during processing")

class SnapshotBase(BaseModel):
    snapshot_id: str = Field(..., description="Unique identifier for the snapshot")
    timestamp: datetime = Field(..., description="Timestamp when the snapshot was created")
    machine_id: str = Field(..., description="Identifier for the machine where the snapshot was taken")
    backupset_name: str = Field(..., description="Name of the backup set")
    summary: SnapshotSummary = Field(..., description="Summary of the snapshot")
    files: List[FileMetadata] = Field(..., description="List of file metadata in the snapshot")

class SnapshotCreate(SnapshotBase):
    pass

class SnapshotInDB(SnapshotBase):
    id: Optional[int] = Field(None, description="Database ID")

