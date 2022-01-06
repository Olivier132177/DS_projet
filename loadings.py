import pickle
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
    
def loading():
    cv_lr=pickle.load(open('cv_lr.pickle','rb'))
    cv_rf=pickle.load(open('cv_rf.pickle','rb'))
    cv_svc=pickle.load(open('cv_svc.pickle','rb'))

    modele_lr=pickle.load(open('lr.pickle','rb'))
    modele_rf=pickle.load(open('rf.pickle','rb'))
    modele_svc=pickle.load(open('svc.pickle','rb'))
    return cv_lr, cv_rf, cv_svc, modele_lr, modele_rf, modele_svc
