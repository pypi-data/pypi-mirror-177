
# The organization on charge of this project is SIRIUS Technologies.
# This version still works. But you need to review /json/cache.json and see "seq", "nosso_nr".
# These values need to follow the last incomming file. 
# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# ! >---------->IMPORT>---------->
import os
import json
from datetime import date
from typing import Sequence
import pandas as pd
from reg import pick_log
import reg


# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# * >---------->PRESSETS>---------->


_cache = open('json/cache.json', 'r')
cache_df = json.load(_cache)
_cache.close()

# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# ! >---------->OBJ_MODEL>---------->

reg_cod = "4"
nota_blank = ""

f_name = "4OU"
f_seq = cache_df['seq']
# header

header = {
    "cod_red": "0",
    "cod_rem": "1",
    "literal_rem": "REMESSA",
    "cod_serv": "01",
    "literal_serv": "COBRANCA",
    "cod_empresa": "190600183281600",
    "nome_empresa": "BEAUTY SUPPLY COSMETICOS SOCIE",
    "cod_banco": "707",
    "nome_banco": "BANCO DAYCOVAL",
    "record_date": '',
    "blank": "",
    "seq": 1
}

# titulos
tit_reg_cod = "1"
insc_cod = "02"
insc_nr = "34362718000140"
empresa_cod = "190600183281600"
empresa_uso = ""  # TODO Descontinuado
nosso_nr = "xxxxxxxx"
tit_blank1 = ""
banco_uso = ""
rem_cod = "6"
occurrence_cod = "01"
seu_nr = cache_df['nosso_nr']
vencimento = ""
tit_val = ""
banco_cod = "707"
ag_colletor = "0000"
ag_colletor_dac = "0"
especie = "01"
aceite = "N"
tit_emissao = ""
tit_blank2 = "00"
tit_blank3 = "00"
tit_1_day = "0000000000000"
discount_since = "000000"
discount_val = "0000000000000"
banco_uso2 = "0000000000000"
abatimento_val = "0000000000000"
insc_cod2 = ""
tit_cpf_cnpj = ""
tit_nome = ""
tit_blank4 = ""
tit_logradouro = ""
tit_bairro = ""
tit_cep = ""
tit_cidade = ""
tit_estado = ""
tit_sacador_avalista = "BEAUTY SUPPLY C S U LTDA"
tit_blank5 = ""
tit_blank6 = ""
tit_prazo = "00"
tit_coin = "0"
seq = 2
_seq = 3

# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# TODO >---------->FUNCTIONS>---------->


def rpl_clear(col):
    col = col.replace('/', '').replace('.', '').replace(',',
                                                        '').replace(':', '').replace('-', '')
    return col

        
def rpl_year(col):
    col = col.replace('/2021', '/21').replace('/2022', '/22').replace('/2023',
                                                                        '/23').replace('/2024', '/24').replace('/2025', '/25')
    return col


def rpl_acento(col):
    col = col.replace('Ã', 'A').replace('Õ', 'O').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('Ä', 'A').replace('Ë', 'E').replace('Ï', 'I').replace('Ö', 'O').replace('Ü', 'U').replace('ã', 'a').replace(
        'á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('À', 'A').replace('È', 'E').replace('Ì', 'I').replace('Ò', 'O').replace('Ù', 'U').replace('à', 'a').replace('è', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u')
    return col

# Essa função é particular pq eu tenho preguiça de ficar fazendo print

def show_me(p):
    return print(p)


def get_ev4():
    ev4 = pd.read_excel('xcel/ev4.xlsx', sheet_name='f.ev4')

    conve = list(ev4['valor'])
    b = []
    for i in range(len(conve)):
        b.append(f'{conve[i]:.2f}')
    for i in range(len(b)):
        conve[i] = str(b[i].replace('.', ''))
    conve = pd.DataFrame(conve)
    ev4['valor'] = conve

    ev4['dt_vencimento'] = ev4['dt_vencimento'].apply(rpl_year)
    ev4['dt_vencimento'] = ev4['dt_vencimento'].apply(rpl_clear)
    ev4['cpf_cnpj'] = ev4['cpf_cnpj'].apply(rpl_clear)
    ev4['cep'] = ev4['cep'].apply(rpl_clear)
    ev4['emissao'] = ev4['emissao'].apply(rpl_year)
    ev4['emissao'] = ev4['emissao'].apply(rpl_clear)
    ev4['valor_total'] = ev4['valor_total'].apply(rpl_clear)
    ev4['nome'] = ev4['nome'].apply(rpl_acento)
    return ev4


def get_df_titulo():
    titulo = load_df(titulos_)
    titulo['valor'] = titulo['valor'].apply(rpl_clear)
    titulo['dt_vencimento'] = titulo['dt_vencimento'].apply(rpl_clear)
    titulo['cpf_cnpj'] = titulo['cpf_cnpj'].apply(rpl_clear)
    titulo['cep'] = titulo['cep'].apply(rpl_clear)
    pick_log(str(titulo))
    return titulo


def titulo_format():
    p = get_df_titulo()
    numero_split = p['numero'].str.split('/')
    pick_log(str(numero_split))
    numero_main = numero_split.str.get(0)
    pick_log(str(numero_main))
    numero_parcela = numero_split.str.get(1)
    pick_log(str(numero_parcela))
    p['numero'] = numero_main
    p['parcela'] = numero_parcela
    pick_log(str(p))
    return p


def df_toList(_):
    _x = _.tolist()
    return _x


# def nota_value_list():
#     nota = get_df_nota()
#     val = nota['valor_total'].tolist()
#     return val


# def nota_cod_list():
#     nota = get_df_nota()
#     cod = nota['numero'].tolist()
#     return cod


# def nota_date_list():
#     nota = get_df_nota()
#     date = nota['emissao'].tolist()
#     return date


# def nota_key_list():
#     nota = get_df_nota()
#     key = nota['key'].tolist()
#     return key


def cod_ins(p):
    z = ""
    z = len(p)
    z = int(p)
    if z >= 14:
        _ = "02"
    else:
        _ = "01"

    return _


# ! MÓDULO DE ITERAÇÃO DINÂMICO

def bl_sd(p):
    return p == "r"


def lado_b(p):
    if bl_sd(p):
        return 1
    else:
        return 0


def iter_f(a, p, l, t):

    if t == "0":
        fill = "0"
    else:
        fill = " "

    lado = lado_b(l)

    if lado == 1:

        r4nge = p

        a = a
        i = len(str(a))
        z = 0

        if i > r4nge:
            z = i - r4nge
            a = a[:-z]
            return(a)

        else:
            z = r4nge - i
            fill = fill*z
            a = str(a) + fill
            return(a)

    elif lado == 0:

        r4nge = p

        a = a
        i = len(str(a))
        z = 0

        if i > r4nge:
            z = i - r4nge
            a = a[:-z]
            return(a)

        else:
            z = r4nge - i
            fill = fill*z
            a = fill + str(a)
            return(a)

# ! (FIM) MÓDULO DE ITERAÇÃO DINÂMICO

# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# ! >---------->PROCEED>---------->

# HEADER


rem = ""
rem += header["cod_red"]
rem += header["cod_rem"]
rem += header["literal_rem"]
rem += header["cod_serv"]
rem += iter_f(header["literal_serv"], 15, "r", "1")
rem += iter_f(header["cod_empresa"], 20, "r", "1")
rem += iter_f(header["nome_empresa"], 30, "r", "1")
rem += header["cod_banco"]
rem += iter_f(header["nome_banco"], 15, "r", "1")
rem += reg.date_today_i()
rem += iter_f(header["blank"], 294, "r", "1")
rem += iter_f(str(header["seq"]), 6, "l", "0")
rem += "\n"
header["seq"] = header["seq"] + 1
show_me(rem)

ev4 = get_ev4()

ev_valor = df_toList(ev4['valor'])
print(ev_valor)
ev_dt_vencimento = df_toList(ev4['dt_vencimento'])
ev_cpf_cnpj = df_toList(ev4['cpf_cnpj'])
ev_nome = df_toList(ev4['nome'])
ev_numero = df_toList(ev4['numero'])
ev_endereco = df_toList(ev4['endereco'])
ev_numero1 = df_toList(ev4['numero1'])
ev_cep = df_toList(ev4['cep'])
ev_bairro = df_toList(ev4['bairro'])
ev_cidade = df_toList(ev4['cidade'])
ev_uf = df_toList(ev4['uf'])
ev_descricao = df_toList(ev4['descricao'])
ev_valor_total = df_toList(ev4['valor_total'])
ev_emissao = df_toList(ev4['emissao'])
ev_key = df_toList(ev4['key'])

tran = ""
tran_range = len(ev_key)
tran_range = int(tran_range)
i = 0
tran = ""

for i in range(tran_range):
    tran += tit_reg_cod
    tran += insc_cod
    tran += insc_nr  # TODO CNPJ
    # TODO CODIGO DA EMPRESA NO BANCO
    tran += iter_f(empresa_cod, 20, "r", "1")
    tran += iter_f(empresa_uso, 25, "r", "1")  # TODO branco
    tran += iter_f(str(seu_nr), 8, "r", "1")
    seu_nr = seu_nr + 1
    tran += iter_f(tit_blank1, 13, "r", "1")
    tran += iter_f(banco_uso, 24, "r", "1")
    tran += rem_cod
    tran += occurrence_cod
    tran += iter_f(ev_numero[i], 10, "r", "1")
    tran += iter_f(ev_dt_vencimento[i], 6, "r", "1")
    tran += iter_f(ev_valor[i], 13, "l", "0")
    tran += banco_cod
    tran += ag_colletor
    tran += ag_colletor_dac
    tran += especie
    tran += aceite
    tran += iter_f(ev_emissao[i], 6, "r", "1")
    tran += tit_blank2
    tran += tit_blank3
    tran += tit_1_day
    tran += discount_since
    tran += discount_val
    tran += banco_uso2
    tran += abatimento_val
    tran += cod_ins(ev_cpf_cnpj[i])
    tran += iter_f(ev_cpf_cnpj[i], 14, "l", "0")
    tran += iter_f(ev_nome[i], 30, "r", "1")
    tran += iter_f(tit_blank4, 10, "r", "1")
    tran += iter_f(ev_endereco[i], 40, "r", "1")

    tran += iter_f(ev_bairro[i], 12, "r", "1")
    tran += ev_cep[i]
    tran += iter_f(ev_cidade[i], 15, "r", "1")
    tran += ev_uf[i]
    tran += iter_f(tit_sacador_avalista, 30, "r", "1")
    tran += iter_f(tit_blank5, 4, "r", "1")
    tran += iter_f(tit_blank6, 6, "r", "1")
    tran += tit_prazo
    tran += tit_coin
    tran += iter_f(str(seq), 6, "l", "0")
    seq = seq + 2
    tran += "\n"
    tran += reg_cod
    tran += iter_f(ev_numero[i], 15, "r", "1")
    tran += iter_f(ev_valor_total[i], 13, "l", "0")
    tran += iter_f(f'{ev_emissao[i][:4]}20{ev_emissao[i][-2:]}', 8, "r", "1")   
    tran += iter_f(ev_key[i], 44, "r", "0")
    tran += iter_f(nota_blank, 313, "r", "1")
    tran += iter_f(str(_seq), 6, "l", "0")
    _seq = _seq + 2
    tran += "\n"

trailler = ''
trailler += '9'
trailler += iter_f("", 393, "r", "1")
trailler += iter_f(str(_seq-1), 6, "l", "0")
tran += trailler

_nrFile = f_name + str(reg.date_today_rm()) + str(f_seq) + ".TXT"
f_seq = f_seq + 1
_cache = open('json/cache.json', 'w')
cache_df['seq'] = f_seq
cache_df['nosso_nr'] = seu_nr
json.dump(cache_df, _cache)
_cache.close()
with open(f'{os.environ["homepath"]}/Desktop/CONV2REM/files/{_nrFile}', "x", encoding="utf-8") as n_rem:

    n_rem.write(rem)
    n_rem.write(tran)
    n_rem.close()


# ? >---------->---------->---------->---------->---------->---------->---------->---------->---------->----------]
# TODO >---------->NOTES>---------->
