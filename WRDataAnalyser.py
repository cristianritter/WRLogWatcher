"""Biblioteca que realiza a analise dos dados do log e reporta se existem problemas"""
from datetime import datetime, timedelta

class WRAnalizer:   
    """"""
    def __init__(self, flag_max_time):
        self.FLAG_MAX_TIME = flag_max_time   #tempo maximo entre o horario atual e o horario da flag no log que não gera relato de problemas

    def get_datahora_registro(self, registro):
        '''Recebe em registro uma lista de tamanho 4 no formato
        [indice no log, data, hora, flag]
        Ex.
        [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
        '''
        data_registro = datetime.strptime(registro[1], "%d/%m/%Y")                
        hora_registro =  datetime.strptime(registro[2], "%H:%M:%S,%f")    
        datahora_registro = datetime.combine(data_registro.date(), hora_registro.time())
        return datahora_registro
        
    def tempo_desde_flag(self, registro):
        """Retorna a diferenca entre o horario atual do sistema e o horario do ultimo registro da flag no log;
        retorna 0 se o registro não for encontrado."""
        try:
            datahora_atual = datetime.now()
            return datahora_atual - self.get_datahora_registro(registro)
        except Exception as Err:
            print(Err)
            return 0

    def verifica_atraso_flag(self, registro):
        """ Booleano que retorna True se existem problemas; False se o sistema não detectou erros."""
        try:
            if (self.tempo_desde_flag(registro) > timedelta(seconds=self.FLAG_MAX_TIME)):  #verifica se o horario de registro da flag é anterior ao tempo maximo especificado
                return True
            else:
                return False

        except Exception as Err:
            print("Erro1: ",Err)
            return 0

    def get_flag_time_offset(self, regMaster, regSlave):
        last_flag_time_master = self.get_datahora_registro(regMaster)
        last_flag_time_slave = self.get_datahora_registro(regSlave)
        return last_flag_time_master - last_flag_time_slave




if (__name__ == "__main__"):    #exemplo de uso da biblioteca
    analizer = WRAnalizer(30)
    data_ = [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
    print(analizer.verifica_atraso_flag(data_))
    analizer.get_flag_time_offset(data_, data_)
   