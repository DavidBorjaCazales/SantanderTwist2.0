#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import nltk
from nltk.corpus import stopwords
from math import log
import random
import sys
from nltk.stem.snowball import SnowballStemmer
reload(sys)
sys.setdefaultencoding("ISO-8859-1")


def getCon():
        _conn = pymysql.connect(host='174.143.111.53', port=3306, user='root', passwd='i1vpoLfaVDVL', db='santandertwist', use_unicode=True, charset="utf8")

        _cur = _conn.cursor()
        _cur.execute('SET NAMES utf8;')
        _cur.execute('SET CHARACTER SET utf8;')
        _cur.execute('SET character_set_connection=utf8;')

        res = []
        res.append(_cur)
        res.append(_conn)

        return res

class Buscador:
    
 """
  clase la cual contiene el algoritmo Buscacor
 """
       
 
 def Buscar(self,patron):
  
  """
   En este paratado tenemos el algoritmo para buscar en tryme.
  """
  
  CadenaSQLUno=""""""
  CadenaSQLDos=""""""
  CadenaSQLTres=""""""
  CadenaSQLCuatro=""""""
  TerminosRelevantesUsuario=[]
  TokensPatron=nltk.word_tokenize(patron.lower())
  StopWordsSpanish=stopwords.words('spanish')
  TokensPatronTemporal=[]

  for b in TokensPatron:
   IsStopWord=False
   for a in StopWordsSpanish:
    if(a.lower()==b.lower()):
     IsStopWord=True
   if not(IsStopWord):
    TokensPatronTemporal=TokensPatronTemporal+[b]

  TokensPatron=TokensPatronTemporal

  stemmer = SnowballStemmer("spanish",ignore_stopwords=False)
  SinRuidoPatron=[]
  SinRuidoPatron= [stemmer.stem(a) for a in TokensPatron]

  i=0  
  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQLUno=CadenaSQLUno+"lower(campaign_name) like '%"+SinRuidoPatron[i]+"%' and "
   i=i+1
 
  if (len(SinRuidoPatron)>0):
   CadenaSQLUno=CadenaSQLUno+"lower(campaign_name) like '%"+SinRuidoPatron[len(SinRuidoPatron)-1]+"%' "

  CadenaSQLUno="("+CadenaSQLUno+")"

  i=0  
  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQLDos=CadenaSQLDos+"lower(title) like '%"+SinRuidoPatron[i]+"%' and "
   i=i+1
 
  if (len(SinRuidoPatron)>0):
   CadenaSQLDos=CadenaSQLDos+"lower(title) like '%"+SinRuidoPatron[len(SinRuidoPatron)-1]+"%' "

  CadenaSQLDos="("+CadenaSQLDos+")"


  i=0  
  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQLTres=CadenaSQLTres+"lower(home) like '%"+SinRuidoPatron[i]+"%' and "
   i=i+1
 
  if (len(SinRuidoPatron)>0):
   CadenaSQLTres=CadenaSQLTres+"lower(home) like '%"+SinRuidoPatron[len(SinRuidoPatron)-1]+"%' "

  CadenaSQLTres="("+CadenaSQLTres+")"

  i=0  
  while(i<(len(SinRuidoPatron)-1)):
   CadenaSQLCuatro=CadenaSQLCuatro+"lower(paragraph) like '%"+SinRuidoPatron[i]+"%' and "
   i=i+1
 
  if (len(SinRuidoPatron)>0):
   CadenaSQLCuatro=CadenaSQLCuatro+"lower(paragraph) like '%"+SinRuidoPatron[len(SinRuidoPatron)-1]+"%' "

  CadenaSQLCuatro="("+CadenaSQLCuatro+")"



  QueryString= "select campaign_id,campaign_name,title,home,paragraph from campaigns where ("+CadenaSQLUno+" or "+CadenaSQLDos+" or  "+CadenaSQLTres+" or "+CadenaSQLCuatro+")"

  _con = getCon()

  rows = _con[0]

  try:
   rows.execute(QueryString)
   
  
   Busquedas=[]

   for row in rows:
    DimensionalidadDocumento=DimensionalidadDocumento+1.0
    Codificacion= (row[1].lower())+" "+(row[2].lower())+" "+(row[3].lower())+" "+(row[4].lower())
    Codificacion= Codificacion.replace(".", "")
    Codificacion= Codificacion.replace("-", "")
    Codificacion= Codificacion.replace(":", "")
    Codificacion= Codificacion.replace(",", "")
    Codificacion= Codificacion.replace("?", "")
    Codificacion= Codificacion.replace("!", "")

    Tokens=nltk.word_tokenize(Codificacion)
    TokensTemporal=[]

    for b in Tokens:
     IsStopWord=False
     for a in StopWordsSpanish:
      if(a.lower()==b):
       IsStopWord=True
     if not(IsStopWord):
      TokensTemporal=TokensTemporal+[b]

    Tokens=TokensTemporal
    Frecuencia=[0.0]*len(TokensPatron)

    i=0
    for a in TokensPatron:
     for b in Tokens:
      if(a in b):
       Frecuencia[i]=Frecuencia[i]+1.0
     i=i+1
    
    Busquedas=Busquedas+[[row[0],row[1],row[2],row[3],row[4],Frecuencia]]

   
   TemBusqueda=[]

   i=0
   while i <len(Busquedas):
    Busquedas[i][5]=sum(Busquedas[i][5])
    i=i+1

  
   Busquedas.sort(key=lambda x: x[5],reverse=True)
   
   Busquedas=[ [a[0],a[5]] for a in Busquedas]

   for a in Busquedas:
    if (a[1]>0):
     TemBusqueda=TemBusqueda+[a[0]]

   _con[0].close()
   _con[1].close()
  
   return  TemBusqueda

  except:
   _con[0].close()
   _con[1].close()
   return [] 
 
  """ 

  NDT=[1.0]*len(SinRuidoPatron)   
  MaquinaEstadosNDT=['0']*len(SinRuidoPatron)
  DimensionalidadDocumento=0.0

  for row in rows: 
   DimensionalidadDocumento=DimensionalidadDocumento+1.0
   Codificacion=row[1].encode('utf-8').strip()
   Codificacion=Codificacion.replace('"',"")
   Codificacion=Codificacion.lower()
   TokensMedoide=nltk.word_tokenize(Codificacion)
   SinRuidoMedoide=[]
   SinRuidoMedoide= [stemmer.stem(b) for b in TokensMedoide]
   Frecuencia=[0.0]*len(SinRuidoPatron)
   i=0
   
  
   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if (a==b):
      if(MaquinaEstadosNDT[i]=='0'):
       NDT[i]=NDT[i]+1
       MaquinaEstadosNDT[i]='a'
    MaquinaEstadosNDT[i]='0'        
    i=i+1
  
   i=0
   for a in SinRuidoPatron:
    for b in SinRuidoMedoide:
     if(a==b):
      Frecuencia[i]=Frecuencia[i]+1.0
    i=i+1 


   ListaDeClasificacion=ListaDeClasificacion+[[row[0],Codificacion,Frecuencia,row[2],row[3]]]
  
 
  i=0
  while i <len(ListaDeClasificacion):
   j=0
   while (j<len(NDT)):
    TF=ListaDeClasificacion[i][2][j]
    IDF=(log(DimensionalidadDocumento/NDT[j]))
    TF_IDF=(TF*IDF)
    ListaDeClasificacion[i][2][j]=TF_IDF
    j=j+1
   i=i+1
  
  i=0
  while i < len(ListaDeClasificacion):
   j=0
   Suma=0.0
   while j < len(ListaDeClasificacion[i][2]):
    Suma=(Suma+ListaDeClasificacion[i][2][j])       
    j=j+1 

   PesoMarca= GetValue(ListaDeClasificacion[i][4],marcasproductos)
   ListaDeClasificacion[i][2]=(Suma*PesoMarca)
   i=i+1

  ListaDeClasificacion.sort(key=lambda x: x[2],reverse=True)
  
  ListaDeClasificacion=ListaDeClasificacion[:Phi]
  ListaDeClasificacion=[[a[0],a[1],len([stemmer.stem(aa)  for aa in nltk.word_tokenize(a[1])]),a[3]] for a in ListaDeClasificacion]
  BloqueDePrecios=[a[2] for a in ListaDeClasificacion]
  BloqueDePrecios=sorted(list(set(BloqueDePrecios)))
  
  ListaBucketSort=[]   

  for a in BloqueDePrecios:
   bucket=[]
   for b in ListaDeClasificacion:
    if (a == b[2]):
     bucket=bucket+[[b[0],b[1],b[3]]]
   bucket.sort(key=lambda x: x[2])
   ListaBucketSort=ListaBucketSort+bucket

  ListaBucketSort=[a[0] for a  in ListaBucketSort]
    
  #Apartado Final para el programador 
  #return  ListaBucketSort

  # Apartado modificado  por el cliente  
  CadenaListaBucketSort=str(ListaBucketSort)
  CadenaListaBucketSort=CadenaListaBucketSort.replace("[","")
  CadenaListaBucketSort=CadenaListaBucketSort.replace("]","")
  CadenaListaBucketSort="("+CadenaListaBucketSort+")"
  CadenaListaBucketSort=CadenaListaBucketSort.replace("u","")   
  QueryString="select id_producto, producto ,precio_limpio,marcasitio from producto where (id_producto in "+CadenaListaBucketSort+")"
  _con = getCon()
  
  rows = _con[0]
  rows.execute(QueryString)
  ResultadoFinal=[]

  for row in rows:
   id_producto=row[0]
   producto=row[1]
   precio=row[2]
   marcasitio=row[3]
   ResultadoFinal=ResultadoFinal+[[id_producto,producto,precio,marcasitio]]
  
  _con[0].close()
  _con[1].close()

  return  ResultadoFinal
  
  """  
  
 
  # Fin de Apartado modificado por el cliente  


