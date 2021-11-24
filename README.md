# WRLogWatcher
Este projeto é um sistema desenvolvido em Python que realizará o monitoramento dos arquivos de Log (registro de operações) do exibidor de comerciais das rádios do grupo NSC de Santa Catarina.
A rádio atlântida possui exibidores em diferentes locais físicos, que trabalham em conjunto. A comunicação entre estes exibidores é realizada por meio de mensagens seriais RS232. 
Todas as mensagens seriais recebidas são registradas neste log de eventos. 
Este programa verifica em tempo real o log para detectar problemas relacionados a erros de conexão, ou problemas de roteamento na cadeia.
Os problemas detectados serão encaminhados para uma plataforma de monitoramento Zabbix.

Segue o diagrama de funcionamento dos exibidores

| Exibidor |                      | Exibidor |                       | Exibidores  |
| POA      |--> Dados Seriais --> | Flops    | --> Dados Seriais --> | das praças  |
|          |       Puros          |          |     Identificados     | do interior |
     |                                                                     ^
      ------------------------- Dados Seriais Puros ------------------------

Uma chave nos exibidores do interior define quais Dados estão chegando (Dados Seriais Puros ou Dados Seriais Identificados)
O log nos permite descobrir se a chave está na posição correta, ou se existe um erro de conexão.

Etapas do projeto:
 - Desenvolvimento do arquivo de import de configurações 'config.ini';
 - Desenvolvimento da abertura do arquivo de log e tratamento das informações;
 - Desenvolvimento da engine Zabbix para envio dos alarmes;
 - Desenvolvimento do mecanismo inteligente para analise dos dados;
 - Desenvolvimento da Interface do Usuário;
 - Demais etapas ainda a serem definidas

Atualizações:
- Adicionada biblioteca parse-config que importa dados do arquivo de configurações config.ini
- Em curso o desenvolvimento do arquivo WRFileParser que importa os dados do arquivo de log.
