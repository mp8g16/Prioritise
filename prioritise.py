from datetime import datetime
import json



class Task:
    def __init__(self,
                 name="",
                 description="",
                 state="Not Started",
                 from_dict=None):
        
        if from_dict is None:
            assert isinstance(name, str)
            assert isinstance(description, str)
            assert isinstance(state, str)

            self.name = name
            self.time = datetime.now().replace(microsecond=0)
            self.description = description
            self.order = None
            self.state = state
        else:
            self.name = from_dict["name"]
            self.time = datetime.fromisoformat(from_dict["time"])
            self.description = from_dict["description"]
            self.order = from_dict["order"]
            self.state = from_dict["state"]

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

    #def __eq__(self, other):
    #    """less or equals"""
    #    return self.compare(other, {"s"})

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
                "time": self.time.isoformat(),
                "order": self.order,
                "state": self.state,
                "description": self.description}
        
class Prioritise:
    def __init__(self, file="data\\tasks.json"):
        """
        init
        """
        self.file = file
        self.commands = ["help", "add", "sort", "sort_all", 
                         "list", "list_all", "show", "show_all",
                         "task_numbers", "delete", "close"]
        if file is not None: self.load()
   
    def save(self):
        """
        init
        """
        data = json.dumps([item.get_dict() for item in self.tasks])
        with open(self.file, 'w') as f:
            f.write(data)

    def load(self):
        """
        init
        """
        try:
            with open(self.file, 'r') as f:
                data = f.read()
        except:
            self.tasks= []
            self.save()
            with open(self.file, 'r') as f:
                data = f.read()

        self.tasks = [Task(from_dict=item) for item in json.loads(data)]
    
    def run(self):
        """
        Runs the prioritise command line application
        """
        ans = input("What can I do for you:\n    ").lower()
        print()

        while getattr(self, ["invalid", ans][ans in self.commands])():
            ans = input("Is there anything else I can do?\n    ").lower()
            print()

    def invalid(self):
        """
        This method is run when Prioritise does not recognise a command
        """
        print("I'm sorry, that input isn't a command I recognise. "
              "To see a list of commands, type help.")
        return True
            
    def help(self):
        """
        Prioritise can sort a list of tasks based on user comparisons.
        The following commands can be given to Prioritise:
        """
        
        print("Prioritise understands the following commands")
        for item in self.commands:
            print(f"    {item}\t{getattr(self, item).__doc__}")

        return True
        
    def add(self):
        """
        Adds a new task to the task list given the name, description
        and state specified by the user.
        """
        
        task_params = {"name" : input("What is the task name?\n    "),
                       "description" :input("\nTask description:\n    ")
                      }
        state_text = ("\nAdd a task state. The state may be: "
                      "Not Started/In Progress/Complete/Frozen/"
                      "Fossilised (ns/ip/co/fr/fo). "
                      "For a description of what these states mean "
                      "type explain (e)\n    ")
        states = {"not started" : "Not Started",
                  "in progress" : "In Progress",
                  "complete"    : "Complete",
                  "frozen"      : "Frozen",
                  "Fossilised"  : "Fossilised",  
                  "ns"          : "Not Started",
                  "ip"          : "In Progress",
                  "co"          : "Complete",
                  "fr"          : "Frozen",
                  "fo"          : "Fossilised"}
        state_missing = True
        
        while state_missing:
            state = input(state_text).lower()
            if state in {"explain", "e"}:
                print("\nNot written yet")
            elif state in states:
                task_params["state"] = states[state]
                state_missing = False
            else:
                state_text = ("Sorry, I don't recognise that state."
                              "Could you input either Not Started/"
                              "In Progress/Complete/Frozen/Fossilised "
                              "(ns/ip/co/fr/fo).\n    ")
        
        self.tasks.append(Task(**task_params))
        self.save()
        print("Task added\n")

        return True
            
    def sort(self):
        """
        Sorts the list of tasks which are Not Started or In Progress
        based on user comparisons and the previous ordering. 
        Once sorted, this method assigns a new
        integer to the order variable for each task in the list
        """
        self.tasks.sort(reverse=True)
        
        for ind, val in enumerate(self.tasks):
            val.order = ind

        return True
    
    def sort_all(self):
        """
        Sorts the list of tasks which are Not Started or In Progress
        based only on user comparisons. Once sorted, this method assigns
        a new integer to the order variable for each task in the list.
        """
        raise NotImplementedError

        return True
    
    def list(self):
        """
        Prints a list of all the task names which are
        not complete or fossilised
        """
        print("Current Tasks:")
        for val in self.tasks:
            if val.state not in {"Complete", "Fossilised"}:
                print(f"    {val}")

        return True
    
    def list_all(self):
        """
        Prints a list of all the task names
        """
        print("All Tasks:")
        for val in self.tasks:
            print(f"    {val}")
        
        return True
    
    def show(self):
        """
        After entering a specific task name, show will print all the
        information associated with that task
        """
        raise NotImplementedError

        return True
        
    def show_all(self):
        """
        Will print all the information associated with all tasks
        """
        print("Task Info:")
        for val in self.tasks:
            print("    " + "\n    ".join(repr(val).split('\n'))+"\n")

        return True
    
    def task_numbers(self):
        """
        Will print the total number of tasks, as well as the number
        of tasks with each assigned state.
        """
        
        totals = {"Not Started" : 0,
                  "In Progress" : 0,
                  "Complete"    : 0,
                  "Frozen"      : 0,
                  "Fossilised"  : 0
                  }
        
        for item in self.tasks: totals[item.state] += 1
        
        print("Totals:")
        print(f"    Tasks       : {len(self.tasks)}")
        print(f"    Not Started : {totals['Not Started']}")
        print(f"    In Progress : {totals['In Progress']}")
        print(f"    Complete    : {totals['Complete']}")
        print(f"    Frozen      : {totals['Frozen']}")
        print(f"    Fossilised  : {totals['Fossilised']}")
        print()

        return True
    
    def delete(self):
        ans = input("Which item do you wish to delete?\n    ")

        for item in self.tasks:
            if ans == item.name: 
                self.tasks.remove(item)
                print(f"\nDeleted {ans}\n")
                break
        else:
            print("\nI couldn't find any tasks with that name\n")
            
        return True
        
    
    def close(self):
        """
        Will save the information stored in Prioritise and end
        the command line function.
        """

        self.save()
        return False

if __name__ == "__main__":
    Prioritise().run()