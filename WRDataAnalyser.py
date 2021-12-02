"""Verifica erros retorna um boolean com informacoes sobre problemas no sistema"""
from datetime import datetime, timedelta

class WRAnalizer:
    def __init__(self, flag_max_time):
        self.FLAG_MAX_TIME = flag_max_time
        
    def tempo_desde_flag(self, registro):
        """retorna a diferenca entre o horario atual e o horario do ultimo registro encontrado em log"""
        datahora_atual = datetime.now()
        data_registro = datetime.strptime(registro[1], "%d/%m/%Y")                
        hora_registro =  datetime.strptime(registro[2], "%H:%M:%S,%f")    
        datahora_registro = datetime.combine(data_registro.date(), hora_registro.time())
        return datahora_atual - datahora_registro

    def verifica_erros(self, registro):
        """ Retorna se existem problemas com base nas informacoes do log
        e do horario atual do sistema, recebe os dados do ultimo registro 
        encontrado em log"""
        try:
            if (self.tempo_desde_flag(registro) > timedelta(seconds=self.FLAG_MAX_TIME)):
            #if ( timedelta(seconds=100) > timedelta(seconds=self.FLAG_MAX_TIME)):
                return True
            else:
                return False

        except Exception as Err:
            print("Erro: ",Err)
            return 0


if (__name__ == "__main__"):
    analizer = WRAnalizer(30)
    data_ = [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
    #print(analizer.verifica_erros(data_))
    print(analizer.tempo_desde_flag(data_))