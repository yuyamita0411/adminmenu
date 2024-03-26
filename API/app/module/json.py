from flask import request, jsonify
import json

class Json:
    def __init__(self, name):
        self.name = name

    def get_json_data():
        data = request.get_json()
        if data is None:
            return None, jsonify({'error': 'No JSON data received'}), 400
        return data, None, None

    def save_json_data(filePath, fileData):
        try:
            with open(filePath, 'w', encoding='utf-8') as json_file:
                json.dump(fileData, json_file, ensure_ascii=False, indent=4)
            return jsonify({'message': 'JSON data saved successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def read_json_data(filePath):
        try:
            with open(filePath, 'r', encoding='utf-8') as file:
                return json.load(file), 200
        except FileNotFoundError:
            return {'error': f"The file '{filePath}' does not exist."}, 404
        except Exception as e:
            return {'error': str(e)}, 500