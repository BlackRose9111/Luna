#objects can be json or database related. Json objects should be managed by the filemanager class in system

class DataObject():
    def __init__(self):
        pass
    def create(self):
        pass
    def delete(self):
        pass
    def update(self):
        pass

    @staticmethod
    def get(**kwargs) -> object:
        pass
    @staticmethod
    def get_all() -> list:
        pass
    @staticmethod
    def get_all_by(**kwargs) -> list:
        pass



