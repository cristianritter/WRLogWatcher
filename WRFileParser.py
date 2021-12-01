"""parse_file function returns fata from the last line with the flag or 0 if no flags found"""
from file_read_backwards.buffer_work_space import _remove_trailing_new_line
import parse_config
import os
from datetime import datetime, timedelta
from file_read_backwards import FileReadBackwards

class WRFileParse:
    def __init__(self, flag, log_path):
        self.FLAG = flag
        self.LOG_PATH = log_path

    def get_log_filename(self):
        """retorna o caminho completo para acesso ao arquivo de log"""
        log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
        log_fullfilepath = os.path.join(self.LOG_PATH, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
        return log_fullfilepath

    def get_conteudo_log(self):
        """Retorna a quantidade de linhas informada do arquivo de log como uma string"""
        try:
            arquivo_de_log = self.get_log_filename()
            conteudo = []
            with FileReadBackwards(arquivo_de_log, encoding='utf-8') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for linha in frb:
                    conteudo.append(linha)
            return conteudo
        except Exception as Err:
            print(Err)

    def get_last_flag_line(self):
        """retorna uma lista com o conteudo da ultima linha de log com a flag ou retorna 0 em caso de erro"""
        try:
            arquivo_de_log = self.get_log_filename()
            data_list = [['id', 'date','time', 'message']]  #criacao de um dicionario para armazenar os dados
            conteudo = self.get_conteudo_log()
            #print(conteudo)
            for idx, linha in enumerate(conteudo):
                line_data = linha.replace(" - ", "-").split('-')  #separa dos dados da linha em uma lista 
                line_data.insert(0, idx)    #insere um indice na lista
                data_list.append (line_data)  #adiciona os dados em uma lista global
            #print(data_list)
            for linha in data_list:    #itera sobre a lista contendo todos os dados organizados
                if (self.FLAG in linha):  #procura pela Flag Flops
                    print(f"A flag {self.FLAG} foi encontrada")
                    return linha  #caso encontre retorna as informações da linha
            return 0
            
        except Exception as Err:
            print(Err)

if (__name__ == '__main__'):
    configuration = parse_config.ConfPacket()
    configs = configuration.load_config(
    'diretorios, default'  #carrega configuracoes do arquivo config.ini
    )
    FLAG = configs['default']['flag_string']
    LOG_PATH = (configs['diretorios']['pasta_raiz_dos_logs'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini
    parser = WRFileParse(FLAG, LOG_PATH)
    print(parser.get_last_flag_line())
    