from datetime import datetime, timedelta

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
