import json

class WorkhoursDecoder(json.JSONDecoder):
    def default(self, dct):
        return dct
