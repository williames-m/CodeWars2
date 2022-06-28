from mysql.connector import errorcode,connect,Error
import pytest
import os,sys
mypath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(mypath)

from src.business.access_data_base import conectar, fecha_conexao

def test_connect_to_database():
  try:
    cnx = conectar()
    connected=True
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    connected=False
  else:
    connected=True
  cnx.close()
  
  assert connected==True  
