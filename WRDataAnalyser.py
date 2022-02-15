from datetime import datetime, timedelta
import sys
from WRFileLogger import WRLogger

class WRAnalizer:   
    """    Classe que realiza a analise dos dados do log   """
    def __init__(self, logger: WRLogger):
        self.logger = logger
        pass

    def get_datahora_registro(self, registro):
        '''Recebe em registro uma lista de tamanho 4 no formato
        [indice no log, data, hora, flag]
        Ex.
        [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
        Retorna 0 em caso de erro
        '''
        try:
            data_registro = datetime.strptime(registro[1], "%d/%m/%Y")                
            hora_registro =  datetime.strptime(registro[2], "%H:%M:%S,%f")    
            datahora_registro = datetime.combine(data_registro.date(), hora_registro.time())
            return datahora_registro
        except:
            return 0

    def tempo_desde_flag(self, registro):
        """Retorna a diferenca entre o horario atual do sistema e o horario do ultimo registro da flag no log;
        retorna 0 se o registro não for encontrado."""
        try:
            datahora_atual = datetime.now()
            return datahora_atual - self.get_datahora_registro(registro)
        except Exception as Err:
            print(f'Erro em tempo desde flag: {Err}')
            self.logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}')
            return 0

    def get_time_offset(self, regMaster, regSlave):
        '''Retorna a diferança de tempo entre os registros informados timedelta, retorna 999 em caso de erros'''
        try:
            last_flag_time_slave = self.get_datahora_registro(regSlave)
            last_flag_time_master = self.get_datahora_registro(regMaster)
            offset: timedelta

            if (last_flag_time_master == 0 or last_flag_time_master == 0):
                return timedelta(seconds=900)                                                    # se houver problemas na leitura de algum registro

            if last_flag_time_master > last_flag_time_slave:                    # se master estiver atrasado com relacao a slave
                offset = last_flag_time_master - last_flag_time_slave  
                if (offset < timedelta(milliseconds=20)):
                    offset = -offset                                            # retorna valor positivo caso o timedelta seja menor do que a tolerancia
            else:
                offset = last_flag_time_slave - last_flag_time_master
            return offset
        except Exception as Err:
            self.logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}')
               


    def mode_detect(self, config_offsets, current_offset):
        '''Detecta o modo de operacao com base no offset de tempo entre os disparos,
        recebe os parametros de tempo para realizacao da analise.'''
        try:
            avaiable_modes = ["SAT POA", "BARIX", "SAT REG", "LINK DOWN"]
            offsets = config_offsets.split(', ')
            if (current_offset <= timedelta(milliseconds=int(offsets[0]))):
                return avaiable_modes[0]
            elif (current_offset < timedelta(milliseconds=int(offsets[1]))):
                return avaiable_modes[1]
            elif (current_offset < timedelta(milliseconds=int(offsets[2]))):
                return avaiable_modes[2]
            else:
                return avaiable_modes[3]
        except Exception as Err:
            self.logger.adiciona_linha_log(f'Erro em: {sys._getframe().f_code.co_name}, Descrição: {Err}')
            print(f'Erro em mode_detect: {Err}')
  
  
if (__name__ == "__main__"):    #exemplo de uso da biblioteca
    analizer = WRAnalizer()
    data_ = [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
    analizer.get_time_offset(data_, data_)
   