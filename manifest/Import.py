import json
from model import Container 

class JSONFileHandler:
    def read(self, manifest, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data.get('manifest', []):
                manifest.add_container(Container(**item))

class TextFileHandler:
    def read(self, manifest, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                position = parts[0].strip('[]')
                weight = parts[1].strip('{}')
                description = parts[2]
                manifest.add_container(Container(position, weight, description))
