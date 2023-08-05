# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import igl
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import re

publishableVidsFacescape = ['121','211','339','343','392','394','420','526','593','609']


def construct_X_Y(trainv,list_v_i_m,v_bar_neutral,nameOfNeutralMesh="1_neutral"):
    nbExpressionTrain = trainv.shape[1]
    print(nbExpressionTrain)
    nbFacesTrain = trainv.shape[0]
    print(nbFacesTrain)
    nbVertices = int(trainv.iloc[0].iloc[0][0].shape[0])
    print(nbVertices)
    Y = np.zeros((nbExpressionTrain*nbFacesTrain,nbVertices*3)) 
    X = np.zeros((nbFacesTrain,nbVertices*3))

    for i in range(nbFacesTrain):
        for j in range(nbExpressionTrain):
            if(isinstance(trainv.iloc[i].iloc[j], list) and list_v_i_m[i]):
                u_i_j = list_v_i_m[i] - trainv.iloc[i].iloc[j][0]
                Y[nbExpressionTrain*i+j] =np.array(u_i_j.flatten(order='F'))
            else:
                print("a mesh is missing")

    print(v_bar_neutral.shape)
    for i in range(nbFacesTrain):
        if(isinstance(trainv.iloc[i][nameOfNeutralMesh], list)):
            u_i_j = v_bar_neutral - trainv.iloc[i][nameOfNeutralMesh][0]
            X[i] =np.array(u_i_j.flatten(order='F'))
        else:
            print("missing neutral number: "+ str(i))

    Y=Y.transpose()
    X=X.transpose()
    return X,Y

def computeMeanTemplates(trainv,nameOfNeutralMesh="1_neutral"):
    nbExpressionTrain = trainv.shape[1]
    nbFacesTrain = trainv.shape[0]
    v_bar_neutral= np.array([])
    nbMeshes=0
    for i in range(nbFacesTrain):
        if(isinstance(trainv.iloc[i][nameOfNeutralMesh], list)):
            if(i==0):
                v_bar_neutral = trainv.iloc[i][nameOfNeutralMesh][0]
            else:
                v_bar_neutral = v_bar_neutral + trainv.iloc[i][nameOfNeutralMesh][0]
            nbMeshes =nbMeshes+1
        else:
            print("a mesh is missing")
    v_bar_neutral = v_bar_neutral / nbMeshes

    list_v_i_m = [None]*nbFacesTrain

    for i in range(nbFacesTrain):
        if(isinstance(trainv.iloc[i][nameOfNeutralMesh], list)):
            v_m_j =trainv.iloc[i][nameOfNeutralMesh]
            list_v_i_m[i]=v_m_j
        else:
            print("missing neutral number: "+ str(i))
    return v_bar_neutral, list_v_i_m

def splitDataset(v,filenameNeutralPose):
    trainv, testv = train_test_split(v, test_size=0.3)
    v_bar_neutral, list_v_i_m = computeMeanTemplates(trainv,filenameNeutralPose)
    X,Y = construct_X_Y(trainv,list_v_i_m,v_bar_neutral,filenameNeutralPose)
    return X, Y , testv, v_bar_neutral
    

def findObjPaths(directory,regexS='(.*)\.obj'):
    list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if(re.search(regexS, file)):
                list.append(os.path.join(root, file))
                print(file)
    print(len(list))
    return list

def computeMean(pathToFolder : str):
    listPath = findObjPaths(pathToFolder)
    return computeMean(listPath)

def computeMean(listPath : list):
    v_bar, f_bar = igl.read_triangle_mesh(listPath[0])
    N = len(v_bar)
    M = len(listPath)
    i = 0
    for obj in listPath:
        v_i, f_i = igl.read_triangle_mesh(obj)
        v_bar = v_bar + v_i
        if( i%10 ==0):
            print(i%M)
        i= i+1
    v_bar = v_bar / M
    return v_bar,f_bar

def computeMean(arrays :np.array):
    v_bar = np.array(arrays[0])
    M = np.shape(arrays)[0]
    print(M)
    for v_i in arrays:
        v_bar = v_bar + v_i
    v_bar = v_bar / M
    return v_bar

def readPositions(listPath: list):
    print("readPositions()")
    v_bar, f_bar = igl.read_triangle_mesh(listPath[0])
    N = len(v_bar)
    M = len(listPath)
    print(M)
    i = 0
    df = pd.DataFrame()
    for obj in listPath:
        objPath = Path(obj)
        v_i, f_i = igl.read_triangle_mesh(obj)
        expressionID = str(os.path.basename(objPath)).split(".")[0]
        if not expressionID in df.columns:
            df[expressionID] = ""
            df[expressionID] = df[expressionID].astype(object)
        df.at[str(os.path.basename(objPath.parents[1])),expressionID]=[v_i]
        
        if( i%10 ==0):
            print(i%M)
            
        i= i+1
    return df
    
    


