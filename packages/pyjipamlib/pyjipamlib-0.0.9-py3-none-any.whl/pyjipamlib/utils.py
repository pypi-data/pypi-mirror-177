from datetime import datetime, timedelta
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pymysql


class hora:
   """
   Retorna la Hora
   """

   def __init__(self):
      self.nada=0

   def get(self):
      """
      :return: la hora
      :rtype: string
      """
      return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   def hoy(self):
      """
      :return: la fecha actual
      :rtype: string
      """
      return datetime.now().strftime("%Y-%m-%d")

   def ayer(self):
      """
      :return: la fecha de ayer
      :rtype: string
      """
      today = datetime.today()
      yesterday = today - timedelta(days=1)
      return yesterday.strftime("%Y-%m-%d")

   def diasAtras(self,dias):
      """
      :return: la fecha de ayer
      :rtype: string
      """
      today = datetime.today()
      yesterday = today - timedelta(days=dias)
      return yesterday.strftime("%Y-%m-%d")

hora=hora()

class out:
   """
   escribe log modo append
   :param filename: nombre del archivo
   :type filename: string
   """

   def __init__(self,filename='/dev/null'):
      self.filename = filename

   def log(self,text):
      """
      :param text: texto a escribir
      :type text: string
      """
      horax=hora.get()
      f = open(self.filename, "a")
      f.write(horax + "; " + text + "\n")
      f.close()

   def print(self,text):
      """
      :param text: texto a imprimir
      :type text: string
      """
      horax=hora.get()
      print(horax + "; " + text)

outx=out()

class mysql:
   """
   queries mysql db
   :param servidor: ip
   :type servidor: string

   :param user: user
   :type user: string

   :param pass: ip
   :type pass: string

   :param db: ip
   :type db: string
   """

   def __init__(self,servidorx,userx,passx,dbx):
      self.servidorx=servidorx
      self.userx=userx
      self.passx=passx
      self.dbx=dbx

   def mysqlQueryRe(self,q,intentos=3,sleepStep=1):
      looper=0
      intentos=int(intentos)
      valid=False
      while looper < intentos:
          if looper>1:
              time.sleep(sleepStep*looper)
          looper+=1
          try:
              df=self.mysqlQuerySilent(q)
              if isinstance(df, pd.DataFrame):
                  valid=True
                  break
          except Exception as e:
              falla='Err mysql; Check Install sqlalchemy pymysql pandas ;'+str(e)
              out().print(falla)
              nada=0

      if(valid):
        out().print('intentos:' + str(looper) + '; df.shape:' + str(df.shape) )
        return {'result':1,'data':df}
      else:
        out().print('Err mysql; intentos:' + str(looper) )
        return {'result':0,'data':pd.DataFrame()}


   def mysqlQuerySilent(self,query):
      df='err:'
      try:
         sqlEngine       = create_engine('mysql+pymysql://'+self.userx+':'+self.passx+'@'+self.servidorx)
         dbConnection    = sqlEngine.connect()
         frame           = pd.read_sql(query, dbConnection);
         dbConnection.close()
         return frame
      except OperationalError as e:
         out().print('Err mysql; ' + str(e))
         return ''
      except Exception as e:
         out().print('Err mysql; ' + str(e))
         return ''
      finally:
         dbConnection.close()
