import os
# import pandas as pd
from ftplib import FTP
from ftplib import all_errors
# from subprocess import call
from time import time as time_i
# import time
from datetime import datetime
# # import sockett#
import json
from shutil import copyfile
from pathlib import Path
import subprocess
import requests

def seconds_timestamp(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)																																																																															
	restore_time = "%02d:%02d:%02d" % (h, m, s)
	# print ("Tardó:",restore_time)
	return(restore_time)

def ftp_download(item,conf):
	tiempo_inicial = time_i()
	ftp = FTP(conf["origin_ftp_server"]["host"])
	print(ftp.login(conf["origin_ftp_server"]["user"],conf["origin_ftp_server"]["pass"]))
	print(ftp.pwd())
	# ftp.retrlines('LIST')
	ftp.cwd(item["folder"])
	print("Descargando: "+item["clip"])
	try:
		ftp.retrbinary('RETR '+item["clip"], open(item["clip"], 'wb').write)
		download_success = True
	except all_errors as e:
		print(e)

	ftp.quit()
	tiempo_final = time_i()
	tiempo_ejecucion = tiempo_final - tiempo_inicial
	print("Tardó: " , tiempo_ejecucion,"s")
	print(seconds_timestamp(tiempo_ejecucion))
	return tiempo_ejecucion



tiempo_inicial = time_i()


json_data=open("conf.json").read()
conf = json.loads(json_data)
print(conf['user'])
print(conf["origin_ftp_server"]["host"])

clip_name = "AMLO BELINDA-BITE_DF006JEN"
clip_name = input('Nombre del clip:')
print(conf['default_origin_path'])
origin_folder = ""
if(conf['default_origin_path'] == "") or (conf['default_origin_path'] == "none"):
	# print("No hay default_origin_path")
	origin_folder = input("From Folder:")
else:
	print("From Folder: ",conf['default_origin_path'])
	origin_folder = conf['default_origin_path']

if(conf['default_origin_path_tare'] in origin_folder):
	print("Taring:",conf['default_origin_path_tare'])
	di = origin_folder.replace(conf['default_origin_path_tare'],"")
	origin_folder = di

down_item = {"clip": clip_name,"folder": origin_folder}
print(down_item)
ftp_download(down_item,conf)


muxer_file = conf["muxer_folder"]+conf["muxer"]+".mux"
if(os.path.exists(muxer_file)):
	print("Muxing...")
	muxer_query_raw=open(muxer_file).read()
	print(muxer_query_raw)
	ffmpeg_query = muxer_query_raw.replace("$i_video",clip_name)
	local_dest = conf["local_dest_folder"] + clip_name
	ffmpeg_query = conf["render_engine_path"]+"ffmpeg "+ffmpeg_query.replace("$o_video",local_dest)
	print(ffmpeg_query)
	p = subprocess.Popen(ffmpeg_query)
	p.wait()

tiempo_final = time_i()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print("Tardó: " , tiempo_ejecucion,"s")
print(seconds_timestamp(tiempo_ejecucion))
input("Presiona cualquier tecla para cerrar el programa...")
