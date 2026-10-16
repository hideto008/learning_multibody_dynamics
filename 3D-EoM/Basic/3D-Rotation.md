## 回転行列

物体に張り付き、物体の位置・姿勢の変化とともに変化する座標系を物体座標系と呼ぶ。
この物体の姿勢を動かない座標系である世界座標系の上での表し方の一つに回転行列がある。

以下の図のように、物体座標系として$\Sigma_1$があり、世界座標系として$\Sigma_0$があるとする。座標系の表し方として、それぞれに直交する単位行列$x,y,z$を右手座標系として構成する。

$$
\Sigma_0 = \begin{bmatrix}x_0 & y_0 & z_0 \end{bmatrix}
=\begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
$$


世界座標系上での物体の姿勢は初期では以下のようにそれぞれの単位ベクトルが一致している。

$$
\begin{aligned}
x_1 &= x_0 \\
y_1 &= y_0 \\
z_1 &= z_0
\end{aligned}
$$

次に物体の姿勢が変更したとき、下の右部のように$x_1, y_1, z_1$が$x_0, y_0, z_0$からずれることになり、このとき世界座標系上での物体の姿勢を単位行列を用いて次のように表すことが出来る。

$$
^0 R_1 = \begin{bmatrix} x_1 & y_1 & z_1 \end{bmatrix} =\begin{bmatrix}
x_{1,x} & y_{1,x} & z_{1,x} \\
x_{1,y} & y_{1,y} & z_{1,y} \\
x_{1,z} & y_{1,z} & z_{1,z} \\
\end{bmatrix}
$$

<p align="center">
<img src="./images/BodyCorrdnation_WorldCorrdination.png" style="width:90%;"/>
</p>

これは、世界座標系上の世界座標の姿勢を$^0R_0$ とすると、ある変換行列にRによって、

$$
^0R_0 = \begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
$$

