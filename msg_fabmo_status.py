class FabmoStatus:
    def __init__(self, statusText):
        if not isinstance(statusText, dict):
            raise TypeError('statusText must be a dictionary')
        self.dictionary = statusText

    def get_key(self, key):
        return self.dictionary.get(key)

    def get_sub_key(self, main_key, sub_key):
        if main_key not in self.dictionary:
            return
        if not isinstance(self.dictionary[main_key], dict):
            raise TypeError(f'{main_key} is not a dictionary')
        return self.dictionary[main_key].get(sub_key)

    def printMe(self):
        for key, value in self.dictionary.items():
            if key == "job" and isinstance(value, dict):
                for job_key, job_value in value.items():
                    print(f"       {job_key} : {job_value}")
            elif key == "info" and isinstance(value, dict):
                for info_key, info_value in value.items():
                    print(f"       {info_key} : {info_value}")
            else:
                print(f"       {key} : {value}")
