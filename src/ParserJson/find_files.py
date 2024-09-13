import os
from src.ParserJson import ParserEntity


def find_all_files(directory, extension=".json"):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                file_path = os.path.join(root, filename)
                yield file_path


def read_entity_files(directory):
    for file_path in find_all_files(directory):
        try:
            ParserEntity.EntityParser(file_path)
            print(f"Parsed {file_path} successfully.")
        except Exception as e:
            print(f"Failed to parse {file_path}: {str(e)}")
            raise
