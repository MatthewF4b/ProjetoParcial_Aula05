import random
import datetime

def menu():
    nome_arquivo = 'log.txt'
    while True:
        print('MENU\n')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e Analisar logs')
        print('4 - Sair')
        opc = int(input('Escolha uma opção: '))
        if opc == 1:
            try:
                qtd = int(input('Insira a quantidade de log (registros): '))
                gerarArquivo(nome_arquivo, qtd)
            except:
                print('Entrada inválida.')
        elif opc == 2:
            analisarLogs(nome_arquivo)
        elif opc == 3:
            try:
                qtd = int(input('Insira a quantidade de log (registros): '))
                gerarArquivo(nome_arquivo,qtd)
                analisarLogs(nome_arquivo)
            except:
                print('Entrada inválida.')
        elif opc == 4:
            print('Até mais')
            break
        else:
            print('Opção inválida')

def gerarArquivo(nome_arquivo, qtd):
    with open(nome_arquivo, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    print('Log gerado')

def montarLog(i):
    data    = gerarData(i)
    ip      = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo  = gerarMetodo(i)
    status  = gerarStatus(i)
    tempo   = gerarTempo(i)
    agente  = gerarAgente(i)
    protocolo = gerarProtocolo(i)
    tamanho = gerarTamanho(i)
    return f'[{data}] {ip} | {metodo} | {status} | {recurso} | {tempo}ms | {tamanho} | {protocolo} | {agente} | /home'

def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds= i * random.randint(5,30))
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    r = random.randint(1,6)
    if i >= 20 and i <= 50:
        return '203.120.45.7'
    else:
        return f'{random.randint(10,200)}.{random.randint(100,200)}.{random.randint(0,250)}.{random.randint(1,250)}'