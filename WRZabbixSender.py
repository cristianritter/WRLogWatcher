from pyzabbix import ZabbixMetric, ZabbixSender
import time
from threading import Thread

class WRZabbixSender:
    def __init__(self, metric_interval, hostname, key, server, port, status):
        self.metric_interval = int(metric_interval)
        self.hostname = hostname
        self.key = key
        self.server = server
        self.port = int(port)
        self.status = status

    def send_metric(self, value):
        '''Envia metricas para zabbix:    
            
        Sugestão de uso:
            Em caso de problemas -> envia mensagem contendo informações do erro [strlen > 1]
                Em caso de sucesso nas rotinas -> envia flag str com '0' [strlen == 1]'''
        try:
            while True:
                time.sleep(self.metric_interval)       
                try:
                    packet = [
                        ZabbixMetric(self.hostname, self.key, value[0])
                    ]
                    ZabbixSender(zabbix_server=self.server, zabbix_port=self.port).send(packet)
                except Exception as Err:
                    print(f"Falha de conexão com o Zabbix - {Err}")
        except Exception as Err:
            print(f"Erro: {Err}")

    def start_zabbix_thread(self, v_data):
        """v_data é o valor da metrica que precisa ser passado como lista e pode ser alterada no contexto do programa"""
        try:
            u = Thread(target=self.send_metric, args=[v_data], daemon=True)
            u.start()
        except Exception as Err:
            print(f'Erro: {Err}')

if __name__ == '__main__':
    data = [1]
    zsender = WRZabbixSender()
    zsender.start_zabbix_thread(data)
    while(True):
        time.sleep(1)
        pass