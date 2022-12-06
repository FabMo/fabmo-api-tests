#Module is an object that encapsulates the fabmo api text of "status" as an object with fields

class FabmoStatus:
    def __init__(self, statusText):
        self.dictionary = statusText

    def get(self, key):
        return self.dictionary[key]        

    def printMe(self):
        for key in self.dictionary.keys():
            if key == "job":
                for job_key in self.dictionary[key].keys():
                    print(f"       {job_key} : {self.dictionary[key].get(job_key)}")
            else:        
                print(f"{key} : {self.dictionary.get(key)}")
 
