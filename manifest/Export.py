import json
from model import Container  
class JSONFileHandler:
    def write(self, manifest, file_path):
        formatted_data = {
            'manifest': [container.to_dict() for container in manifest.get_containers()]
        }
        with open(file_path, 'w') as file:
            json.dump(formatted_data, file, indent=4)

class TextFileHandler:
    def write(self, manifest, file_path):
        with open(file_path, 'w') as file:
            for container in manifest.get_containers():
                line = f"[{container.position}], {{{container.weight}}}, {container.description}\n"
                file.write(line)
