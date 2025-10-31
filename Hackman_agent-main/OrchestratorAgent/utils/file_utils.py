"""File utility functions for finding and managing user_view files."""
import os
import glob
from typing import Optional


def find_latest_user_view(exports_dir: str = "ArcueAgent/exports") -> Optional[str]:
    """
    Find the most recent user_view JSON file in the exports directory.
    
    Args:
        exports_dir: Directory to search for user_view files
        
    Returns:
        Path to the latest user_view file, or None if not found
    """
    # Pattern to match user_view files (new format: user_view_{timestamp}.json)
    pattern = os.path.join(exports_dir, "user_view_*.json")
    
    # Find all matching files
    user_view_files = glob.glob(pattern)
    
    if not user_view_files:
        return None
    
    # Sort by modification time (most recent first)
    user_view_files.sort(key=os.path.getmtime, reverse=True)
    
    # Return the most recent file
    return user_view_files[0]


def list_recent_user_views(exports_dir: str = "ArcueAgent/exports", limit: int = 5) -> list:
    """
    List the most recent user_view JSON files.
    
    Args:
        exports_dir: Directory to search for user_view files
        limit: Maximum number of files to return
        
    Returns:
        List of file paths sorted by modification time (most recent first)
    """
    # Pattern to match user_view files (new format: user_view_{timestamp}.json)
    pattern = os.path.join(exports_dir, "user_view_*.json")
    user_view_files = glob.glob(pattern)
    
    if not user_view_files:
        return []
    
    # Sort by modification time (most recent first)
    user_view_files.sort(key=os.path.getmtime, reverse=True)
    
    return user_view_files[:limit]


def format_file_info(filepath: str) -> dict:
    """
    Get formatted information about a user_view file.
    
    Args:
        filepath: Path to the user_view file
        
    Returns:
        Dictionary with file information
    """
    import json
    from datetime import datetime
    
    info = {
        "path": filepath,
        "filename": os.path.basename(filepath),
        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S"),
        "size": os.path.getsize(filepath)
    }
    
    # Try to extract story info
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            info["title"] = data.get("title", "Unknown")
            info["genre"] = data.get("genre", "Unknown")
            info["characters"] = len(data.get("characters", []))
            info["scenes"] = len(data.get("scenes", []))
    except:
        pass
    
    return info

