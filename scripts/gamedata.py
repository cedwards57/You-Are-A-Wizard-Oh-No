class GameData():
    def __init__(self):
        self.items = set()
        self.sprites = {
            "WIZARD": "img/wizard.png",
            "BAKER": "img/baker.png",
            "NONE": "img/none.png",
            "SWORDSMAN": "img/swordsman.png",
            "WITCH": "img/witch.png",
            "VOID": "img/void.png",
        }
    
    def add(self, item):
        self.items.add(item)
    
    def meets_requirement(self, item):
        if item is None:
            return True
        if item in self.items:
            return True
        if item[0] == "!" and item[1:] not in self.items:
            return True
        
        return False
    