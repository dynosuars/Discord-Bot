import enum
import json
import random



class responses:
    
    methods = {
            "lower()" : str.lower,
            "upper()" : str.upper, 
        }
        
        # Deadass wish there was ENUM
    operators = {
            "==" : lambda x, y: x == y,
            "!=" : lambda x, y: x != y,
            "has" : lambda x, y: y in x,
            "endswith" : str.endswith,
            "startswith" : str.startswith
        }
    
    
    
    def __init__(self, name: str, condition: list[str], repsonse: list[str], weights: list[int] = None, relation: list[str] | None= None):
        self.name = name
        self.condition = condition
        self.response = repsonse
        self.weights = weights or [1 for _ in repsonse]
        self.relation = relation or []

    @staticmethod
    def parse(file: str) -> dict:
        
        with open(file, "r") as f:
            data = json.load(f)
            f.close()
        ret:list[responses] = []

        for value in data['responses']:
            ret.append(responses(value["name"], value["condition"], value["response"], value["weights"], relation=value["relation"]))
            
        return {"responses": ret, "default": data["default"]}
    

    def check_condition(self, message: str) -> bool:
        # Semi parser
        
        # Compilation
        ret = []
        
        for condition in self.condition:
            for operator in sorted(self.operators.keys(), key=len, reverse=True):
                if(operator in condition):
                    # Evaluation
                    left, right = condition.split(operator, 1)
                    left, right = left.strip(), right.strip()
                    
                    base = message 
                    
                    parts = left.split(".")
                    if parts[0] != "{msg}":
                        raise ValueError("Invalid base")

                    # Evaluating the left side---putting fucntions
                    for method in parts[1:]:
                        if(method in self.methods.keys()):
                            if method in self.methods:
                                base = self.methods[method](base)
                        else:
                            raise LookupError(f"Invalid method: {method} at {condition}")
                        
                    ret.append(self.operators[operator](base, right))
                    break       
                        
        if(len(ret) == 0):
            raise LookupError(f"Invalid or no operator")
        
        # Default is OR
        if(len(self.relation) == 0):
            return any(ret)
        # Evaluate from left to right
        
        # Check if missing condition
        
        if( self.relation and len(self.relation) != len(self.condition) - 1):
            raise LookupError(f"Invalid number of relation and conditon")
        
        current = ret[0] if ret else False
        for i in range(1, len(ret)):
            if self.relation[i - 1] == "or":
                current = current or ret[i]
            else:  # assume "and"
                current = current and ret[i]
            
        return current
            
            
        
        
        
                
    
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    

# debug
if(__name__ == "__main__"):
    reponses1 = responses.parse("ext/responses.json")
    
    while(True):
        msg = input("You: ")
        responded = False
        for reponse in reponses1["responses"]:
            if(reponse.check_condition(msg)):
                print("Bot: " + random.choices(reponse.response, reponse.weights)[0])
                responded = True
                break
        if(not responded):
            print("Bot: " + random.choices(reponses1["default"])[0])
            
    
    
            



