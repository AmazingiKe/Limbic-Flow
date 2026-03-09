"""
数据备份
"""

import shutil
import json
from pathlib import Path
from datetime import datetime


def backup_data(
    data_dir: str = "data",
    backup_dir: str = "backups"
):
    """备份数据"""
    
    Path(backup_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / f"backup_{timestamp}"
    backup_path.mkdir()
    
    # 复制数据文件
    data_path = Path(data_dir)
    if data_path.exists():
        for file in data_path.rglob("*"):
            if file.is_file():
                dest = backup_path / file.relative_to(data_path)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
    
    # 保存备份信息
    info = {
        "timestamp": timestamp,
        "files": [str(f.relative_to(backup_path)) for f in backup_path.rglob("*") if f.is_file()]
    }
    
    with open(backup_path / "info.json", "w") as f:
        json.dump(info, f, indent=2)
    
    print(f"备份完成: {backup_path}")
    return str(backup_path)


def restore_backup(backup_path: str, data_dir: str = "data"):
    """恢复备份"""
    
    backup_path = Path(backup_path)
    data_path = Path(data_dir)
    
    # 读取备份信息
    with open(backup_path / "info.json") as f:
        info = json.load(f)
    
    # 恢复文件
    for file in info["files"]:
        src = backup_path / file
        dest = data_path / file
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    
    print(f"恢复完成: {data_dir}")


def list_backups(backup_dir: str = "backups") -> list:
    """列出备份"""
    
    backups = []
    
    for path in Path(backup_dir).iterdir():
        if path.is_dir():
            info_file = path / "info.json"
            if info_file.exists():
                with open(info_file) as f:
                    info = json.load(f)
                    backups.append({
                        "path": str(path),
                        "timestamp": info["timestamp"],
                        "files": len(info["files"])
                    })
    
    return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
