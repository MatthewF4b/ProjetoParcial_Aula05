import random
import datetime

# -------------------------
# MENU
# -------------------------
def menu():
    nome = 'log.txt'

    while True:
        print('\nMENU')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar')
        print('4 - Sair')

        try:
            opc = int(input('Escolha: '))
        except:
            print('Entrada inválida')
            continue

        if opc == 1:
            qtd = int(input('Quantidade: '))
            gerar_logs(nome, qtd)

        elif opc == 2:
            analisar(nome)

        elif opc == 3:
            qtd = int(input('Quantidade: '))
            gerar_logs(nome, qtd)
            analisar(nome)

        elif opc == 4:
            print('Encerrando...')
            break


# -------------------------
# GERAÇÃO
# -------------------------
def gerar_data(i):
    base = datetime.datetime.now()
    return (base + datetime.timedelta(seconds=i*10)).strftime('%d/%m/%Y %H:%M:%S')

def gerar_ip(i):
    if 60 <= i <= 70:
        return '111.111.111.111'
    if 80 <= i <= 90:
        return '222.222.222.222'
    return f'{random.randint(1,200)}.{random.randint(1,200)}.{random.randint(1,200)}.{random.randint(1,200)}'

def gerar_recurso(i):
    if 60 <= i <= 70:
        return '/login'
    if i % 7 == 0:
        return '/admin'
    if i % 9 == 0:
        return '/backup'
    if i % 11 == 0:
        return '/config'
    if i % 13 == 0:
        return '/private'
    return '/home'

def gerar_metodo():
    return 'GET'

def gerar_status(i, recurso):
    if 60 <= i <= 70:
        return 403
    if 100 <= i <= 105:
        return 500
    if recurso == '/login' and i % 3 == 0:
        return 403
    if i % 10 == 0:
        return 404
    return 200

def gerar_tempo(i, status):
    if 30 <= i <= 40:
        return 100 + i*50
    if status == 500:
        return random.randint(800,1200)
    return random.randint(50,600)

def montar_log(i):
    data = gerar_data(i)
    ip = gerar_ip(i)
    recurso = gerar_recurso(i)
    metodo = gerar_metodo()
    status = gerar_status(i, recurso)
    tempo = gerar_tempo(i, status)

    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - 500B - HTTP/1.1 - Chrome - /home'

def gerar_logs(nome, qtd):
    with open(nome, 'w', encoding='utf-8') as f:
        for i in range(qtd):
            f.write(montar_log(i) + '\n')

    print('Logs gerados com sucesso!')


# -------------------------
# ANÁLISE
# -------------------------
def analisar(nome):

    f = open(nome, 'r', encoding='utf-8')

    total = sucesso = erros = erro500 = 0
    soma = maior = 0
    menor = 999999

    rapido = normal = lento = 0
    s200 = s403 = s404 = s500 = 0

    home = login = admin = backup = config = private = 0

    ultimo_ip = ''
    cont_ip = 0
    ip_top = ''
    ip_top_qtd = 0

    cont_ip_erro = 0
    ip_erro_top = ''
    ip_erro_qtd = 0

    cont_login = forca = 0
    ip_fb = data_fb = metodo_fb = recurso_fb = ''

    cont_admin = 0

    tempo_ant = 0
    cont_deg = degradacao = 0

    cont_500 = falha = 0

    cont_bot = bots = 0
    ultimo_bot = ''

    rotas = falhas_rotas = 0

    while True:
        linha = f.readline()
        if not linha:
            break

        total += 1
        i = 1

        # DATA
        data = ''
        while linha[i] != ']':
            data += linha[i]
            i += 1
        i += 2

        # IP
        ip = ''
        while linha[i] != ' ':
            ip += linha[i]
            i += 1
        i += 3

        # MÉTODO
        metodo = ''
        while linha[i] != ' ':
            metodo += linha[i]
            i += 1
        i += 3

        # STATUS
        status_str = ''
        while linha[i] != ' ':
            status_str += linha[i]
            i += 1
        status = int(status_str)
        i += 3

        # RECURSO
        recurso = ''
        while linha[i] != ' ':
            recurso += linha[i]
            i += 1
        i += 3

        # TEMPO
        tempo_str = ''
        while linha[i] != 'm':
            tempo_str += linha[i]
            i += 1
        tempo = int(tempo_str)

        soma += tempo

        if tempo > maior: maior = tempo
        if tempo < menor: menor = tempo

        if status == 200:
            sucesso += 1
            s200 += 1
        else:
            erros += 1

        if status == 403: s403 += 1
        if status == 404: s404 += 1
        if status == 500:
            s500 += 1
            erro500 += 1

        if tempo < 200: rapido += 1
        elif tempo < 800: normal += 1
        else: lento += 1

        if recurso == '/home': home += 1
        if recurso == '/login': login += 1
        if recurso == '/admin': admin += 1
        if recurso == '/backup': backup += 1
        if recurso == '/config': config += 1
        if recurso == '/private': private += 1

        # IP MAIS ATIVO
        if ip == ultimo_ip:
            cont_ip += 1
        else:
            cont_ip = 1

        if cont_ip > ip_top_qtd:
            ip_top_qtd = cont_ip
            ip_top = ip

        # IP COM MAIS ERROS
        if status != 200:
            if ip == ultimo_ip:
                cont_ip_erro += 1
            else:
                cont_ip_erro = 1

            if cont_ip_erro > ip_erro_qtd:
                ip_erro_qtd = cont_ip_erro
                ip_erro_top = ip

        # FORÇA BRUTA
        if ip == ultimo_ip and recurso == '/login' and status == 403:
            cont_login += 1
        else:
            cont_login = 1 if recurso == '/login' and status == 403 else 0

        if cont_login == 3:
            forca += 1
            ip_fb = ip
            data_fb = data
            metodo_fb = metodo
            recurso_fb = recurso

        # ADMIN
        if recurso == '/admin' and status != 200:
            cont_admin += 1

        # DEGRADAÇÃO
        if tempo > tempo_ant:
            cont_deg += 1
        else:
            cont_deg = 0

        if cont_deg == 3:
            degradacao += 1

        tempo_ant = tempo

        # FALHA CRÍTICA
        if status == 500:
            cont_500 += 1
        else:
            cont_500 = 0

        if cont_500 == 3:
            falha += 1

        # BOT
        if ip == ultimo_ip:
            cont_bot += 1
        else:
            cont_bot = 1

        if cont_bot == 5:
            bots += 1
            ultimo_bot = ip

        # ROTAS SENSÍVEIS
        if recurso == '/admin' or recurso == '/backup' or recurso == '/config' or recurso == '/private':
            rotas += 1
            if status != 200:
                falhas_rotas += 1

        ultimo_ip = ip

    f.close()

    disponibilidade = (sucesso/total)*100
    taxa = (erros/total)*100
    media = soma/total

    recurso_top = '/home'
    maior_rec = home

    if login > maior_rec: recurso_top, maior_rec = '/login', login
    if admin > maior_rec: recurso_top, maior_rec = '/admin', admin
    if backup > maior_rec: recurso_top, maior_rec = '/backup', backup
    if config > maior_rec: recurso_top, maior_rec = '/config', config
    if private > maior_rec: recurso_top = '/private'

    # ESTADO FINAL
    if falha > 0 or disponibilidade < 70:
        estado = 'CRITICO'
    elif disponibilidade < 85 or lento > normal:
        estado = 'INSTAVEL'
    elif disponibilidade < 95 or bots > 0:
        estado = 'ATENCAO'
    else:
        estado = 'SAUDAVEL'

    print('\n===== RELATÓRIO FINAL =====')
    print('Total acessos:', total)
    print('Sucessos:', sucesso)
    print('Erros:', erros)
    print('Erros críticos:', erro500)
    print('Disponibilidade:', round(disponibilidade,2))
    print('Taxa erro:', round(taxa,2))
    print('Tempo médio:', round(media,2))
    print('Maior tempo:', maior)
    print('Menor tempo:', menor)
    print('Rápidos:', rapido)
    print('Normais:', normal)
    print('Lentos:', lento)

    print('\nStatus:')
    print('200:', s200)
    print('403:', s403)
    print('404:', s404)
    print('500:', s500)

    print('\nRecurso mais acessado:', recurso_top)
    print('IP mais ativo:', ip_top)
    print('IP com mais erros:', ip_erro_top)

    print('\nForça bruta:')
    print('Total:', forca)
    print('Último IP:', ip_fb)
    print('Quando:', data_fb)
    print('Método:', metodo_fb)
    print('Recurso:', recurso_fb)

    print('\nAdmin indevido:', cont_admin)
    print('Degradação:', degradacao)
    print('Falha crítica:', falha)
    print('Bots:', bots)
    print('Último bot:', ultimo_bot)
    print('Rotas sensíveis:', rotas)
    print('Falhas rotas:', falhas_rotas)
    print('Estado final:', estado)


# EXECUÇÃO
menu()
