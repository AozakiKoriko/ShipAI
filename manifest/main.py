from Import import TextFileHandler as ImportTextFileHandler, JSONFileHandler as ImportJSONFileHandler
from Export import TextFileHandler as ExportTextFileHandler, JSONFileHandler as ExportJSONFileHandler
from model import Manifest   

def main():
    manifest = Manifest()
    import_text_handler = ImportTextFileHandler()
    export_text_handler = ExportTextFileHandler()
    import_json_handler = ImportJSONFileHandler()
    export_json_handler = ExportJSONFileHandler()

    # Read from text file and write to JSON
    import_text_handler.read(manifest, 'document/manifest.txt')
    export_json_handler.write(manifest, 'manifest.json')

    # Update a container and write the updated data to JSON
    manifest.update_container('01,01', '10000', 'Apple')
    export_json_handler.write(manifest, 'manifest.json')

    # Read updated JSON and write to text
    # Reset the manifest to avoid duplication
    manifest = Manifest()
    import_json_handler.read(manifest, 'manifest.json')
    export_text_handler.write(manifest, 'updated_manifest.txt')

    print("Conversion to and from JSON completed.")

if __name__ == "__main__":
    main()

