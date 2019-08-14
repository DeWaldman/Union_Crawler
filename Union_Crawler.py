from bs4 import BeautifulSoup as bs
import mysql.connector
from selenium import webdriver
#import Union_Crawler_DataBase as miojao
from time import sleep

login=input('Login: ')
mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="mangazada")

def raspaCap(manga,sopa_linda):
  #pega as tags que tem a os capitulos (class:col-xs-6 col-md-6);
  cap=str(sopa_linda.findAll('div',{'class':'col-xs-6 col-md-6'})).lower()
  manga=manga.lower().replace(" ","_")
  #recebe a tag com o capitulo, assim conseguimos pegar o numero do capitulo contido no link da tag <a> dentro de <div>
  cap = cap[cap.find(manga):cap.find(manga)+len(manga)+5]
  #tratando a informação; caso venha algo desnecessario
  cap=cap.replace(manga,"")
  cap=cap.replace("/","")
  cap=cap.replace(">","")
  cap=cap.replace('"','')
  return cap

def procuraLogin():
  mycursor = mydb.cursor()
  mycursor.execute('select nome_usuario from teste')
  myresult = mycursor.fetchall()
  if login not in str(myresult):
    "vc ñ tem login ;~;"
    inserirManga()
    return "vc nunca vera essa mensagem q-p"
  else:
    return f"youkoso {login}-san ^-^"
  
def listaMangas(listaAp=""):
  mycursor = mydb.cursor()
  mycursor.execute(f'select nome_manga from teste where nome_usuario="{login}"')
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)
    listaAp+=f'{x}>'
  listaAp=listaAp.replace("'","").replace("[","").replace("]","").replace(",","").replace("(","").replace(")","").replace("'\'","").lower()
  listaAp=listaAp.split(">")
  return listaAp[:-1]
  
def inserirManga():
  myinsert= mydb.cursor()
  sql=f'INSERT INTO teste (nome_usuario, nome_manga) VALUES ("{login}","{input("Qual manga esta acompanhando agora? ").lower()}")'
  myinsert.execute(sql)
  mydb.commit()
  return "vc esta cada vez mais otaku XD"
 
def site_magazada_html():
  raposa_fogo = webdriver.Firefox()# inicia uma instancia
  raposa_fogo.get('https://unionmangas.top/')
  html_site = raposa_fogo.page_source #esse é a variavel com o html do site
  #Esse while é para pegar o codigo fonte com os dados sobre os mangas de hoje ( ^ _ ^)
  #Temos um problema com essa condicao: nós presumimos que averá alguma palavra 'ontem' no site, se não tiver ficaremos para sempre nesse loop :(
  while html_site.find('Ontem') == -1:
    botao_verMais = raposa_fogo.find_element_by_id('linha-botao-mais')#ID name do botao maluko: 'linha-botao-mais';
    botao_verMais.click()#Ao clicar no botao chama uma funçao 'paginacaoNoticias()' no condigo do site 
    html_site = raposa_fogo.page_source
    #raposa_fogo.close()
    sleep(7)
  return html_site

#selecionando os mangas lançados á partir de "hoje" até onde ainda tem;
html_site = site_magazada_html()
lista_html = html_site[html_site.find('Hoje'):html_site.find('Ontem')]
menu=0
procuraLogin()
while menu !=3:
  menu=int(input("\n1.para adicionar manga\n2.para consultar os mangas\n3.para fechar:\n"))
  if menu==1:
    while menu != 2:
      print(inserirManga())
      menu=int(input("deseja adicionar mais?\n1. para sim :3\n2. para não >-<\n"))
    #se não for mais adicionar mangas, então partiu consulta;
    menu=2
  if menu==2:
    #transforma a "lista" em uma lista de um modo organizado pelos parametros do bs4, para fazer um busca usando o .findALL()
    sopa_linda = bs(lista_html, 'html.parser')
    manga_lista=listaMangas()
    for manga in manga_lista:
      #se o manga NAO nao estiver na lista_html(saida==-1),entao saiu;
      if not str(sopa_linda.findAll('a',{'class':'link-titulo'})).lower().find(manga) == -1:
        print('saiu: {}, no capitulo {} ^=^'.format(manga.capitalize(),raspaCap(manga,sopa_linda)))
      else: print('nao saiu {} ;-;'.format(manga.capitalize()))
  else:print("seu login ainda não existe :(\nDigite uma entrada válida ¬¬")
print("obg pela preferencia XD")


