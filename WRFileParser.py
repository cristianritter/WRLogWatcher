"""parse_file function returns fata from the last line with the flag or 0 if no flags found"""
import parse_config
import os
from datetime import datetime, timedelta
from file_read_backwards import FileReadBackwards

def parse_file():
    try:
        configuration = parse_config.ConfPacket()
        configs = configuration.load_config(
        'diretorios, default'  #carrega configuracoes do arquivo config.ini
        )
        #print(configs)
        FLAG = configs['default']['flag']
        log_filename = f'Comm_{datetime.now().year}_{datetime.now().month}_{datetime.now().day}.txt'  # define o nome do arquivo de log atual baseado na data de hoje
        log_path = (configs['diretorios']['pasta_raiz_dos_logs'])  #carrega o diretorio dos logs desde o arquivo de configuracoes config.ini
        arquivo_de_log = os.path.join(log_path, log_filename)  # cria o caminho completo do arquivo unindo o diretorio de logs com o nome do arquivo

        data_list = [['id', 'date','time', 'message']]  #criacao de um dicionario para armazenar os dados
        try:
            with FileReadBackwards(arquivo_de_log, encoding='utf-8') as conteudo:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
                for idx, linha in enumerate(conteudo):
                    line_data = linha.replace(" - ", "-").split('-')  #separa dos dados da linha em uma lista 
                    line_data.insert(0, idx)    #insere um indice na lista
                    data_list.append (line_data)  #adiciona os dados em uma lista global
                    if idx == 10:         #define quantas linhas serao analisadas 
                        break

        except Exception as Err:
            print("Erro ao abrir o arquivo. Verifique o caminho no arquivo 'config.ini'")
            print(Err)

        #print(data_list)
        for linha in data_list:    #itera sobre a lista contendo todos os dados organizados
            if (FLAG in linha):  #procura pela Flag Flops
                print(f"A flag {FLAG} foi encontrada")
                return linha  #caso encontre retorna as informações da linha
                break
        return 0
        
    except Exception as Err:
        print(Err)

if (__name__ == '__main__'):
    print(parse_file())