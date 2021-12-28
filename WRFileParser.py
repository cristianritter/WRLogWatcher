"""Biblioteca que realiza a leitura dos arquivos de log"""
import os
from datetime import datetime

class WRFileParse:
    '''Classe que realiza a leitura dos arquivos de log'''
    def __init__(self, ):
        pass

    def get_log_filename(self, path):
        """
        - retorna o caminho completo para acesso ao arquivo de log path+filename
        - se receber um path, retorna o path+arquivo do dia
        - se receber um caminho com arquivo, somente retorna o valor informado
        """
        if (os.path.isfile(path)):
            return path
        else:
            log_filename = f"Comm_{datetime.now().strftime('%Y_%m_%d')}.txt"  # define o nome do arquivo de log atual baseado na data de hoje
            log_fullfilepath = os.path.join(path, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo
            return log_fullfilepath

    def get_conteudo_log(self, fullfilepath):
        """ Retorna uma lista com o conteudo do arquivo de log e um idx de linha no estilo [f'{idx} - {linha}'] """
        try:
            arquivo_de_log = self.get_log_filename(fullfilepath)
            conteudo = []
            with open(arquivo_de_log, mode='r', encoding='utf-8', errors='ignore') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for idx, linha in enumerate((frb.readlines())):  #reversed removed                   
                    conteudo.append(f'{idx} - {linha}')
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
    pathlog_list = configs['diretorios']['praca01'].split(', ')
    parser = WRFileParse()
    conteudo = parser.get_conteudo_log(pathlog_list[0]) 
    print(conteudo)