import os
from git import Repo
from src.dtos import CodeFileDTO, RepositoryDTO, Language

class CodeParserAgent:
    def __init__(self):
        # Define the folders we want to ignore so we don't process garbage data 
        self.ignored_dirs = ['.git', 'node_modules', 'venv', '__pycache__']
        # The local folder where we will download the code 
        self.base_repo_path = "data/repos"

    def parse(self, repo_url: str) -> RepositoryDTO:
        # 1. Extract the name of the repository from the URL
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        local_path = os.path.join(self.base_repo_path, repo_name)

        # 2. Clone the repository if it is not already downloaded
        if not os.path.exists(local_path):
            print(f"Cloning {repo_url} into {local_path}...")
            # We use depth=1 to download only the latest version, which is much faster [cite: 523]
            Repo.clone_from(repo_url, local_path, depth=1) 

        # 3. Analyze the downloaded files
        parsed_files = []
        total_loc = 0
        detected_languages = set()

        for root, dirs, files in os.walk(local_path):
            # Tell the system to ignore specific folders
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file in files:
                # Skip hidden files or extensions we don't care about
                if file.startswith('.'):
                    continue

                file_path = os.path.join(root, file)

                try:
                    # Open and read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.splitlines()
                        loc = len(lines)
                        total_loc += loc

                        # Determine the programming language (simplified check)
                        lang = Language.OTHER
                        if file.endswith('.py'):
                            lang = Language.PYTHON
                            detected_languages.add(Language.PYTHON)

                        # Package the file data into our DTO
                        file_dto = CodeFileDTO(
                            file_path=file_path,
                            language=lang,
                            content=content,
                            lines_of_code=loc,
                            functions=[], 
                            imports=[],
                            dependencies=[]
                        )
                        parsed_files.append(file_dto)
                except Exception as e:
                    # If we hit an unreadable or binary file, we just log it and move on [cite: 346]
                    print(f"Could not read {file_path}: {e}")

        # Package the entire repository into the final DTO [cite: 340]
        return RepositoryDTO(
            url=repo_url,
            name=repo_name,
            local_path=local_path,
            files=parsed_files,
            total_loc=total_loc,
            languages=list(detected_languages)
        )