import numpy as np
import numpy.typing as npt
import Lib.Spatial_Vector as sv

class ABA:
    def __init__(self, number_of_links: int,
                 init_sp_vel: npt.ArrayLike,
                 init_sp_acc: npt.ArrayLike,
                 sbms: npt.ArrayLike,
                 sp_Is: npt.ArrayLike):
        self.number_of_links = number_of_links
        self.init_sp_vel = np.array(init_sp_vel)
        self.init_sp_acc = np.array(init_sp_acc)
        self.sbms = np.array(sbms)
        self.sp_Is = np.array(sp_Is)

        self.c = np.zeros((number_of_links, 6)) # Spatial Accelertionの速度依存項
        self.p_a = np.zeros((number_of_links, 6)) # バイアス力
        self.I_a = np.zeros((number_of_links, 6, 6)) # ABI
        self.d = np.zeros((number_of_links)) # 関節空間に射影したABI
        self.u = np.zeros((number_of_links)) # ABIに作用する投影力
        self.U = np.zeros((number_of_links, 6)) # ABIに作用する投影力の行列

    def _pass1_forward_pass(self, transform_mats: npt.ArrayLike, omegas: npt.ArrayLike):

        sp_vel = self.init_sp_vel

        for i in range(self.number_of_links):
            # ここで各リンクの前進パスの計算を行う

            sp_vel = transform_mats[i] @ sp_vel + self.sbms[i] * omegas[i]
            self.c[i] = sv.spatial_motion_cross_matrix(sp_vel) @ (self.sbms[i] * omegas[i])
            self.p_a[i] = sv.spatial_force_cross_matrix(sp_vel) @ self.sp_Is[i] @ sp_vel
            self.I_a[i] = self.sp_Is[i]


    def _pass2_backward_pass(self,transform_mats:npt.ArrayLike, torques:npt.ArrayLike):
        for i in reversed(range(self.number_of_links)):

            self.U[i] = self.I_a[i] @ self.sbms[i]
            self.d[i] = self.sbms[i].T @ self.U[i]
            self.u[i] = torques[i] - self.sbms[i].T @ self.p_a[i]

            if  (i > 0) :
                bar_I_A = self.I_a[i] - np.outer(self.U[i], self.U[i]) / self.d[i]
                bar_p_a = self.p_a[i] + bar_I_A @ self.c[i] + self.U[i] * self.u[i] / self.d[i]

                self.I_a[i-1] = self.I_a[i-1] + transform_mats[i].T @ bar_I_A @ transform_mats[i]
                self.p_a[i-1] = self.p_a[i-1] + transform_mats[i].T @ bar_p_a

    def _pass3_forward_acceleration(self, transform_mats: npt.ArrayLike):
        sp_acc = self.init_sp_acc
        accs = np.zeros((self.number_of_links)) # 各リンクの加速度を格納する配列

        for i in range(self.number_of_links):
            part_acc = transform_mats[i] @ sp_acc + self.c[i]
            accs[i] = (self.u[i] - self.U[i].T @ part_acc) / self.d[i]
            sp_acc = part_acc + self.sbms[i] * accs[i]

        return accs

    def calculate_accelerations(self, 
                                transform_mats: npt.ArrayLike,
                                omegas: npt.ArrayLike,
                                torques: npt.ArrayLike) -> npt.ArrayLike:

        self._pass1_forward_pass(transform_mats, omegas)
        self._pass2_backward_pass(transform_mats, torques)
        return self._pass3_forward_acceleration(transform_mats)
        