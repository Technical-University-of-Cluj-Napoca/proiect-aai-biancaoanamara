import sys
import os

# Add the root project directory to the system path so we can import 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.parser_agent import CodeParserAgent

def main():
    # Initialize the parser agent
    parser = CodeParserAgent()
    
    # A public repository URL (Uniform Resource Locator) for testing
    test_repo_url = "https://github.com/pallets/click.git" 
    
    print("Starting the parsing process. This might take a few seconds...")
    
    # Parse the repository and get the RepositoryDTO (Data Transfer Object)
    repository_data = parser.parse(test_repo_url)
    
    # Display the results as requested in the documentation
    print("\n--- Parsing Results ---")
    print(f"Total parsed files: {len(repository_data.files)}")
    print(f"Detected languages: {[lang.value for lang in repository_data.languages]}")
    
    # Calculate total functions extracted (currently 0, but prepared for AST parsing)
    total_functions = sum(len(file_dto.functions) for file_dto in repository_data.files)
    print(f"Total extracted functions: {total_functions}")
    
    print("\n--- First 3 CodeFileDTOs ---")
    for i, file_dto in enumerate(repository_data.files[:3]):
        print(f"\nFile {i + 1}: {file_dto.file_path}")
        print(f"Language: {file_dto.language.value}")
        print(f"Lines of code: {file_dto.lines_of_code}")

if __name__ == "__main__":
    main()