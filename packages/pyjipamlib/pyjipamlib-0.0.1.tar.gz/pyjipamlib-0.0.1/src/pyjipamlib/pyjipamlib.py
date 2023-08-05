from datetime import datetime
class Ahora:
   """
   Retorna la Hora
   """

   def __init__(self):
      self.nada=0

   def now(self):
      """
      :return: la hora
      :rtype: string
      """

      return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ToLog:
   """
   escribe log modo append
   :param filename: nombre del archivo
   :type filename: string
   """

   def __init__(self,filename):
      self.filename = filename

   def log(self,text):
      """
      :param text: texto a escribir
      :type text: string
      """
      hora=Ahora().now()
      f = open(self.filename, "a")
      f.write(hora + "; " + text + "\n")
      f.close()
