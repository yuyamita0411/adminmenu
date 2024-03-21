from flask import jsonify
import os

class Function:
    def __init__(self, name):
        self.name = name

    def fileExists(p):
        if p is None:
            return {'status_code': 400}
        if not os.path.exists(p):
            return {'status_code': 400}
        return {'status_code': 200}