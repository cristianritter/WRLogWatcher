"""Verifica erros retorna um boolean com informacoes sobre problemas no sistema"""
from WRFileParser import parse_file
from datetime import datetime, timedelta
import parse_config


def hora_atual():   
    """retorna a hora atual"""
    return datetime.now()

def hora_do_registro(registro):
    """retorna a hora do registro informado"""
    data = datetime.strptime(registro[1], "%d/%m/%Y")
    hora =  datetime.strptime(registro[2], "%H:%M:%S,%f")    
    return data.combine(data.date(), hora.time())

def tempo_da_ultima_flag(registro):
    """retorna a diferenca entre o horario atual e o horario do ultimo registro encontrado em log"""
    return hora_atual()-hora_do_registro(registro)

def verifica_erros(registro):
    """ Retorna se existem problemas com base nas informacoes do log
    e do horario atual do sistema, recebe os dados do ultimo registro 
    encontrado em log"""
    try:
        configuration = parse_config.ConfPacket()
        configs = configuration.load_config(
            'default'  #carrega configuracoes do arquivo config.ini
        )
        FLAG_MAX_TIME = int(configs['default']['flag_max_time_seconds'])
        if (tempo_da_ultima_flag(registro) > timedelta(seconds=30)):
            return True
        else:
            return False

    except Exception as Err:
        print(Err)
        return 0


if (__name__ == "__main__"):
    data_ = parse_file()
    if (data_):
        pass
        print(verifica_erros(data_))
    
