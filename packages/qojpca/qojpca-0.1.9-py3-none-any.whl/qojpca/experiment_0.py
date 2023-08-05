from qojpca import base
import numpy as np
import pandas as pd 
from numpy import linalg as LA
import plotly.graph_objects as go
import os

# Orthogonality plot on facescape data
# the bases P and Q should be computed prior to this

def main():
    print(os.getcwd())
    folder = "output_lambda_0/"
    P=np.load(folder+"P.npy")
    P_vals=np.load(folder+"P_vals.npy").reshape(-1,1)

    Q=np.load(folder+"Q.npy")
    Q_vals=np.load(folder+"Q_vals.npy").reshape(-1,1)

    folder = "output_lambda_10/"
    P_ortho_10=np.load(folder+"P.npy")
    P_ortho_vals_10=np.load(folder+"P_vals.npy").reshape(-1,1)


    Q_ortho_10=np.load(folder+"Q.npy")
    Q_ortho_vals_10=np.load(folder+"Q_vals.npy").reshape(-1,1)

    folder = "output_lambda_100/"

    P_ortho_100=np.load(folder+"P.npy")
    P_ortho_vals_100=np.load(folder+"P_vals.npy").reshape(-1,1)


    Q_ortho_100=np.load(folder+"Q.npy")
    Q_ortho_vals_100=np.load(folder+"Q_vals.npy").reshape(-1,1)

    folder = "output_lambda_500/"

    P_ortho_500=np.load(folder+"P.npy")
    P_ortho_vals_500=np.load(folder+"P_vals.npy").reshape(-1,1)


    Q_ortho_500=np.load(folder+"Q.npy")
    Q_ortho_vals_500=np.load(folder+"Q_vals.npy").reshape(-1,1)

    folder = "output_lambda_1000/"

    P_ortho_1000=np.load(folder+"P.npy")
    P_ortho_vals_1000=np.load(folder+"P_vals.npy").reshape(-1,1)


    Q_ortho_1000=np.load(folder+"Q.npy")
    Q_ortho_vals_1000=np.load(folder+"Q_vals.npy").reshape(-1,1)

    results = pd.DataFrame(columns=["Number of modes", "Orthogonality score", "type"])
    print(P.shape)
    for i in range(1,50):
        score1 = np.linalg.norm(P[:i,:].dot(Q[:i,:].transpose()))
        score2 = np.linalg.norm(P_ortho_10.dot(Q_ortho_10[:i,:].transpose()))
        score3 = np.linalg.norm(P_ortho_100.dot(Q_ortho_100[:i,:].transpose()))
        score4 = np.linalg.norm(P_ortho_500.dot(Q_ortho_500[:i,:].transpose()))
        score5 = np.linalg.norm(P_ortho_1000.dot(Q_ortho_1000[:i,:].transpose()))

        results=results.append({"Number of modes": i,"Orthogonality score" :score1, "type": "Joint PCA" },  ignore_index=True)
        results=results.append({"Number of modes": i,"Orthogonality score" :score2, "type": "Regularized joint PCA 10" }, ignore_index=True)
        results=results.append({"Number of modes": i,"Orthogonality score" :score3, "type": "Regularized joint PCA 100" }, ignore_index=True)    
        results=results.append({"Number of modes": i,"Orthogonality score" :score4, "type": "Regularized joint PCA 500" }, ignore_index=True)   
        results=results.append({"Number of modes": i,"Orthogonality score" :score5, "type": "Regularized joint PCA 1000" }, ignore_index=True)   
    np.random.seed(1)

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=results.loc[results['type']=='Joint PCA']['Orthogonality score'],
                             x=results.loc[results['type']=='Joint PCA']['Number of modes'],
                        mode='lines+markers',
                                name=r"$\text{Joint PCA}..............$"))
    fig.add_trace(go.Scatter(y=results.loc[results['type']=='Regularized joint PCA 10']['Orthogonality score'],
                             x=results.loc[results['type']=='Regularized joint PCA 10']['Number of modes'],
                        mode='lines+markers',
                        name=r"$\text{QOJPCA}\;\lambda = 10 e_1 $)"))
    fig.add_trace(go.Scatter(y=results.loc[results['type']=='Regularized joint PCA 100']['Orthogonality score'] ,
                             x=results.loc[results['type']=='Regularized joint PCA 100']['Number of modes'],
                        mode='lines+markers',
                        name=r"$\text{QOJPCA}\;\lambda = 100 e_1  \quad      $)"))
    # fig.add_trace(go.Scatter(y=results.loc[results['type']=='Regularized joint PCA 500']['Orthogonality score'] ,
    #                          x=results.loc[results['type']=='Regularized joint PCA 500']['Number of modes'],
    #                     mode='lines+markers',
    #                     name=r"$\text{QOJPCA}\;500\lambda  \quad      $)"))
    fig.add_trace(go.Scatter(y=results.loc[results['type']=='Regularized joint PCA 1000']['Orthogonality score'] ,
                             x=results.loc[results['type']=='Regularized joint PCA 1000']['Number of modes'],
                        mode='lines+markers',
                        name=r"$\text{QOJPCA}\;\lambda = 1000 e_1  \quad      $)"))
    fig.update_layout(
        #title='Mean Error (mm) before expression correction on the test set',
        font_color="black",
        font_family="sans serif",
        font_size=25,
        margin=dict(
            l=40,
            r=30,
            b=30,
            t=50,
        ),
        legend=dict(
            x=.7,
            y=0.9,
            traceorder="normal",
            font=dict(
                family="sans serif",
                size=50,
                color="black"
            ),
        ),
        paper_bgcolor='rgb(250, 250, 250)',
        plot_bgcolor='rgb(250, 250, 250)',
        showlegend=True,xaxis_title="Number of components",
        yaxis_title=r"$\Large{||PQ^T||}$",
        )
    fig.show()
if __name__ == "__main__":  # pragma: no cover
    main()
