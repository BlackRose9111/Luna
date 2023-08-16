import json

class filemanager():
    aliases : dict = {"alias": "variables/config/aliases.json"}
    def __init__(self):
        self.get_aliases()

    def get_aliases(self):
        obj : dict = filemanager.get_json(address=self.aliases["alias"],debug=False)
        for key in obj.keys():
            self.aliases[key] = obj[key]
    def get_alias(self,alias):
        try:
            return self.aliases[alias]
        except:
            return None


    @staticmethod
    def get_json(*, address : str = None,alias : str = None,debug = True) -> dict or None:
        file_address = None

        try:
            if address is not None:
                file_address = address
            elif address is None and alias is not None:
                fm = filemanager()
                file_address = fm.get_alias(alias=alias)
            elif address is None and alias is None:
                raise Exception("Missing address and alias")
            with open(file_address,"r") as f:
                contents = f.read()
                _object = dict(json.loads(contents))
                if debug is True:
                    print(f"Accessed {file_address}")
                return _object

        except:
            return None
    @staticmethod
    def enter_json(*, dictionary : dict, address :str = None, alias : str = None, debug = True):
        file_address = None
        try:
            if address is not None:
                file_address = address
            elif address is None and alias is not None:
                fm = filemanager()
                file_address = fm.get_alias(alias)
            elif address is None and alias is None:
                raise Exception("Missing address and alias")
            with open(file_address,"w") as f:
                json.dump(dictionary,f)
            if debug is True:
                print(f"Wrote {dictionary} on {file_address}")
        except Exception as e:
            print(f"An exception as occued {e}")

    @staticmethod
    def get_value_from_json(*, key : str, address : str = None,alias : str = None, debug = True,default = None) -> object or None:
        obj = filemanager.get_json(address=address, alias=alias, debug=debug)
        try:
            return obj[key]
        except:
            return default

    @staticmethod
    def change_or_add_value_on_json(*, key : str, new_value, address : str = None, alias : str = None, debug =True):
        obj = filemanager.get_json(address=address, alias=alias, debug=debug)
        obj[key] = new_value
        filemanager.enter_json(dictionary=obj,address=address,alias=alias,debug=debug)

    @staticmethod
    def delete_value_on_json(*, key : str, address : str  = None,alias : str = None, debug = True):
        obj : dict = filemanager.get_json(address=address,alias=alias,debug=debug)
        obj.pop(__key=key)
        filemanager.enter_json(dictionary=obj,address=address,alias=alias,debug=debug)



