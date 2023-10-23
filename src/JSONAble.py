import json, Util

class JSONAble:
    def __init__(self) -> None:
        self.id = Util.getId()

    def getId(self):
        return self.id

    def toJSON(self) -> dict:
        return self.__dict__
    
    def __str__(self) -> str:
        return json.dumps(self.toJSON())