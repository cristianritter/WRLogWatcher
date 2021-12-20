"""parse_file function returns fata from the last line with the flag or 0 if no flags found"""
import os
from datetime import datetime
from file_read_backwards import FileReadBackwards

class WRFileParse:
    def __init__(self, flag, log_paths):
        self.FLAG = flag
        self.LOG_PATHS = log_paths
      
    def get_log_filename(self, description='master'):
        """retorna o caminho completo para acesso ao arquivo de log"""
        if (description.lower() == 'master'):
            LOG_PATH = self.LOG_PATHS[0]
        elif (description.lower() =='slave'):
            LOG_PATH = self.LOG_PATHS[1]
        else:
            raise NameError("Argumento incorreto")
 
        log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
        log_fullfilepath = os.path.join(LOG_PATH, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
        return log_fullfilepath

    def get_conteudo_log(self, description='master'):
        """Retorna uma lista com o conteudo do log, retorna também uma informacao com a especie de linha, se erro, flag ou nenhuma especial"""
        try:
            arquivo_de_log = self.get_log_filename(description)
            conteudo = []
            with open(arquivo_de_log, mode='r', encoding='utf-8', errors='ignore') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for idx, linha in enumerate((frb.readlines())):  #reversed removed
                    if (self.FLAG in linha):
                        estilo = 'FLAG'
                    elif ('Error' in linha or 'filtrado' in linha):
                        estilo = 'ERROR'
                    else:
                        estilo = 'NENHUM'
                    
                    conteudo.append([f'{idx} - {linha}', estilo])
            return conteudo
        except Exception as Err:
            print(f'Erro durante o carregamento do arquivo de log, {arquivo_de_log} - {Err}')

    def get_last_flag_line(self, description='master'):
        """retorna uma lista com o conteudo da ultima linha de log com a flag ou retorna 0 em caso de erro"""
        try:
            data_list = []  #criacao de um dicionario para armazenar os dados
            for linha in reversed(self.get_conteudo_log(description)):  #adicionado reversed
                line_data = linha[0].replace(" - ", "-").split('-')  #separa dos dados da linha em uma lista 
                data_list.append (line_data)  #adiciona os dados em uma lista global
            for linha in data_list:    #itera sobre a lista contendo todos os dados organizados
                if (self.FLAG in ' '.join(linha)):  #procura pela Flag 
                    return linha  #caso encontre retorna as informações da linha
            return 0
        except Exception as Err:
            print(f'Erro em get_last_flag_line: {Err}')

    def get_some_reg(self, finded_reg, descricao='master'):
        """Procura pela existencia de um registro especifico em um log com base em um disparo registrado em outro log"""
        for linha in self.get_conteudo_log(descricao):
            if (finded_reg[3] in linha[0]):
                return linha[0].replace(" - ", "-").split('-')
  
if (__name__ == '__main__'):
    import parse_config
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'diretorios, default'  #carrega configuracoes do arquivo config.ini
    )
    FLAG = configs['default']['flag_string']
    pathlog_list = configs['diretorios']['praca01'].split(', ')
    parser = WRFileParse(FLAG, pathlog_list)
    somereg = parser.get_last_flag_line('slave')
    