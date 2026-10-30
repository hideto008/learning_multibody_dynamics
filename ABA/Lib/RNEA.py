import numpy as np
import numpy.typing as npt

import Spatial_Vector as sv

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
    parent_force = sp_net_force + transform_mat@sp_force
    return parent_force

# 固定ベースとする
class Forward_Pass():

    def __init__(self,number_of_link:int):
        self.number_of_link = number_of_link

        self.net_forces = np.zeros((number_of_link, 6))      

    def process(self, 
                angles:npt.ArrayLike, omegas:npt.ArrayLike, alphas:npt.ArrayLike,
                tranform_matrices:npt.ArrayLike, sbms:npt.ArrayLike, sp_Is:npt.ArrayLike):
        assert len(angles) == self.number_of_link
        assert len(omegas) == self.number_of_link
        assert len(alphas) == self.number_of_link
        assert len(tranform_matrices) == self.number_of_link
        assert len(sbms) == self.number_of_link
        assert len(sp_Is) == self.number_of_link

        for i in range(self.number_of_link):
            angle = angles[i]
            omega = omegas[i]
            alpha = alphas[i]
            if i == 0:
                # Base link
                vel = np.zeros(6)
                acc = np.zeros(6)
            else:
                # Compute child link velocity and acceleration
                sbm = sbms[i]
                transform_mat = tranform_matrices[i]
                vel = recursion_spatial_velocity(transform_mat, vel, sbm, omega)
                acc = recursion_spatial_acceleration(transform_mat, acc, vel, sbm, alpha, omega)
                sp_I = sp_Is[i]
                self.net_forces[i] = sv.calculete_net_spatial_newton_euler_spatial_force(sp_I, acc, vel)

class Backward_Pass():

    def __init__(self, number_of_link:int):
        self.number_of_link = number_of_link
        self.net_forces = np.zeros((number_of_link, 6))

    def process(self, tranform_matrices:npt.ArrayLike, sp_forces:npt.ArrayLike):
        assert len(tranform_matrices) == self.number_of_link
        assert len(sp_forces) == self.number_of_link

        for i in reversed(range(self.number_of_link)):
            sp_force = sp_forces[i]
            transform_mat = tranform_matrices[i]
            if i == self.number_of_link - 1:
                # End link
                parent_force = self.net_forces[i]
            else:
                parent_force = recursion_spatial_force(self.net_forces[i], transform_mat, sp_force)
            self.net_forces[i-1] = parent_force if i > 0 else self.net_forces[i-1]