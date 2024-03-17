# Criador         : Brayan vieira 
# função          : Um sistema de consulta de cnpj 
# versão          : 1.2
# data da criação : 24/2/2024
# Notas           : 1.1 Correção de erros e melhoria de instabilidade
# Notas           : 1.2 Adicionando interface Gráfica
import requests
import flet as ft
cnpj_global = ""
API = ""
texto1 = ""
#                           Realizando a requisição para a api 
#__________________________________________________________________________________
def realizar_requisicao_api():
     global API
     valor_nulo = 0
     requisicao = requests.get(API)
     codigo_da_requisicao = requisicao.status_code
     if codigo_da_requisicao == 200:
        dados_totais = requisicao.json()
        for indices, informacoes in dados_totais.items():
                if indices == "atividade_principal": # Testando valores e limpando 
                    for total in informacoes:
                        texto1.value += f" {indices} : {total['text']} \n "
                elif indices == "atividades_secundarias":
                        for total in informacoes:
                            texto1.value += f" Atividade Secundaria da empresa : {total['text']} \n"
                elif indices == "qsa":
                    for total in informacoes:
                            texto1.value += f" funcionario : {total['nome']}  Cargo : {total['qual']} \n "
                elif informacoes == '' or indices == 'billing' or indices == 'extra': # Removendo valores nulos 
                        valor_nulo += 1
                else:
                        texto1.value += f"{indices} : {informacoes} \n "
     elif codigo_da_requisicao == 404:
           texto1.value += "Erroo com a api tente mais tarde "
     elif codigo_da_requisicao == 504:
           texto1.value += "erro tente novamente mais tarde "
#__________________________________________________________________________________
#                           pagina principal 
def pagina(pagina: ft.Page):
    pagina.title = "Consultar cnpj "
    pagina.window_width = 450
    pagina.window_height = 350
#           validando o cnpj
    def testar_cnpj(e):
         total = len(cnpj.value)
         try:
              a = int(cnpj.value)
         except ValueError:
              texto.value = "Insira somente numeros"
              pagina.update()
              return False
         if total < 10:
              texto.value = "CNPJ inválido" 
              pagina.update()
              return False
         if not cnpj.value:
              texto.value = "CNPJ inválido"
              pagina.update()
              return False
         if total > 17:
              texto.value = "CNPJ inválido"
              pagina.update()
              return False
         return True
    def epol(e):
        if testar_cnpj(None): #configurando o CNPJ
            global cnpj_global 
            global API
            cnpj_global = cnpj.value
            API = f"https://receitaws.com.br/v1/cnpj/{cnpj_global}"
            pagina.window_close()
    cnpj = ft.TextField(hint_text="Insira o CNPJ que deseja consultar ", )
    texto = ft.Text(value="Insira o CNPJ sem os caracteres especiais  [ . / - ] ")
    botao_consultar = ft.TextButton(text="Consultar", on_click=lambda e: epol(None))
    pagina.add(
    ft.Row([cnpj, botao_consultar]),
    ft.Row([texto])
    )
ft.app(target=pagina)
#                       Pagina de consulta 
if cnpj_global:
    def page01(pagina: ft.Page):
        pagina.window_width = 950
        pagina.window_height = 900
        global texto1
        global cnpj_global
        pagina.title = "Consulta do CNPJ"
        texto1 = ft.Text(value=f"Resultado da consulta do CNPJ Número : {cnpj_global} ")
        realizar_requisicao_api()
        pagina.add(
            ft.Row([texto1])
               
                
                )    

    ft.app(target=page01)

