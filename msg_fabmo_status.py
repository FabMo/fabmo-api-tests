#Module is an object that encapsulates the fabmo api text of "status" as an object with fields

class FabmoStatus:
    def __init__(self, statusText):
        self.dictionary = statusText

    def get_key(self, key):
        return self.dictionary[key]

    def get_sub_key(self, main_key, sub_key):
        for key in self.dictionary.keys():
            # This check is specifically for the 'info' field
            # which is not always present in the status report
            if main_key not in self.dictionary.keys():
                return

        return self.dictionary[main_key][sub_key]

    def printMe(self):
        for key in self.dictionary.keys():
            if key == "job":
                for job_key in self.dictionary[key].keys():
                    print(f"       {job_key} : {self.dictionary[key].get_key(job_key)}")
            elif key == "info":
                for info_key in self.dictionary[key].keys():
                    print(f"       {info_key} : {self.dictionary[key].get_key(info_key)}")
            else:
                print(f"{key} : {self.dictionary.get_key(key)}")
