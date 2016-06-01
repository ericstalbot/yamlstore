import yaml
import simplejson as json
 
class InvalidYaml(Exception):
    pass
    

 
def process_yaml(yaml_string):
    
    try:
    
        data = yaml.safe_load(yaml_string)
        json_string = json.dumps(data, indent='  ')
    
    except yaml.YAMLError as e: #to do: json error here
    
        raise InvalidYaml(msg=str(e))
        
    return json_string
 