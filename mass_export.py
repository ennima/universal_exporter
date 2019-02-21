"""
Mass Export v 0.1
Autor: Enrique Nieto Martínez
Fecha: 21/02/2019
El script descarga por ftp una cantidad masiva de clips

# Valores Conf importantes
	origin_ftp_server: De aquí se extrae los clips
	local_temp_folder: Aquí se pasan los clips 
					Valores	
						"" or "<path>"
						si el valor es "" se descarga en la raíz del programa
	mass_origin_path: En qué carpeta viven los clips
					Valores
						"V:\\media\\Comercial\\VIDRIOS BLINDADOS\\"

	mass_origin_path_tare: Pedazo de la ruta que se elimina en la ruta ftp
					Valores
						"V:\\media\\"

"""

from header import *

def mainProcess(callback):
	time_metric = TimeMetrics()
	time_metric.init()

	print("Begin \n")
	# sleep(1000/1000)
	callback()
	print("\nend")
	print(time_metric.get_elapsed_time())


def downloadClip(clip_name,conf,mass_origin_path=None):
	""" descargar un clip """
	down_item = {}

	""" Generamos un down_item """
	if(mass_origin_path == None):

		if(conf['mass_origin_path_tare'] in conf['mass_origin_path']):
			taring_path = conf['mass_origin_path'].replace(conf['mass_origin_path_tare'],"")
			down_item = {"clip": clip_name,"folder": taring_path}

	else:
		if(conf['mass_origin_path_tare'] in mass_origin_path):
			taring_path = mass_origin_path.replace(conf['mass_origin_path_tare'],"")
			down_item = {"clip": clip_name,"folder": taring_path}

		else:
			print("Error: mass_origin_path no es valido.")


	""" Si es un down_item válido """
	if(len(down_item)>1):
		if(ftp_download(down_item,conf)):
			print("La descarga terminó bien.")
			return True
		else:
			print("Error: El clip {0} no pudo descargarse.".format(down_item['clip']))
			return False
	else:
		print("Error: Problema con down_item.")
		return False




def getListClipsToDownload(origin_path):
	print(origin_path)
	down_list = []
	for root, dirs, files in os.walk(origin_path):
		media_path = ""
		if(len(dirs)>0):
			media_path = root 
			for item in dirs:
				if('cmf' in item):
					down_item = {"mass_origin_path":media_path,"clip":item.replace(".cmf","")}
					down_list.append(down_item)
				else:
					print("Error: No es válido:",item)

	return down_list



def mainLogic():
	conf = load_conf("conf.json")
	delay_time_seconds = 5
	if(not conf):
		print("No se pudo leer el archivo de configuración: conf.json")
	else:
		key_exists = confKeyExists('mass_origin_path', conf)
		if(key_exists == False):
			print("Error: No hay mass_origin_path dentro de conf.json")
		elif(key_exists == None):
			print("Error: mass_origin_path: En qué carpeta viven los clips?")
		else:
			down_list = getListClipsToDownload(conf['mass_origin_path'])
			print(len(down_list))
			print(down_list)
			count = 0
			for clip in down_list:
				count += 1
				print("Descargando ({0}/{1}): ".format(count, len(down_list)),clip)
				downloadClip(clip['clip'],conf,clip['mass_origin_path'])	
				sleep(delay_time_seconds)
				# break
			



if __name__ == '__main__':
	mainProcess(mainLogic)