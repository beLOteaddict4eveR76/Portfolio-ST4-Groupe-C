# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:50:07 2023

@author: thibt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import *


'''Création de la dataframe des pointés avec le fichier .sgt'''
def dataframe(nom_fich):
    # Ouvrir le fichier en lecture seule
    file = open(nom_fich, "r")
    #On récupère la première ligne du fichier
    line=file.readline()
    #On décompose cette ligne en liste de chaine de caractère
    line_split=line.split()
    #On prend uniquement le premier caractère pour avoir le nombre de position des sources et des récepteurs
    n_S_R=line_split[0]

    #On récupère la liste de toutes les lignes du fichier
    lines = file.readlines()
    #On créer une liste de liste pour les positions des émetteurs et récepteurs
    S_R=[]
    for lin_c in lines[0:int(n_S_R)+1]:    
        S_R=S_R + [lin_c.split()]

    #On créer une liste de liste pour les donnees pointées
    data=[]
    for lin_c in lines[int(line_split[0])+3:]:
        data=data + [lin_c.split()]

    #On crée une dataframe pour les positions des émetteurs et récepteurs et pour les donnees pointées

    #Dataframe de 2 colonnes: position x et y
    donnees_SR=pd.DataFrame(S_R)
    #print(donnees_SR)
    #Dataframe de 3 colonnes: index de la ligne de la sources dans donnees_SR, index de la ligne du récepteur, temps pointé
    donnees_pick=pd.DataFrame(data)
    donnees=donnees_pick.copy()
    #print(donnees_pick)

    for i in range (len(donnees[0][:])):
        ligne_S=donnees[0][i]
        donnees[0][i]=donnees_SR[0][int(ligne_S)]
    for i in range(len(donnees[1][:])):
        ligne_S=donnees[1][i]
        donnees[1][i]=donnees_SR[0][int(ligne_S)]
    donnees.columns = ['Source', 'Recepteur','Temps']
    print(donnees)
    return(donnees)


'''Fonction qui ajoute le résultat d'un modèle dans une dataframe' '''
def add_data_res(res,E):
    A=[E]
    df=pd.DataFrame(A,columns =res.columns.tolist())
    for i in range(len(res['Source'])):
        if (res['Source'][i]) == E[0]:
            res.drop([i],axis=0,inplace=True)
    res=pd.concat([res,df])
    res=res.sort_values(by='Source')
    res.reset_index(drop = True, inplace = True)
    return(res)

'''Fonction qui supprime une ligne d une dataframe'''
def suppr_data_res(res,Source):
    for i in range(len(res['Source'])):
        if (res['Source'][i]) == Source:
            res.drop([i],axis=0,inplace=True)
    res.reset_index(drop = True, inplace = True)
    return

'''Fonction qui permet d enlever une valeur abérente dans une dataframe'''
def suppr_val(res,nom_colonne,index_ligne):
    res[nom_colonne][index_ligne]= np.nan
    return()

'''Fonction qui permet d ajouter une valeur dans une dataframe'''
def add_val(res,nom_colonne,index_ligne,val):
    res[nom_colonne][index_ligne]= val
    return()
    

'''Fonction qui créer une dataframe vide pour les données de cassures de pente'''
def data_cassure(res,donnees):
    L_sources=[]
    for i in donnees['Source']:
        if i not in L_sources:
            L_sources=L_sources + [i]
    for i in L_sources:
        L=[i,np.nan,np.nan]
        M=[L]
        df=pd.DataFrame(M,columns=res.columns.tolist())
        res=pd.concat([res,df])
        res=res.sort_values(by='Source')
        res.reset_index(drop = True, inplace = True)
    print(res)

'''Fonction qui affiche les temps d arrivés en fonction de la position'''
def donnees_observees(donnees):
    #On créé la liste des sources
    L_sources=[]
    for i in donnees['Source']:
        if i in L_sources:
            L_sources=L_sources
        else:
            L_sources=L_sources + [i]
   
    fig, ax = plt.subplots()
    plt.xlabel('Position (en m)')
    plt.ylabel('temps de trajet (en s)')
    for i in L_sources:
        X=[]
        Y=[]
        for k in range (len(donnees['Source'])):
            if donnees['Source'][k]==i:
                X = X + [float(donnees['Recepteur'][k])]
                Y = Y + [float(donnees['Temps'][k])]
        ax.plot(X,Y,label= 'Source:' + ' '+ i +' m' )
        ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    return()

'''Fonction qui affiche les temps d arrivés en fonction de la distance 
entre les sources et les récepteurs'''
def donnees_replace(donnees):
    L_sources=[]
    for i in donnees['Source']:
        if i in L_sources:
            L_sources=L_sources
        else:
            L_sources=L_sources + [i]
    
    fig, ax = plt.subplots()
    plt.xlabel('Position (en m)')
    plt.ylabel('temps de trajet (en s)')
    for i in L_sources:
        X=[]
        Y=[]
        for k in range (len(donnees['Source'])):
            if donnees['Source'][k]==i:
                X = X + [abs(float(donnees['Recepteur'][k])-float(donnees['Source'][k]))]
                Y = Y + [float(donnees['Temps'][k])]
        ax.plot(X,Y,'+',label= 'Source:' + ' '+ i +' m' )
        ax.legend()
    return()

'''Fonction qui affiche les temps d arrivés en fonction de la distance 
entre les sources et les récepteurs dans des graphiques différents'''
def donnees_recepteurs(donnees):
    L_sources=[]
    for i in donnees['Source']:
        if i in L_sources:
            L_sources=L_sources
        else:
            L_sources=L_sources + [i]
    fig, ax = plt.subplots(nrows=len(L_sources),ncols=1,figsize=(15., 10.))
    plt.xlabel('Distance source-récepteur (en m)')
    plt.ylabel('temps de trajet (en s)')
    c=0
    for i in L_sources:
        X=[]
        Y=[]
        for k in range (len(donnees['Source'])):
            if donnees['Source'][k]==i:
                X = X + [abs(float(donnees['Recepteur'][k])-float(donnees['Source'][k]))]
                Y = Y + [float(donnees['Temps'][k])]

        ax[c].plot(X,Y,label= 'Source:' + ' '+ i +' m' )
        ax[c].legend()
        c=c+1
    return()


"""BICOUCHE"""

'''Fonction qui calcul l epaisseur de la premiere couche et les vitesses 
des deux premieres couches'''
def bicouche_sans_pendage(cassure,Source,donnees):
    X_1=[]
    Y_1=[]
    X_2=[]
    Y_2=[]
    for i in range(len(donnees['Source'])):
        if donnees['Source'][i]==Source and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) <= cassure:
            X_1= X_1 + [abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i]))]
            Y_1= Y_1 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) >= cassure:
            X_2= X_2 + [abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i]))]
            Y_2= Y_2 + [float(donnees['Temps'][i])]
    plt.plot(X_1,Y_1)
    plt.plot(X_2,Y_2)
    pente_1,T1=np.polyfit(X_1,Y_1,1)
    pente_2,T2=np.polyfit(X_2,Y_2,1)

    V1=1/pente_1
    V2=1/pente_2

    ic= asin(V1/V2)

    H=T2*V1/(2*cos(ic))
    return([float(Source),H,V1,V2])

def bicouche_avec_pendage(Source_directe,Source_retour,cassure1,cassure2,donnees):
    X_1=[]
    Y_1=[]
    X_2=[]
    Y_2=[]
    X_3=[]
    Y_3=[]
    X_4=[]
    Y_4=[]
    for i in range(len(donnees['Source'])):
        if donnees['Source'][i]==Source_directe and float(donnees['Recepteur'][i])>float(Source_directe) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) < cassure1:
            X_1= X_1 + [float(donnees['Recepteur'][i])]
            Y_1= Y_1 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_directe and float(donnees['Recepteur'][i])>float(Source_directe) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) > cassure1:
            X_2= X_2 + [float(donnees['Recepteur'][i])]
            Y_2= Y_2 + [float(donnees['Temps'][i])]

        elif donnees['Source'][i]==Source_retour and float(donnees['Recepteur'][i])<float(Source_retour) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) > cassure2:
            X_3= X_3 + [float(donnees['Recepteur'][i])]
            Y_3= Y_3 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_retour and float(donnees['Recepteur'][i])<float(Source_retour) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) < cassure2:
            X_4= X_4 + [float(donnees['Recepteur'][i])]
            Y_4= Y_4 + [float(donnees['Temps'][i])]
    plt.plot(X_1,Y_1)
    plt.plot(X_2,Y_2)
    plt.plot(X_3,Y_3)
    plt.plot(X_4,Y_4)

    pente_1,T1=np.polyfit(X_1,Y_1,1)
    pente_2,T2=np.polyfit(X_2,Y_2,1)
    #Attention pente négative
    pente_3,T3=np.polyfit(X_3,Y_3,1)
    pente_4,T4=np.polyfit(X_4,Y_4,1)

    V1=(1/pente_1 -1/pente_3)/2
    V2S=1/pente_2
    V2E=-1/pente_4

    i12=0.5*(asin(V1/V2E)+asin(V1/V2S))
    teta1=0.5*(asin(V1/V2S)-asin(V1/V2E))

    V2=V1/sin(i12)

    T1S= T2 + pente_2*float(Source_directe)
    T1E= T4 + pente_4*float(Source_retour)
    print([T1E,T1S])
    H1E=V1*T1E/(2*cos(i12))
    H1S=V1*T1S/(2*cos(i12))
    return([[float(Source_directe),H1S,V1,V2],[float(Source_retour),H1E,V1,V2]])

def modele_bicouche(res):
    X=res['Source']
    Y=-res['Epaisseur']
    V1= round(np.nanmean(res['Vitesse 1']))
    V2= round(np.nanmean(res['Vitesse 2'])) 
    plt.plot(X,Y,'-k')
    ax_c=plt.gca()
    plt.setp(ax_c,'ylim',[-30,0])
    plt.setp(ax_c,'xlim',[min(X),max(X)])
    ax_c.xaxis.set_ticks_position('top')
    ax_c.xaxis.set_ticks([floor(min(X))+5*i for i in range(round((max(X)-min(X))/5)+1)])
    plt.fill_between(X, Y, color='magenta', label=str(V1) + ' m/s')
    plt.fill_between(X,Y,-30, color='red', label=str(V2) + ' m/s')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel('Profil (m)')
    ax_c.xaxis.set_label_position('top') 
    plt.ylabel('Profondeur (m)')
    ax_c.set_aspect('equal')
    return()


'''TRICOUCHE'''

def tricouche_sans_pendage(Source,cassure1,cassure2,donnees):
    X_1=[]
    Y_1=[]
    X_2=[]
    Y_2=[]
    X_3=[]
    Y_3=[]
    for i in range(len(donnees['Source'])):
        if donnees['Source'][i]==Source and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) <= cassure1:
            X_1= X_1 + [abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i]))]
            Y_1= Y_1 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) >= cassure1 and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) <= cassure2:
            X_2= X_2 + [abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i]))]
            Y_2= Y_2 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source and abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i])) >= cassure1:
            X_3= X_3 + [abs(float(donnees['Recepteur'][i])-float(donnees['Source'][i]))]
            Y_3= Y_3 + [float(donnees['Temps'][i])]
    plt.plot(X_1,Y_1)
    plt.plot(X_2,Y_2)
    plt.plot(X_3,Y_3)
    pente_1,T1=np.polyfit(X_1,Y_1,1)
    pente_2,T2=np.polyfit(X_2,Y_2,1)
    pente_3,T3=np.polyfit(X_3,Y_3,1)
    
    V1=1/pente_1
    V2=1/pente_2
    V3=1/pente_3

    i12= asin(V1/V2)
    i23= asin(V2/V3)

    H1=T2*V1/(2*cos(i12))
    H2=(T3-T2)*V2/(2*cos(i23))
    return([float(Source),H1,H2,V1,V2,V3])

def tricouche_avec_pendage(Source_directe,Source_retour,cassure1,cassure2,cassure3,cassure4,donnees):
    X_1=[]
    Y_1=[]
    X_2=[]
    Y_2=[]
    X_3=[]
    Y_3=[]
    X_4=[]
    Y_4=[]
    X_5=[]
    Y_5=[]
    X_6=[]
    Y_6=[]

    for i in range(len(donnees['Source'])):
        if donnees['Source'][i]==Source_directe and float(donnees['Recepteur'][i])>float(Source_directe) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) <= cassure1:
            X_1= X_1 + [float(donnees['Recepteur'][i])]
            Y_1= Y_1 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_directe and float(donnees['Recepteur'][i])>float(Source_directe) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) >= cassure1 and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) <= cassure2:
            X_2= X_2 + [float(donnees['Recepteur'][i])]
            Y_2= Y_2 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_directe and float(donnees['Recepteur'][i])>float(Source_directe) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) >= cassure2:
            X_3= X_3 + [float(donnees['Recepteur'][i])]
            Y_3= Y_3 + [float(donnees['Temps'][i])]

        elif donnees['Source'][i]==Source_retour and float(donnees['Recepteur'][i])<float(Source_retour) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) >= cassure3:
            X_4= X_4 + [float(donnees['Recepteur'][i])]
            Y_4= Y_4 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_retour and float(donnees['Recepteur'][i])<float(Source_retour) and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) <= cassure3 and float(donnees['Recepteur'][i])-float(donnees['Source'][i]) >=cassure4:
            X_5= X_5 + [float(donnees['Recepteur'][i])]
            Y_5= Y_5 + [float(donnees['Temps'][i])]
        elif donnees['Source'][i]==Source_retour and float(donnees['Recepteur'][i])<float(Source_retour) and  float(donnees['Recepteur'][i])-float(donnees['Source'][i]) <=cassure4:
            X_6= X_6 + [float(donnees['Recepteur'][i])]
            Y_6= Y_6 + [float(donnees['Temps'][i])]
        
    plt.plot(X_1,Y_1)
    plt.plot(X_2,Y_2)
    plt.plot(X_3,Y_3)
    plt.plot(X_4,Y_4)
    plt.plot(X_5,Y_5)
    plt.plot(X_6,Y_6)

    pente_1,T1=np.polyfit(X_1,Y_1,1)
    pente_2,T2=np.polyfit(X_2,Y_2,1)
    pente_3,T3=np.polyfit(X_3,Y_3,1)
    #Attention pente négative
    pente_4,T4=np.polyfit(X_4,Y_4,1)
    pente_5,T5=np.polyfit(X_5,Y_5,1)
    pente_6,T6=np.polyfit(X_6,Y_6,1)
    
    V1=(1/pente_1 -1/pente_4)/2
    V2S=1/pente_2
    V3S=1/pente_3
    V2E=-1/pente_5
    V3E=-1/pente_6
    

    i12=0.5*(asin(V1/V2E)+asin(V1/V2S))
    teta1=0.5*(asin(V1/V2S)-asin(V1/V2E))

    V2=V1/sin(i12)
    
    b13=teta1 + asin(V1/V3E)
    a13=asin(V1/V3S)- teta1
    
    i23=0.5*(asin(V2/V1*sin(b13))+asin(V2/V1*sin(a13)))
    teta2= teta1 + 0.5*(asin(V2/V1*sin(a13))-asin(V2/V1*sin(b13)))
    
    V3= V2/sin(i23)
    
    T1S= T2 + pente_2*float(Source_directe)
    T2S= T3 + pente_3*float(Source_directe)
    T1E= T5 + pente_5*float(Source_retour)
    T2E= T6 + pente_6*float(Source_retour)

    H1E=V1*T1E/(2*cos(i12))
    H1S=V1*T1S/(2*cos(i12))
    H2E=V2/(2*cos(i23))*(T2E-H1E*(cos(a13)+cos(b13))/V1)
    H2S=V2/(2*cos(i23))*(T2S-H1S*(cos(a13)+cos(b13))/V1)

    return([[float(Source_directe),H1S,H2S,V1,V2,V3],[float(Source_retour),H1E,H2E,V1,V2,V3]])

def modele_tricouche(res):
    X=res['Source']
    Y1=-res['Epaisseur 1']
    Y2=-res['Epaisseur 2']
    V1= round(np.nanmean(res['Vitesse 1']))
    V2= round(np.nanmean(res['Vitesse 2'])) 
    V3= round(np.nanmean(res['Vitesse 3']))
    plt.plot(X,Y1,'-k')
    plt.plot(X,Y2,'-k')
    ax_c=plt.gca()
    plt.setp(ax_c,'ylim',[-30,0])
    plt.setp(ax_c,'xlim',[min(X),max(X)])
    ax_c.xaxis.set_ticks_position('top')
    ax_c.xaxis.set_ticks([floor(min(X))+5*i for i in range(round((max(X)-min(X))/5)+1)])
    plt.fill_between(X, Y1, color='magenta', label=str(V1) + ' m/s')
    plt.fill_between(X,Y1,Y2, color='red', label=str(V2) + ' m/s')
    plt.fill_between(X,Y2,-30, color='brown', label=str(V3) + ' m/s')
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel('Profil (m)')
    ax_c.xaxis.set_label_position('top') 
    plt.ylabel('Profondeur (m)')
    ax_c.set_aspect('equal')
    return()