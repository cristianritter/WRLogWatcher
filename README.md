# WRLogWatcher
Este projeto é um sistema desenvolvido em Python que realizará o monitoramento dos arquivos de Log (registro de operações) do exibidor de comerciais das rádios do grupo NSC de Santa Catarina.
A rádio atlântida possui exibidores em diferentes locais físicos, que trabalham em conjunto. A comunicação entre estes exibidores é realizada por meio de mensagens seriais RS232. 
Todas as mensagens seriais recebidas são registradas neste log de eventos. 
Este programa verifica em tempo real o log para detectar problemas relacionados a erros de conexão, ou problemas de roteamento na cadeia.
Os problemas detectados serão encaminhados para uma plataforma de monitoramento Zabbix.

São utilizados sincronizadores de tempo NTP em todas as maquinas, e os erros sao verificados por meio de analise do timestamp de registros dos logs.

Uma chave nos exibidores do interior define o roteamento dos disparos recebidos e enviados
A analise executada deste aplicativo nos permite descobrir se a chave está na posição correta e se os disparos estão sendo recebidos corretamente.

Etapas do projeto:
 - Desenvolvimento do arquivo de import de configurações 'config.ini'; OK
 - Desenvolvimento da abertura do arquivo de log e tratamento das informações; OK
 - Desenvolvimento da engine Zabbix para envio dos alarmes; OK
 - Desenvolvimento do mecanismo inteligente para analise dos dados; OK
 - Desenvolvimento da Interface do Usuário; OK
 - Demais etapas ainda a serem definidas

Atualizações:
- Adicionada biblioteca parse-config que importa dados do arquivo de configurações config.ini
- Em curso o desenvolvimento do arquivo WRFileParser que importa os dados do arquivo de log.
- Concluida versão inicial do arquivo WRFileParser que retorna como resultado a última linha do log contendo a Flag ou retorna 0 se não for encontrada
- Concluida a versão inicial do arquivo WRZabbixSender que envia as métricas para o Zabbix.
- Concluido o desenvolvimento da interface do usuario no arquivo user_interf.py
- Iniciado o desenvolvimento do loop main no arquivo WRMain.py
- Alteradas biblotecas WRAnalizer e WRUserInterf para uso como classes, resolvido erro com WxLocale substituindo o metodo LocaleInit
- Criado arquivo de teste para operacoes em tempo real no log do winradio (finalizado com sucesso sem causar erros no sistema)
- Alteração do sistema para permitir a configuração de multiplas praças 
- Alterado sistema config e bibliotecas
- Sistema multiframe concluido em branch multiframe
- Migrados todos os frames para main
- Alterações de documentação, adicionadas informações de autor e descrição das funções


Pendentes:
 - Alterar todas as bibliotecas para uso como classes (resolvido)
 - Realizar o parsing dos logs em duas funções, uma trazendo somente texto e outra trazendo a lista com o resultado (resolvido)
 - Resolver problema com wx task relacionado ao locale (resolvido)
 - Comentar as funcoes e adicionar as descricoes (WRUserInterf.py->OK, WRZabbixSender.py->OK, ) resolvido
 - Elaborar e integrar icones da interface de usuario (resolvido)
 - Testes pré produção
 - fix para erro que informa erro de interpretação caso o tamanho das listas nao seja igual (resolvido)
