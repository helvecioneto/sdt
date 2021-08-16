from dependecies import * 

def load_config(config_file = "./config.json"):
    
    with open(config_file) as json_file:
            json_data = json.load(json_file)
    return json_data