import os
import shutil
from git import Repo
from typing import List

def clone_repo(repo_url: str, dest_dir: str = "data/repos") -> str:
    """Clones a GitHub repository to the local filesystem and returns the path."""
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    target_path = os.path.join(dest_dir, repo_name)
    
    if os.path.exists(target_path):
        print(f"Repository {repo_name} already exists at {target_path}. Removing it...")
        shutil.rmtree(target_path)
    
    print(f"Cloning {repo_url} into {target_path}...")
    Repo.clone_from(repo_url, target_path)
    return target_path

def list_python_files(repo_path: str) -> List[str]:
    """Lists all Python files in the given repository path."""
    py_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def read_file_content(file_path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""
