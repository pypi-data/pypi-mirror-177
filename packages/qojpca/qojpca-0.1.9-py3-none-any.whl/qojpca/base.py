"""
qojpca base module.

"""
from scipy.sparse.linalg import eigsh
from scipy.sparse.linalg import LinearOperator
#import cupy as np
import numpy as np

l= 1.0
k = 1.0
X=np.array([])
Y=np.array([])
P=np.array([])
Q=np.array([])

def logError(message):
    print("@@@@@")
    print("ERROR: "+message)
    print("@@@@@")
def logInfo(message):
    print("INFO: "+message)
    

def mv1_it1(v):
    return k*X.dot(X.transpose().dot(v)) 

def mv2_it1(v):
    return Y.dot(Y.transpose().dot(v))

def stepP(v):
    return k*X.dot(X.transpose().dot(v)) - l * Q.transpose().dot(Q.dot(v))

def stepQ(v):
    return Y.dot(Y.transpose().dot(v)) - l * P.transpose().dot(P.dot(v))


def qojpca(X_,Y_,l_x, l_y,P_=np.array([]),Q_=np.array([]), l_ = 1.0 , nb_iterations=10, relative_convergence_criteria= 0.05):
    global P,Q,k,l,X,Y
    i=0
    
    if(X_.shape[0]==Y_.shape[0]):
        n = X_.shape[0]
        X=X_
        Y=Y_
        k= X_.shape[1]/X_.shape[1]
        l=l_
        P=P_
        Q=Q_
        if(P.shape[0]==0 or Q.shape[0]==0):
            P_vals,Q_vals,P,Q = jpca(X_,Y_,l_x,l_y)

            logInfo("multiplying the penalization term by the largest eigenvalue of kXX^T, i.e.:" +str(P_vals[0]))
            
            l = l*P_vals[0]
        
        samplingFactor = 40  
        samples  = n/40
        colsIds = np.random.choice(n, int(samples),replace=False)
        
        PQT = P.dot(Q.transpose())
        orthoScore= np.linalg.norm(PQT)
        Xscore = np.linalg.norm(X[colsIds,:] - P[:,colsIds].transpose().dot(P[:,colsIds]).dot(X[colsIds,:]))
        Yscore = np.linalg.norm(Y[colsIds,:] - Q[:,colsIds].transpose().dot(Q[:,colsIds]).dot(Y[colsIds,:]))        
        totalEnergy = k*Xscore*samplingFactor + Yscore*samplingFactor + np.sqrt(l)*orthoScore
        
        
        for i in range(1,nb_iterations): 
            G2 = LinearOperator((n,n), matvec=stepQ)
            Q_vals,Q = eigsh(G2, k=l_y,which ='LA')
            Q = Q.transpose()
    
            G1 = LinearOperator((n,n), matvec=stepP)
            P_vals,P = eigsh(G1, k=l_x, which ='LA')
            P = P.transpose()
            
            PQT = P.dot(Q.transpose())
            orthoScore = np.sqrt(l)*np.linalg.norm(PQT)
            
            Xscore = np.linalg.norm(X[colsIds,:] - P[:,colsIds].transpose().dot(P[:,colsIds]).dot(X[colsIds,:]))
            Yscore = np.linalg.norm(Y[colsIds,:] - Q[:,colsIds].transpose().dot(Q[:,colsIds]).dot(Y[colsIds,:]))        
            newTotalEnergy = k*Xscore*samplingFactor + Yscore*samplingFactor + orthoScore
            logInfo("X score ="+ str(k*Xscore*samplingFactor)+" | Y score ="+ str(Yscore*samplingFactor)+" | orthogonallity score ="+ str(orthoScore)+" |  total energy ="+ str(newTotalEnergy))
            

            if(abs(totalEnergy - newTotalEnergy)/ newTotalEnergy < relative_convergence_criteria ):
                break
            totalEnergy = newTotalEnergy
        
        return P_vals,Q_vals,P,Q
    else:
        logError("dimension mismatch between X and Y")
        return np.array(),np.array(),np.array(),np.array()
        
    


def jpca(X_,Y_,l_p,l_q):
    global X,Y,k
    
    if(X_.shape[0]==Y_.shape[0]):
        n = X_.shape[0]
        X=X_
        Y=Y_
        k=  Y_.shape[1]/X_.shape[1]
        logInfo("Computing k normalization automatically by adjusting the number of samples, k=: "+ str(k))
    else:
        print("ERROR: dimension mismatch between X and Y")
        return 0
    G1_it1 = LinearOperator((n,n), matvec=mv1_it1)
    P_vals,P = eigsh(G1_it1, k=l_p,which ='LA')
    G2_it1 = LinearOperator((n,n), matvec=mv2_it1)
    Q_vals,Q = eigsh(G2_it1, k=l_q,which ='LA')
    P = P.transpose()
    Q = Q.transpose()
    return P_vals,Q_vals,P,Q