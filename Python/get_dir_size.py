import math
import os

path_to_directory = r"C:\Users\joaoh\OneDrive\Área de Trabalho\Financeiro\Contas_aniversario.xlsx"
for i in os.listdir(path_to_directory):

os.stat(path_to_directory).st_size

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])