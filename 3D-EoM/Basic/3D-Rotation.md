## 1. 回転行列について

物体に張り付き、物体の位置・姿勢の変化とともに変化する座標系を物体座標系と呼ぶ。
この物体の姿勢を動かない座標系である世界座標系の上での表し方の一つに回転行列がある。

以下の図のように、物体座標系として $\Sigma_1$ があり、世界座標系として $\Sigma_0$ があるとする。座標系の表し方として、それぞれに直交する単位行列 $x,y,z$ を右手座標系として構成する。

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

次に物体の姿勢が変更したとき、下の右部のように $x_1, y_1, z_1$ が $x_0, y_0, z_0$ からずれることになり、このとき世界座標系上での物体の姿勢を単位行列を用いて次のように表すことが出来る。これを回転行列と呼ぶ。これは単位行列の列を並べたものであり、右手系をなすため、正規直交基底となる。左肩の数字が表す座標系を示している。

$$
^0 R_1 = \begin{bmatrix} {^0}x_1 & {^0}y_1 & {^0}z_1 \end{bmatrix} =\begin{bmatrix}
x_{1,x} & y_{1,x} & z_{1,x} \\
x_{1,y} & y_{1,y} & z_{1,y} \\
x_{1,z} & y_{1,z} & z_{1,z} \\
\end{bmatrix}
$$

<p align="center">
<img src="./images/BodyCorrdnation_WorldCorrdination.png" style="width:90%;"/>
</p>

世界座標の姿勢 $\Sigma_0$ がある変換行列に $R$ によって、 $^0R_1$ になったと考えることが出来る。

$$
^0R_1 = R \ \Sigma_0
$$

$\Sigma_0$ は単位行列であるため、 $R={^0}R_0$ となり、変換行列自体が姿勢を示す回転行列でもある。

### 1.1. 各座標を基準軸とした回転行列

物体座標 $\Sigma_1$ の初期姿勢が世界座標 $\Sigma_0$ となっている状態で、 $x,y,z$ それぞれの軸で回転を行った場合の回転行列を示す。

#### 1.1.1. $x$軸回転

$x$ 軸で回転させることにより、 $x_0=x_1$ であり、 $y_1,z_1$ が $y_0, z_0$ から変化する。

<p align="center">
<img src="./images/x_axis_rotation.png" style="width:90%;"/>
</p>

- $y_1$ は $y_0 - z_0$ 平面で示され、 $(\cos(\phi), \sin(\phi))$
- $z_1 $は $y_0 - z_0$ 平面で示され、 $(-\sin(\phi), \cos(\phi))$

これより、 $x$ 軸周りの回転行列 $E_x(\phi)$ は以下となる。

$$
E_x(\phi) = \begin{bmatrix}
1 & 0 & 0 \\
0 & \cos(\phi) & -\sin(\phi) \\
0 & \sin(\phi) & \cos(\phi)
\end{bmatrix}
$$

#### 1.1.2. $y$軸回転

$y$ 軸で回転させることにより、 $y_0=y_1$ であり、 $x_1,z_1$ が $x_0, z_0$ から変化する。

<p align="center">
<img src="./images/y_axis_rotation.png" style="width:90%;"/>
</p>

- $x_1$ は $x_0 - z_0$ 平面で示され、 $( \cos(\theta), -\sin(\theta) )$
- $z_1 $は $x_0 - z_0$ 平面で示され、 $( \sin(\theta), \cos(\theta) )$

これより、 $y$ 軸周りの回転行列 $E_y(\theta)$ は以下となる。

$$
E_y(\theta) = \begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta) \\
0 & 1 & 0 \\
-\sin(\theta) & 0 &\cos(\theta)
\end{bmatrix}
$$

#### 1.1.3. $z$軸回転

$z$ 軸で回転させることにより、 $z_0=z_1$ であり、 $x_1,y_1$ が $x_0, y_0$ から変化する。

<p align="center">
<img src="./images/z_axis_rotation.png" style="width:90%;"/>
</p>

- $x_1$ は $x_0 - y_0$ 平面で示され、 $( \cos(\theta), \sin(\theta) )$
- $y_1$ は $x_0 - y_0$ 平面で示され、 $( -\sin(\theta), \cos(\theta) )$

これより、 $z$ 軸周りの回転行列 $E_z(\psi)$ は以下となる。

$$
E_z(\psi) = \begin{bmatrix}
\cos(\psi) & -\sin(\psi) & 0 \\
\sin(\psi) & \cos(\psi) & 0 \\
0 & 0 & 1\\
\end{bmatrix}
$$

## 2. ベクトルの回転について


あるベクトルが $\Sigma_1$ 上で ${^1}v_0 = ({^1}v_{0,x}, {^1}v_{0,y}, {^1}v_{0,z}) $ として表されていたとする。このベクトルは世界座標上で ${^0}v_0 = [0, 1, 0]^T$ となる。

<p align="center">
<img src="./images/vector_ration_2.png" style="width:50%;"/>
</p>

$\Sigma_1$ は回転行列で $\Sigma_0$ との関係を表す ${^0}R{_1}$ で次のように表される。

$$
{^0}R{_1} = \begin{bmatrix} {^0}x_{1,x} &  {^0}x_{1,y} &  {^0}x_{1,z} \end{bmatrix} 
$$

そして、ベクトル ${^0}v_0$ は次のように表すことが出来る。

$$
{^0}v_0 = {^0}R{_1}  {^1}v_0
$$

回転行列の逆行列は転置行列として表すことが出来る性質があるため、 ${{^0}R{_1}}{^{-1}} = {^1}R{_0}$ と定義し、次のように表すことが出来る。   

$$
{^1}v_0 = {^1}R{_0}  {^0}v_0
$$

## 3. 回転の合成

$\Sigma_1$ が初期で $\Sigma_0$ と一致していたときに、その姿勢を $x$ 軸で回転し、さらに $y$ 軸で回転したとする。このとき、掛け方を右と左で確認する。

まず最初の $x$ 軸回転は $\Sigma_0$ が単位行列であるのでどちらでも同じである。これを$R_1$とする。

$$
R_1=\Sigma_0 E_x(\phi) = E_x(\phi) \Sigma_0
$$

次の $y$ 軸回転を行う場合、右と左で結果が異なる。

$$
R_{2r} = R_1 E_y(\theta) , \quad R_{2l} = E_y(\theta) R_1
$$

具体的に、 $\phi=$ 90 deg、 $\theta=$ 90 degとすると $\cos(90 deg) = 0$ , $\sin(90 deg) = 1$ となるので、回転行列は次のようになる。

$$
E_x(90 deg) = \begin{bmatrix}
1 & 0 & 0 \\
0 & 0 & -1 \\
0 & 1 & 0
\end{bmatrix}, \quad 
E_y(90 deg) = \begin{bmatrix}
0 & 0 & 1 \\
0 & 1 & 0 \\
-1 & 0 & 0
\end{bmatrix}
$$

ここから $R_1 = E_x(90 deg)$ であるため、 $R_{2r}, R_{2l}$ はそれぞれ次のようになる。

$$
R_{2r} = \begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0 \\
\end{bmatrix}, \quad
R_{2l} = \begin{bmatrix}
0 & 1 & 0 \\
0 & 0 & -1 \\
-1 & 0 & 0 \\
\end{bmatrix}
$$

これは、図で描くと以下のようにな物体の姿勢の遷移となる。

<p align="center">
<img src="./images/composition_of_rotation.png" style="width:90%;"/>
</p>

$R_1$ から $R_{2r}$ への姿勢変異を確認すると、$R_1$ の $y$ 軸で回転が行われていることが分かる。

$R_1$ から $R_{2l}$ への姿勢変異を確認すると、$\Sigma_0$ の $y$ 軸で回転が行われていることが分かる。

ここから、以下でことが言える。

- 回転行列を右側からかけると、自身の座標系の座標軸で回転を行う。
- 回転行列を左側からかけると、世界座標系の座標系で回転を行う。


