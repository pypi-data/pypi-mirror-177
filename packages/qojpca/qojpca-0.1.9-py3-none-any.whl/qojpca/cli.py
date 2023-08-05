"""CLI interface for qojpca project.
"""
import argparse
#import cupy as np
import numpy as np
from qojpca import base
from qojpca import extractFeatures
from pathlib import Path
import os 
import pandas as pd

def run_qojpca(args):
    P= np.array([])
    Q= np.array([])
 
    X,Y = load_matrices(args)

    if args.l_x is None:
        print("INFO: computing "+str(X.shape[1])+" latent variable for the first matrix.")
        l_p = X.shape[1]
    if args.l_y is None:
        print("INFO: computing "+str(Y.shape[1])+" latent variable for the second matrix.")
        l_q = Y.shape[1]
    if(args.l_x is not None):
        l_p = int(args.l_x)
    if(args.l_y is not None):
        l_q = int(args.l_y)
    l = 1.0
    if(args.penalization is not None):
        l = float(args.penalization)
    P_vals,Q_vals,P,Q = base.qojpca(X,Y,l_p,l_q,P,Q,l)
    if(not os.path.isdir(args.output_folder)):
        os.makedirs(args.output_folder)
    np.save(args.output_folder+"/P.npy",P)
    np.save(args.output_folder+"/P_vals.npy",P_vals)
    np.save(args.output_folder+"/Q.npy",Q)
    np.save(args.output_folder+"/Q_vals.npy",Q_vals)

    
def run_jpca(args):
    X,Y =load_matrices(args)
    if args.l_x is None:
        print("INFO: computing "+str(X.shape[1])+" latent variable for the first matrix.")
        l_x = X.shape[1]
    if args.l_y is None:
        print("INFO: computing "+str(Y.shape[1])+" latent variable for the second matrix.")
        l_y = Y.shape[1]
    if(args.l_x is not None):
        l_x = int(args.l_x)
    if(args.l_y is not None):
        l_y = int(args.l_y)
        
    P_vals,Q_vals,P,Q = base.jpca(X,Y,l_x,l_y)
    if(not os.path.isdir(args.output_folder)):
        os.makedirs(args.output_folder)
    np.save(args.output_folder+"/P.npy",P)
    np.save(args.output_folder+"/P_vals.npy",P_vals)
    np.save(args.output_folder+"/Q.npy",Q)
    np.save(args.output_folder+"/Q_vals.npy",Q_vals)
    
def load_matrices(args):

    X = np.load(args.X)
    Y = np.load(args.Y)
    print("INFO: matrices successfully loaded")
    return X,Y


def load_matrices_old(args):
    matrices = args.matrices
    if(len(matrices) == 2):
        X = np.load(matrices[0])
        Y = np.load(matrices[1])
        print("INFO: matrices successfully loaded")
        return X,Y
    if(len(matrices) == 4):
        X = np.load(matrices[0])
        Y = np.load(matrices[1])
        P = np.load(matrices[2])
        Q = np.load(matrices[3])
        print("INFO: matrices successfully loaded")
        return X,Y,P,Q
    print("ERROR: wrong number of matrices provided")
    return 0

def add_pca_arguments(parser):
    parser.add_argument('--X',help='X')
    parser.add_argument('--Y', help='Y')
    parser.add_argument('--l_x',help='number of latent variables to compute for the first matrix, default is 50')
    parser.add_argument('--l_y', help='number of latent variables to compute for the second matrix, default is 50')
    parser.add_argument('--output_folder',required=True,
                    help='output directory')
    parser.add_argument('--penalization',
                    help='penalization value, that is lambda in the paper')              
    
    
    return parser
def add_extract_features_arguments(parser):
    parser.add_argument('--output_folder',required=True,
                    help='output directory')
    parser.add_argument('--input_folder',required=True,
                    help='input directory')
   
    
    return parser

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m qojpca` and `$ qojpca `.
    """

    usage = '''
        Use can use one of the following commands:
            QOJPCA              - performs quasi orhtogonal joint pca on two matrices 
            JPCA                - performs joint pca on two matrices
            EXTRACT_FEATURES    - construct data matrices from folders of mesh files (obj)
    '''
    parser = argparse.ArgumentParser(description='QOJPCA command line interface.', usage = usage , prog = 'PROG')
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

#COMMAND QOJPCA 
    parser_qojpca = subparsers.add_parser('QOJPCA', help='QOJPCA help')
    parser_qojpca = add_pca_arguments(parser_qojpca)

#COMMAND JPCA
    parser_jpca = subparsers.add_parser('JPCA', help='JPCA help')
    parser_jpca = add_pca_arguments(parser_jpca)
    
#COMMAND EXTRACT_FEATURES
    parser_extract_features = subparsers.add_parser('EXTRACT_FEATURES', help='EXTRACT_FEATURES help')
    parser_extract_features =add_extract_features_arguments(parser_extract_features)
    parser_extract_features.add_argument('--regexFilter',required=True,
                    help='regexFilter')
#COMMAND EXTRACT_FEATURES
    parser_SPLIT_TRAIN_TEST = subparsers.add_parser('SPLIT_TRAIN_TEST', help='SPLIT_TRAIN_TEST help')
    parser_SPLIT_TRAIN_TEST =add_extract_features_arguments(parser_SPLIT_TRAIN_TEST)
    parser_SPLIT_TRAIN_TEST.add_argument('--filenameNeutralPose',required=True,
                    help='filenameNeutralPose')
    

    args = parser.parse_args()

    if (args.subcommand == 'QOJPCA'):
        run_qojpca(args)

    if(args.subcommand == "JPCA"):
        run_jpca(args)

    if(args.subcommand =="EXTRACT_FEATURES"):
        listPaths= extractFeatures.findObjPaths(args.input_folder, args.regexFilter)
        verticesPositions = extractFeatures.readPositions(listPaths)
        if(not os.path.isdir(args.output_folder)):
            os.makedirs(args.output_folder)
        print(verticesPositions.shape)
        verticesPositions.to_pickle(args.output_folder+"/positions.pkl")
    
    if(args.subcommand =="SPLIT_TRAIN_TEST"):
        v = pd.read_pickle(args.input_folder+"/positions.pkl")
        filenameNeutralPose= args.filenameNeutralPose
        X,Y,testv,x_bar= extractFeatures.splitDataset(v,filenameNeutralPose)
        np.save(args.input_folder+"/Y_train.npy",Y)
        np.save(args.input_folder+"/X_train.npy",X)
        np.save(args.input_folder+"/X_bar.npy",x_bar)
        testv.to_pickle(args.input_folder+"/v_test.pkl")  