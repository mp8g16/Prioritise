from datetime import datetime
import json



class Task:
    def __init__(self, name="", description="", from_dict=None):
        
        if from_dict is None:
            assert isinstance(name, str)
            assert isinstance(description, str)

            self.name = name
            self.time = datetime.now().replace(microsecond=0)
            self.description = description
            self.order = None
            self.state = None
        else:
            self.dict.append(from_dict)
     
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return (f"Name        : {self}\n"
                f"Date Added  : {self.time.date()}\n"
                f"Time Added  : {self.time.time()}\n"
                f"Order       : {self.order}\n"
                f"State       : {self.state}\n"
                f"Description : {self.description}")
    
    def __lt__(self, other):
        """less than""" 
        return self.compare(other, {"l"})

    def __le__(self, other):
        """less or equals"""
        return self.compare(other, {"l","s"})

    def __eq__(self, other):
        """less or equals"""
        return self.compare(other, {"s"})
        
    def __ne__(self, other):
        """less or equals"""
        return self.compare(other, {"l","g"})
        
    def __gt__(self, other):
        """less or equals"""
        return self.compare(other, {"g"})

    def __ge__(self, other):
        """less or equals"""
        return self.compare(other, {"g","s"})
        
    def compare(self, other, true_vals):
        ans = input(f"Is {self} of greater/same/less (g/s/l) importance than {other}?\n").lower()
        result = {"g":"g",
                  "s":"s",
                  "l":"l",
                  "greater":"g",
                  "same":"s",
                  "less":"l" }
        
        attempts = 0
        responses = ["I'm sorry, I didn't understand that response. Would you mind typing it again as a single letter? Either g, s, or l.",
        "Ok, so that didn't work either sorry. This usually works, so make sure there are no spaces or other characters in the input.",
        "Bugger, right. Well, this is an infinite loop. You can try mashing keys, or you can quit the program (ctrl + C). Sorry about this.",
        "Still not working sorry. If an input works I will just step to the next question. Unfortunately, this is also the end of the dialogue shrub and consequently my quasi form of consciousness. Don't worry, you can still prod my dead shell, but it will only return the phrase 'I'm sorry, I didn't understand that input'.",
        "I'm sorry, I didn't understand that input"]
        
        while (out := result.get(ans, None)) is None:
            ans = input(responses[attempts]+"\n").lower()
            attempts += 1 if attempts<len(responses)-1 else 0

        return out in true_vals
        
    def get_dict(self):
        return {"name": self.name,
                "time": self.time,
                "order": self.state,
                "state": self.stated,
                "description": self.description}
        
class Prioritise:
    def __init__(self, file="data\\tasks.json"):
        self.file = file
        if file is not None: self.load()
    
    def run():
        ans = input("Prioritise Open\n").lower()
        responses = {"help"     : help,
                     "add"      : help,
                     "sort"     : help,
                     "list"     : help,
                     "list_all" : help,
                     "show"     : help,
                     "size"     : help,
                     "close"    :}

    while responses.get(ans, self.invalid)():
    
    def invalid(self):
        print("I'm sorry, that input isn't a command I recognise."
              "To see a list of commands, type help.")
        return True
            
    def help(self):
        print("stand in")
        
    def add(self):
        pass

        def save(self):
            pass

        def load(self):
            try:
                with open(self.file, 'r') as f:
                    cont = f.readlines()
            except: 
                open(self.file, "x").close()
                self.items = []
                
            
            param
            
    def sort(self):
        pass
    
    def

if __name__ == "__main__":
    Prioritise().run()