import configparser
import os.path

class ConfPacket:
    def __init__(self, arquivo='config.ini'):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        self.CONFIG_PATH = os.path.join(ROOT_DIR, arquivo)  

    def load_config(self, apointed):
        parser = configparser.ConfigParser()

        try:
            parser.read(self.CONFIG_PATH)
        except Exception as error:
            print ('Erro: ', error)

        if (parser.sections() == []):
            raise NameError("Arquivo config.ini corrompido ou nao encontrado.")
        
        configs = {}
        for item in apointed.split(', ') :
            item = item.lower() 
            configs[item] = {}

            try:
                for key in parser[item]:
                    configs[item][key] = parser[item][key]          
            
            except Exception as error:
                print ('Erro no arquivo config.ini: ', error)
        return configs

if __name__ == '__main__':
    configs = ConfPacket()
    items = configs.load_config('default')
    print(items)
