class Brb():

    data = 'teste'
    
    def format_brb(self):
        return self.data
    
    def __str__(self):
        return self.data
    
    
    from modules.load_config import load_config
config = load_config()
