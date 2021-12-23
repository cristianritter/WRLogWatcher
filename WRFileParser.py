"""parse_file function returns fata from the last line with the flag or 0 if no flags found"""
import os
from datetime import datetime

class WRFileParse:
    def __init__(self, flag):
        self.FLAG = flag
      
    def get_log_filename(self, path):
        """retorna o caminho completo para acesso ao arquivo de log"""
        if (os.path.isfile(path)):
            return path
        else:
            log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
            log_fullfilepath = os.path.join(path, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
            return log_fullfilepath

    def get_conteudo_log(self, fullfilepath):
        """Retorna uma lista com o conteudo do log, retorna também uma informacao com a especie de linha, se erro, flag ou nenhuma especial"""
        try:
            arquivo_de_log = self.get_log_filename(fullfilepath)
            conteudo = []
            with open(arquivo_de_log, mode='r', encoding='utf-8', errors='ignore') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for idx, linha in enumerate((frb.readlines())):  #reversed removed                   
                    conteudo.append(f'{idx} - {linha}')
            #print(conteudo)
            return conteudo
        except Exception as Err:
            print(f'Erro durante o carregamento do arquivo de log, {arquivo_de_log} - {Err}')
            return 0

  
if (__name__ == '__main__'):
    import parse_config
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'diretorios, default'  #carrega configuracoes do arquivo config.ini
    )
    FLAG = configs['default']['flag_string']
    pathlog_list = configs['diretorios']['praca01'].split(', ')
    parser = WRFileParse(FLAG)
    conteudo = parser.get_conteudo_log(pathlog_list[0]) 
    print(conteudo)