"""parse_file function returns fata from the last line with the flag or 0 if no flags found"""
import parse_config
import os
from datetime import datetime
from file_read_backwards import FileReadBackwards

class WRFileParse:
    def __init__(self, flag, log_path_master, log_path_slave):
        self.FLAG = flag
        self.LOG_PATH_MASTER = log_path_master
        self.LOG_PATH_SLAVE = log_path_slave

    def get_log_filename(self, description='master'):
        """retorna o caminho completo para acesso ao arquivo de log"""
        if (description.lower() == 'master'):
            LOG_PATH = self.LOG_PATH_MASTER
        elif (description.lower() =='slave'):
            LOG_PATH = self.LOG_PATH_SLAVE
        else:
            raise NameError("Argumento incorreto")

        log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
        log_fullfilepath = os.path.join(LOG_PATH, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
        return log_fullfilepath

    def get_conteudo_log(self, description='master'):
        """Retorna a quantidade de linhas informada do arquivo de log como uma string"""
        try:
            arquivo_de_log = self.get_log_filename(description)
            conteudo = []
            with FileReadBackwards(arquivo_de_log, encoding='utf-8') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for idx, linha in enumerate(frb):
                    conteudo.append(f'{idx} - {linha}')
            return conteudo
        except Exception as Err:
            print(Err)

    def get_last_flag_line(self, description='master'):
        """retorna uma lista com o conteudo da ultima linha de log com a flag ou retorna 0 em caso de erro"""
        try:
            data_list = []  #criacao de um dicionario para armazenar os dados
            for linha in self.get_conteudo_log(description):
                line_data = linha.replace(" - ", "-").split('-')  #separa dos dados da linha em uma lista 
                data_list.append (line_data)  #adiciona os dados em uma lista global
            for linha in data_list:    #itera sobre a lista contendo todos os dados organizados
                if (self.FLAG in ' '.join(linha)):  #procura pela Flag 
                    return linha  #caso encontre retorna as informações da linha
            return 0
        except Exception as Err:
            print(Err)

    def get_some_reg(self, finded_reg, descricao='master'):
        """Procura pela existencia de um registro especifico em um log com base em um disparo registrado em outro log"""
        for linha in self.get_conteudo_log(descricao):
            if (finded_reg[3] in linha):
                return linha.replace(" - ", "-").split('-')
        pass

if (__name__ == '__main__'):
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'diretorios, default'  #carrega configuracoes do arquivo config.ini
    )
    FLAG = configs['default']['flag_string']
    LOG_PATH_MASTER = (configs['diretorios']['pasta_logs_master'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini
    LOG_PATH_SLAVE = (configs['diretorios']['pasta_logs_slave'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini
    parser = WRFileParse(FLAG, LOG_PATH_MASTER, LOG_PATH_SLAVE)
    somereg = parser.get_last_flag_line('slave')
    print(somereg)
    print(parser.get_some_reg(somereg, 'master'))
    