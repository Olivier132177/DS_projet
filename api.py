from fastapi import FastAPI, Header, HTTPException
from typing import Optional
from pydantic import BaseModel
from loadings import loading
import pandas as pd
import numpy as np
import base64
import random


cv_lr, cv_rf, cv_svc, modele_lr, modele_rf, modele_svc=loading()

class Observation(BaseModel):
	gender: str
	age : float
	hypertension : str
	heart_disease : str
	residence_type : str
	avg_glucose_level : float
	bmi : Optional[float]=None
	smoking_status : str

class Evalu(BaseModel):
	modele: str 

def recherche_droits(ind,df_acces, mod):
	''' verifie si un utilisateur donné a l'autorisation d'utiliser un modèle '''
	if df_acces.loc[ind,mod].values == 1:
		return 1
	else :
		raise HTTPException(status_code=403, detail="L'utilisateur n'as pas accès à ce modèle")

def eval_login_base64(saisie, df_acces):
	'''Vérifie si le login et le password fournis sont valides
	Arguments : 
		saisie (str) : la chaîne de caractères saisie
		df_acces : le DataFrame contenant la base des utilisateurs
	Retourne :
		0 si l'authentification échoue
		1 si l'authentification aboutit
	'''
	recherche_cred=df_acces.loc[df_acces['cred']==base64.b64encode(saisie.encode())]

	if len(recherche_cred)!=0:
		return 1, recherche_cred.index
	else:
		raise HTTPException(status_code=404, detail="Echec de l'authentification")

def enregistrement_aleatoire():

	return {
	'gender':[random.choice(['Male','Female','Other'])],
	'age':[random.randint(1,99)],
	'hypertension':[random.choice(['1','0'])],
	'heart_disease':[random.choice(['1','0'])],
	'Residence_type':[random.choice(['Urban','Rural'])],
	'avg_glucose_level':[random.randrange(20,250)],
	'bmi':[random.randrange(15,80)],
	'smoking_status':[random.choice(['formerly smoked', 'never smoked', 'smokes', 'Unknown'])],
	'bmi_nan':[random.choice(['oui','non'])],
	}

obs_alea=enregistrement_aleatoire()
df_t2=pd.DataFrame.from_dict(obs_alea)

acces=[
	{'login':'alice','password':'wonderland','lr':1,'rf':1,'svc':1,'cred':b'YWxpY2U6d29uZGVybGFuZA=='},
	{'login':'bob','password':'builder','lr':1,'rf':0,'svc':0,'cred':b'Ym9iOmJ1aWxkZXI='},
	{'login':'clementine','password':'mandarine','lr':0,'rf':1,'svc':0,'cred': b'Y2xlbWVudGluZTptYW5kYXJpbmU='}
      ]
df_acces=pd.DataFrame(acces)

api = FastAPI(title='API modele')

@api.get('/')
def get_root():
   return 'api fonctionnelle'

@api.post('/evaluation',responses=resp)
def evaluation(obs : Observation, mod:Evalu, login=Header(None)):
	'''Classe une observation en 0 ou 1 selon un modèle donné 
	Arguments : obs: l'observation, mod: le modèle('svc', 'rf', 'lr'), : le login+password fournis '''
	
	resu,ind=eval_login_base64(login,df_acces)
	if resu==0:
		return "Erreur d'authentification"
	else:
		if mod.modele not in ['rf','lr','svc']:
			return 'Le modèle spécifié est manquant ou incorrect'
		else :
			if mod.modele =='rf' :
				choix=modele_rf
				nom='RandomForestClassifier'			
			elif mod.modele =='lr':
				choix=modele_lr
				nom='LogisticRegression'
			elif mod.modele =='svc':
				choix=modele_svc
				nom='SVC'
			dr = recherche_droits(ind,df_acces,mod.modele)	
			if dr ==0:
				return "L'utilisateur n'a pas accès à ce modèle"
			else:
				dic_obs ={
				'gender':[obs.gender],
				'age':[obs.age],
				'hypertension':[obs.hypertension],
				'heart_disease':[obs.heart_disease],
				'Residence_type':[obs.residence_type],
				'avg_glucose_level':[obs.avg_glucose_level],
				'bmi':[obs.bmi],
				'smoking_status':[obs.smoking_status],
				}

				if obs.bmi is None:
					dic_obs['bmi_nan']=['Non']
				else:
					dic_obs['bmi_nan']=['Oui']

				resultat=choix.predict(pd.DataFrame.from_dict(dic_obs))

				if resultat[0]==0:
					resu= "Pas d'AVC"
				else:
					resu= "AVC"
				return {'Modele': nom,'Résultat':int(resultat[0]), 'Interprétation':resu}

@api.get('/verif_login')
def get_headers(login=Header(None)):
	'''
	 Vérifie si le couple username/password est présent dans la base utilisateur, retourne "Identifiants valides" ou "erreur d authentification" en fonction du résultat
	'''
	resu,_=eval_login_base64(login,df_acces)
	if resu==1 :
		return "Identifiants valides"
	else:
		raise HTTPException (status_code=404,detail="Erreur d'authentification")

@api.post('/performances')
def get_perf(ev:Evalu):
	
	'''Retourne le F1 score du modèle indiqué, ou le F1 score de l'ensemble des modèles si aucun nom de modèle n'est saisi
	   Argument : ev(str) : le nom du modèle à évaluer '''
	 
	if ev.modele=='lr':
		return {"F1 score du modèle LogisticRegression" : round(cv_lr['test_f1'].mean(),3)}
	elif ev.modele=='rf':
		return {"F1 score du modèle RandomForestClassifier" : round(cv_rf['test_f1'].mean(),3)}
	elif ev.modele=='svc':
		return {"F1 score du modèle SVC" : round(cv_svc['test_f1'].mean(),3)}
	elif ev.modele=='':
		return {"F1 score des différents modèles" :
					{
					"LogisticRegression" : round(cv_lr['test_f1'].mean(),3),
					"RandomForestClassifier" : round(cv_rf['test_f1'].mean(),3),
					"SVC" : round(cv_svc['test_f1'].mean(),3)
					}
				}
	else :
		raise HTTPException(status_code=404, detail= "Le modèle demandé n'existe pas")
