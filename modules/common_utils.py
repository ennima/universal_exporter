"""
Common Utils v 0.2
Autor: Enrique Nieto Martínez
Fecha: 21/02/2019
Funciones primordiales para trabajar con archivos por ftp

"""
from ftplib import FTP
from ftplib import all_errors
import json
import os,sys
import subprocess
# sys.path.append('../trans')
from time_metrics import *


def common_utils_test():
	print("common_utils_test ok")



def percentage(max_value,eval_value):
	return (eval_value * 100) / max_value



def confKeyExists(key_to_find, conf):
	""" Valida la existencia de un valor en la configuración """
	return_value = False
	if(key_to_find in conf.keys()):
		if(conf[key_to_find] == "") or (conf[key_to_find] == "none"):
			print("El valor {0} está vacio.".format(key_to_find))
			return_value = None
		else:
			print("Hay: {0} :D".format(key_to_find))
			return_value = True
	else:
		print("Error: Falta {0} en conf.json.".format(key_to_find))
		return_value = False

	return return_value



def ftp_download(item,conf):
	""" Download media by FTP """
	key_to_find = 'local_temp_folder'
	if(confKeyExists(key_to_find, conf) == False):
		print("Error: No se pudo descargar el clip.")

	else:
		# print("Procesando clip...")
		download_success = False
		ftp = FTP(conf["origin_ftp_server"]["host"])
		print(ftp.login(conf["origin_ftp_server"]["user"],conf["origin_ftp_server"]["pass"]))
		print(ftp.pwd())
		# ftp.retrlines('LIST')
		ftp.cwd(item["folder"])
		# print("Descargando: "+item["clip"])
		try:
			ftp.retrbinary('RETR '+item["clip"], open(conf[key_to_find]+item["clip"], 'wb').write)
			download_success = True
		except all_errors as e:
			print(e)

		ftp.quit()
	
	return download_success



def ftpSend(host,user,passs,destFolder,newFile):
	""" Send media by FTP """
	return_value = False
	passs = ""

	try:
		ftp = ftplib.FTP(host)
	except:
		print("No se pudo establecer conexión con el servidor FTP:",host)
	else:
		try:
			ftp.login(user,passs)
		except ftplib.error_perm as e:
			print("Error de login: ",e)
		else:
			ftp.cwd(destFolder)
			print ("Enviando ",os.path.basename(newFile) ,"a destino FTP...")
			try:
				ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
			except ftplib.error_temp as e:
				print("Error al enviar el archivo:", e)
			else:
				
				print ("Listo.")
				return_value = True

			finally:
				ftp.quit()
			
		finally:
			pass

	finally:
		pass

	return return_value



def load_conf(conf_file):
	""" Cargar la configuración  """
	if(os.path.exists(conf_file)):
		with open(conf_file) as json_file:
			json_data = json_file.read()
			
		conf = json.loads(json_data)
	else:
		conf = False	
	return conf



def find_conf_value(key_conf, conf):
	""" Check that one value are in conf """
	if(key_conf in conf.keys()):
		return conf[key_conf]
	else:
		print("## Error: Se requiere valor: " + key_conf)
		return False



def validate_conf_data(required_keys, conf):
	""" Check that all values are in conf """
	return_val = True
	for key_conf_req in required_keys:
			if(find_conf_value(key_conf_req, conf) == False):
				return_val = False

	return return_val
