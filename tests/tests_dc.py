import os
import requests
import time

api_address = os.environ['API_IP']
api_port= '8000'

def imp(lib,r):
	print (" {} :\n\tréponse : {} \n\tcode : {}\n"\
	.format(lib,r.json(),r.status_code))

def test1():
	lib="Test 1 (fonctionnement de l'API)"
	r = requests.get(
	    url='http://{address}:{port}/'.format(address=api_address, port=api_port),
	)
	imp(lib,r)

def test2():
	lib='Test 2 (endpoint /verif_login avec login correct)'
	r = requests.get(
	    url='http://{address}:{port}/verif_login'.format(address=api_address,\
            port=api_port),headers={'login':'bob:builder','accept':'application/json'}
	)
	imp(lib,r)

def test3():
	lib='Test 3 (endpoint /verif_login avec login incorrect)'
	r = requests.get(
	    url='http://{address}:{port}/verif_login'.format(address=api_address,\
            port=api_port),headers={'login':'bob:wonkderland','accept':'application/json'}
	)
	imp(lib,r)

def test4():
	lib='Test 4 (endpoint /performances avec modele existant : lr)'
	r = requests.post(
	    url='http://{address}:{port}/performances'.format(address=api_address,\
            port=api_port),headers={'accept':'application/json'},
	    data='{"modele": "lr"}'
	)
	imp(lib,r)

def test5():
	lib='Test 5 (endpoint /performances avec modele inexistant : xx)'
	r = requests.post(
	    url='http://{address}:{port}/performances'.format(address=api_address,\
            port=api_port),headers={'accept':'application/json'},
	    data='{"modele": "xx"}'
	)
	imp(lib,r)

def test6():
	ob='{\
		   "obs": {\
   			    "gender": "Female",\
			    "age": 50,\
			    "hypertension": "1",\
			    "heart_disease": "1",\
			    "residence_type": "Urban",\
			    "avg_glucose_level": 100,\
			    "bmi": 30,\
			    "smoking_status": "smokes"\
			},\
		    "mod" : {\
                            "modele": "lr"\
			  }\
	   }'

	lib='Test 6 (endpoint /evaluation avec un utilisateur qui tente d\'accèder à un modèle autorisé)'
	r = requests.post(
	    url='http://{address}:{port}/evaluation'.format(address=api_address,\
            port=api_port),headers={'login':'bob:builder','accept':'application/json','Content-Type': 'application/json'},
	    data=ob
	)
	imp(lib,r)

def test7():
	ob='{\
		   "obs": {\
   			    "gender": "Female",\
			    "age": 50,\
			    "hypertension": "1",\
			    "heart_disease": "1",\
			    "residence_type": "Urban",\
			    "avg_glucose_level": 100,\
			    "bmi": 30,\
			    "smoking_status": "smokes"\
			},\
		    "mod" : {\
                            "modele": "lr"\
			  }\
	   }'

	lib='Test 7 (endpoint /evaluation avec un utilisateur qui tente d\'utiliser un modèle auquel il n\'a pas accès)'
	r = requests.post(
	    url='http://{address}:{port}/evaluation'.format(address=api_address,\
            port=api_port),headers={'login':'clementine:mandarine','accept':'application/json','Content-Type': 'application/json'},
	    data=ob
	)
	imp(lib,r)

def test8():
	ob='{\
		   "obs": {\
   			    "gender": "Female",\
			    "age": 5d0,\
			    "hypdertension": "1",\
			    "heart_disease": "1",\
			    "residence_type": "Urban",\
			    "avg_glucose_level": 100,\
			    "bmi": 30,\
			    "smoking_status": "smokes"\
			},\
		    "mod" : {\
                            "modele": "lr"\
			  }\
	   }'

	lib='Test 8 (endpoint /evaluation avec des erreurs de saisie dans les donnees)'
	r = requests.post(
	    url='http://{address}:{port}/evaluation'.format(address=api_address,\
            port=api_port),headers={'login':'bob:builder','accept':'application/json','Content-Type': 'application/json'},
	    data=ob
	)
	imp(lib,r)

time.sleep(10)

test1()
test2()
test3()
test4()
test5()
test6()
test7()
test8()
