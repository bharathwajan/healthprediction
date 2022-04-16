from django.db import models
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics  import accuracy_score
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier,VotingClassifier,AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
import os

class connect(models.Model):
    firstname=models.CharField(max_length=100)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)




class file():
    general=pd.read_excel('C:/Users/rbw19/healthprediction/firstpage/General.xlsx'  )
    eye=pd.read_excel('C:/Users/rbw19/healthprediction/firstpage/eye.xlsx')
    skin=pd.read_excel('C:/Users/rbw19/healthprediction/firstpage/skin.xlsx')

    #ONE HOT ENCODING 

    one_hot_general =pd.get_dummies(general['symptoms'])
    one_hot_eye     =pd.get_dummies(eye['symptoms'])
    one_hot_skin    =pd.get_dummies(skin['symptoms'])

    general_dise=general['disease']
    eye_dise=eye['disease']
    skin_dise=skin['disease']

    concat_general=pd.concat([general_dise,one_hot_general],axis=1)
    concat_skin=pd.concat([skin_dise,one_hot_skin],axis=1)
    concat_eye=pd.concat([eye_dise,one_hot_eye],axis=1)

    grpby_general = concat_general.groupby('disease').sum()
    grpby_general = grpby_general.reset_index()
    grpby_skin    = concat_skin.groupby('disease').sum()
    grpby_skin     = grpby_skin.reset_index()
    #grpby_skin.to_csv('C:/Users/rbw19/healthprediction/firstpage/aftertelo.csv')
    grpby_eye     = concat_eye.groupby('disease').sum()
    grpby_eye     = grpby_eye.reset_index()

    
    
    general_disease=grpby_general['disease']
    skin_disease=grpby_skin['disease']
    eye_disease=grpby_eye['disease']

    general_symptoms=grpby_general[grpby_general.columns[1:]]
    skin_symptoms=grpby_skin[grpby_skin.columns[1:]]
    eye_symptoms=grpby_eye[grpby_eye.columns[1:]]

class prediction():
    #creating object of the class file
    

    def skin_predict_model(self,user_input):
        files=file()
        dt=DecisionTreeClassifier()
        
        nb=GaussianNB()
        nb=AdaBoostClassifier(nb,n_estimators=10)
        
        rf=RandomForestClassifier(n_estimators=20)
        rf=BaggingClassifier(rf,n_estimators=15)

        vc = VotingClassifier( estimators= [('rf',rf),('dt',dt),('nb',nb)], voting = 'hard')
        vc.fit(files.skin_symptoms,files.skin_disease)

        prediction=vc.predict(user_input)
        
        score=vc.score(files.skin_symptoms,files.skin_disease)*100
        return prediction
    
    
    
    def eye_predict_model(self,user_input):
        files=file()
        
        dt=DecisionTreeClassifier()
        
        nb=GaussianNB()
        nb=AdaBoostClassifier(nb,n_estimators=10)
        
        rf=RandomForestClassifier(n_estimators=20)
        rf=BaggingClassifier(rf,n_estimators=15)

        vc = VotingClassifier( estimators= [('rf',rf),('dt',dt),('nb',nb)], voting = 'hard')
        vc.fit(files.eye_symptoms,files.eye_disease)    

        prediction=vc.predict(user_input)
        score=vc.score(files.eye_symptoms,files.eye_disease)*100
        
        return prediction

        
        
    
        

    def general_predict_model(self,user_input):
        files=file()
        dt=DecisionTreeClassifier()
        
        nb=GaussianNB()
        nb=AdaBoostClassifier(nb,n_estimators=10)
        
        rf=RandomForestClassifier(n_estimators=20)
        rf=BaggingClassifier(rf,n_estimators=15)

        vc = VotingClassifier( estimators= [('rf',rf),('dt',dt),('nb',nb)], voting = 'hard')
        vc.fit(files.general_symptoms,files.general_disease)

        prediction=vc.predict(user_input)
        

        score=vc.score(files.general_symptoms,files.general_disease)*100
        
        return prediction
        



class catagory():
    def cat(self,catagory):
        #print('Select any one of the catagories below')
        #print('---------------------')
        #print('| 1 . General       | ')
        #print('| 2 . Skin disease  | ')
        #print('| 3 . Eye disease   | ')
        #print('---------------------')
        catagory=catagory
        #creating object for file class
        path=file()
        if catagory=='general':
           
            #print('selected general')
            dise=path.grpby_general.columns[1:]
            return (list(dise))
            """
            user_inputs=[]
            for i in dise:
                a=str(i)
                a=int(input(f'Do you have {a} ?'))
                user_inputs.append(a)

            user_inputs=np.array(user_inputs).reshape(1,len(user_inputs))
            user_inputs=pd.DataFrame(user_inputs)
            
            #creating object for prediction class
            pred=prediction()
            result=pred.general_predict_model(user_inputs)
            print(result)
            """
        elif catagory=='skin_disease':
            #print('Selected Skin disease')
            dise=path.grpby_skin.columns[1:]
            return (list(dise))
            """
            user_inputs=[]
            for i in dise:
                a=str(i)
                a=int(input(f'Do you have {a} ?'))
                user_inputs.append(a)
            user_inputs=np.array(user_inputs).reshape(1,len(user_inputs))
            user_inputs=pd.DataFrame(user_inputs)
            #creating path for prediction class
            pred=prediction()
            result=pred.skin_predict_model(user_inputs)
            print(result)
            """
        elif catagory=='eye_disease':
            #print('selected Eye disease')
            dise=path.grpby_eye.columns[1:]
            return (list(dise))
            """
            user_inputs=[]
            for i in dise:
                a=str(i)
                a=int(input(f'Do you have {a} ?'))
                user_inputs.append(a)
            user_inputs=np.array(user_inputs).reshape(1,len(user_inputs))
            user_inputs=pd.DataFrame(user_inputs)
            #creating path for prediction class
            pred=prediction()
            result=pred.eye_predict_model(user_inputs)
            print(result)
            """
        else:
            print('selction is mandatory')
class extra_features():
    def disp(self,disease):
        df=pd.read_excel('C:/Users/rbw19/healthprediction/firstpage/prediction.xlsx')
        a=df.loc[df['diseases']==str(disease)]
        desc=list(a['description'])
        hosp=list(a['Hospital'])
        contact=list(a['contact'])
        addr=list(a['address'])
        return desc,hosp,contact,addr
        