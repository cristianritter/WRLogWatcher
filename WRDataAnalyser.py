from datetime import datetime, timedelta

class WRAnalizer:   
    """    Classe que realiza a analise dos dados do log   """
    def __init__(self, logger):
        self.logger = logger
        pass

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
            print(f'Erro em tempo desde flag: {Err}')
            self.logger.adiciona_linha_log(f'Erro em tempo desde flag: {Err}')
            return 0

    def get_time_offset(self, regMaster, regSlave):
        '''Retorna a diferença de tempo entre dois registros informados (time offset)'''
        last_flag_time_slave = self.get_datahora_registro(regSlave)
        last_flag_time_master = self.get_datahora_registro(regMaster)
        if last_flag_time_master > last_flag_time_slave:  ## se master estiver atrasado com relacao a slave
            offset = [last_flag_time_master - last_flag_time_slave, -1]  ##retorna flag -1 se houver problemas
            if (offset[0] < timedelta(milliseconds=20)):
                offset[1] = 1
        else:
            offset = [last_flag_time_slave - last_flag_time_master, 1]
        return offset

    def mode_detect(self, config_offsets, current_offset):
        try:
            '''Detecta o modo de operacao com base no offset de tempo entre os disparos,
            recebe os parametros de tempo para realizacao da analise.'''
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
            self.logger.adiciona_linha_log(f'Erro em mode_detect: {Err}')
            print(f'Erro em mode_detect: {Err}')
  
  
if (__name__ == "__main__"):    #exemplo de uso da biblioteca
    analizer = WRAnalizer()
    data_ = [209, '24/11/2021', '06:05:37,430', 'WAIT 2']
    analizer.get_time_offset(data_, data_)
   