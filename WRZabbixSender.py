from pyzabbix import ZabbixMetric, ZabbixSender
import time
from threading import Thread


class WRZabbixSender:
    """
    Classe que implementa o sistema de envio de metricas para o Zabbix \n
    Recebe os seguintes parametros: \n
    metric_interval - intervalo entre o envio das metricas para o servidor \n
    hostname - zabbix hostname \n
    key - zabbix key \n
    server - zabbix serve ip address \n
    port - zabbix port number \n
    idx -  indice da variavel de lista que possui os dados de metrica a serem enviados \n
    status - lista que traz os dados de metrica

    """
    def __init__(self, metric_interval, hostname, key, server, port, idx, status):
        self.metric_interval = int(metric_interval)
        self.hostname = hostname
        self.key = key
        self.server = server
        self.port = int(port)
        self.status = status
        self.idx = idx
        
    def send_metric(self, status):
        '''Rotina que continuamente envia as metricas               
        Recebe um array do tipo lista e utiliza os dados de indice da classe criada. Funcionam como ponteiro, \n
        portanto ao alterar os valores na lista se altera também o valor da metrica enviada.
        '''
        try:
            while True:
                #print(status)
                time.sleep(self.metric_interval)       
                texto_metrica = ""
                produto=1
                for mtrc in status:
                    produto *= mtrc
                #print(produto)  
                metrica = status[self.idx]
                #metrica = 3

                if (metrica & (1<<1) or produto):
                    texto_metrica = ' botoneira_master'
                if (metrica & (1<<0)):
                    texto_metrica = texto_metrica + ' botoneira_remota'
                if (not metrica):
                    texto_metrica = "0"

                try:
                    packet = [
                        ZabbixMetric(self.hostname, self.key, texto_metrica)
                    ]
                    ZabbixSender(zabbix_server=self.server, zabbix_port=self.port).send(packet)
                    print(texto_metrica)
                except Exception as Err:
                    print(f"Falha de conexão com o Zabbix - {Err}")
        except Exception as Err:
            print(f"Erro: {Err}")
            time.sleep(30)

    def start_zabbix_thread(self):
        """
        Método que inicia um thread de envio de metricas para o zabbix
        """
        try:
            u = Thread(target=self.send_metric, args=[self.status], daemon=True)
            u.start()
        except Exception as Err:
            print(f'Erro: {Err}')

if __name__ == '__main__':
    """
    Metodo que permite testar a funcao individualmente e fornece um exemplo de uso
    """
    HOSTNAME = "FLS - SERVER-RADIOS"
    ZABBIX_SERVER = "10.51.23.101"
    PORT = 10051
    SEND_METRICS_INTERVAL = 5
    data = [1]
    zsender = WRZabbixSender(SEND_METRICS_INTERVAL, HOSTNAME, 'key', ZABBIX_SERVER, PORT, 0, data )
    zsender.start_zabbix_thread()
    while(True):
        time.sleep(1)
        pass