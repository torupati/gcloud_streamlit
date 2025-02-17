import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import chi2

def plot_covariance_ellipse(mean, cov, nstd=3, ax=None, **kwargs):
    """
    平均と共分散行列から誤差楕円をプロットする関数

    Args:
        mean (numpy.ndarray): 平均ベクトル
        cov (numpy.ndarray): 共分散行列
        nstd (float): 標準偏差の倍数 (楕円の大きさ)
        ax (matplotlib.axes.Axes): プロットする axes (None の場合は新規作成)
        **kwargs: 楕円の描画オプション
    """

    if ax is None:
        fig, ax = plt.subplots()

    # sort eigen value
    vals, vecs = np.linalg.eig(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]

    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))

    # calculate width and height of ellipse
    width, height = 2.0 * np.sqrt(vals) * nstd

    ellipse = Ellipse(
        xy=mean,
        width=width,
        height=height,
        angle=theta,
        **kwargs
    )
    ax.add_patch(ellipse)

    #for i in range(2):
    #    axis = vecs[:, i] * np.sqrt(vals[i]) * nstd
    #    ax.plot([mean[0], mean[0] + axis[0]], [mean[1], mean[1] + axis[1]], color="r")

    for i in range(2):
        axis = vecs[:, i] * np.sqrt(vals[i]) * nstd
        x = [mean[0], mean[0] + axis[0]]
        y = [mean[1], mean[1] + axis[1]]
        if i == 0:
            ax.plot(x, y, color="r", label="Major Axis")
        else:
            ax.plot(x, y, color="g", label="Minor Axis")

    return ax

st.title("2D Point Distribution with Covariance Ellipse")

num_points = st.slider("Number of points", min_value=10, max_value=500, value=100)
mean_x = st.slider("Mean X", min_value=-10.0, max_value=10.0, value=0.0)
mean_y = st.slider("Mean Y", min_value=-10.0, max_value=10.0, value=0.0)
cov_11 = st.slider("Covariance 11", min_value=0.1, max_value=5.0, value=1.0)
cov_12 = st.slider("Covariance 12", min_value=-1.0, max_value=1.0, value=0.5)
cov_22 = st.slider("Covariance 22", min_value=0.1, max_value=5.0, value=1.0)
nstd = st.slider("Standard deviation multiplier", min_value=1, max_value=5, value=2)

mean = np.array([mean_x, mean_y])
cov = np.array([[cov_11, cov_12], [cov_12, cov_22]])

# 2次元の点の分布を生成
np.random.seed(0)  # 乱数シードを固定
points = np.random.multivariate_normal(mean, cov, num_points)

# 点の分布と誤差楕円をプロット
fig, ax = plt.subplots()
ax.scatter(points[:, 0], points[:, 1], label="data points")
plot_covariance_ellipse(mean, cov, nstd=nstd, ax=ax, edgecolor="b", facecolor="none", label="covariance ellipse")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal') 
ax.set_title("2D Point Distribution with Covariance Ellipse")
ax.legend()
ax.grid()

st.pyplot(fig)
