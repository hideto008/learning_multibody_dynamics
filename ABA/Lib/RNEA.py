import numpy as np
import numpy.typing as npt

import Lib.Spatial_Vector as sv

# 子リンクのSpatial Velocityの計算 (forward pass)
def recursion_spatial_velocity(transform_mat:npt.ArrayLike, sp_vel:npt.ArrayLike, sbm:npt.ArrayLike, dq:float):
    child_vel = transform_mat@sp_vel + sbm*dq
    return child_vel

# 子リンクのSpatial Accelerationの計算 (forward pass)
def recursion_spatial_acceleration(transform_mat:npt.ArrayLike, sp_acc:npt.ArrayLike, sp_vel:npt.ArrayLike, sbm:npt.ArrayLike, ddq:float, dq:float):
    child_acc = transform_mat@sp_acc + sbm*ddq + sv.spatial_motion_cross_matrix(sp_vel) @ sbm * dq
    return child_acc

# 親リンクのSpatial Forceの計算 (backward pass)
def recursion_spatial_force(sp_net_force:npt.ArrayLike, transform_mat:npt.ArrayLike, sp_force:npt.ArrayLike):
    parent_force = sp_net_force + transform_mat.T@sp_force
    return parent_force

# 固定ベースとする
class Forward_Pass():

    def __init__(self,number_of_link:int, initial_vel:npt.ArrayLike, initial_acc:npt.ArrayLike):
        self.number_of_link = number_of_link
        self.initial_vel = initial_vel
        self.initial_acc = initial_acc

        self.net_forces = np.zeros((number_of_link, 6))      

    # 再帰的計算でSpatial Velocity, Accelerationを求め、各リンク単体のNet Spatial Forceを計算する
    def process(self, 
                omegas:npt.ArrayLike, alphas:npt.ArrayLike,
                tranform_matrices:npt.ArrayLike, sbms:npt.ArrayLike, sp_Is:npt.ArrayLike):
        assert len(omegas) == self.number_of_link
        assert len(alphas) == self.number_of_link
        assert len(tranform_matrices) == self.number_of_link
        assert len(sbms) == self.number_of_link
        assert len(sp_Is) == self.number_of_link

        vel = self.initial_vel
        acc = self.initial_acc

        for i in range(self.number_of_link):
            # Compute child link velocity , acceleration and net spatial force
            omega = omegas[i]
            alpha = alphas[i]
            sbm = sbms[i]
            sp_I = sp_Is[i]
            transform_mat = tranform_matrices[i]
            vel = recursion_spatial_velocity(transform_mat, vel, sbm, omega)
            acc = recursion_spatial_acceleration(transform_mat, acc, vel, sbm, alpha, omega)
            self.net_forces[i] = sv.calculete_net_spatial_newton_euler_spatial_force(sp_I, acc, vel)

        return self.net_forces

# 固定ベース
class Backward_Pass():

    def __init__(self, number_of_link:int):
        self.number_of_link = number_of_link

    # 再帰的に親リンクのトルクを計算する
    def process(self, tranform_matrices:npt.ArrayLike, sbms:npt.ArrayLike, sp_net_forces:npt.ArrayLike):
        assert len(tranform_matrices) == self.number_of_link
        assert len(sbms) == self.number_of_link
        assert len(sp_net_forces) == self.number_of_link

        forces = np.array(sp_net_forces, copy=True)
        torques = np.zeros(self.number_of_link)

        # Compute parent link torques recursively
        for i in reversed(range(self.number_of_link)):
            torques[i] = sbms[i] @ forces[i]

            if i > 0:
                forces[i-1] += tranform_matrices[i].T @ forces[i]

        return torques