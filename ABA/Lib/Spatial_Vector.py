
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

# for check
def _vector3(vec: npt.ArrayLike, name: str) -> FloatArray:
    result = np.asarray(vec, dtype=np.float64)
    if result.shape != (3,):
        raise ValueError(f"{name} must have shape (3,), got {result.shape}")
    return result

# for check
def _rotation_matrix(rotation: npt.ArrayLike) -> FloatArray:
    result = np.asarray(rotation, dtype=np.float64)
    if result.shape != (3, 3):
        raise ValueError(
            f"rotation_matrix must have shape (3, 3), got {result.shape}"
        )
    return result


# 歪対称行列の生成
def get_skew_matrix(vec: npt.ArrayLike) -> FloatArray:
    """Return the matrix S such that S @ x equals vec cross x."""
    x, y, z = _vector3(vec, "vec")
    return np.array(
        [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]],
        dtype=np.float64,
    )

# 歪対称対称行列からベクトルを抽出
def get_vec_from_skew_matrix(mat: npt.ArrayLike) -> FloatArray:
    """Recover a vector from its 3-by-3 skew-symmetric matrix."""
    matrix = np.asarray(mat, dtype=np.float64)
    if matrix.shape != (3, 3):
        raise ValueError(f"mat must have shape (3, 3), got {matrix.shape}")
    if not np.allclose(matrix + matrix.T, 0.0):
        raise ValueError("mat must be skew-symmetric")
    return np.array([matrix[2, 1], matrix[0, 2], matrix[1, 0]])


def get_Rotation_matrix_on_x(th: float) -> FloatArray:
    c, s = np.cos(th), np.sin(th)
    return np.array(
        [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]],
        dtype=np.float64,
    )

def get_Rotation_matrix_on_y(th: float) -> FloatArray:
    c, s = np.cos(th), np.sin(th)
    return np.array(
        [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]],
        dtype=np.float64,
    )

def get_Rotation_matrix_on_z(th: float) -> FloatArray:
    c, s = np.cos(th), np.sin(th)
    return np.array(
        [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]],
        dtype=np.float64,
    )

def create_spatial_velocity(om, vel) -> FloatArray:
    om = _vector3(om, "omega")
    vel = _vector3(vel, "velocity")
    return np.concatenate([om, vel])

def get_element_of_motion_vector(vector):
    vector = _spatial_vector6(vector)
    return vector[:3], vector[3:]

def create_spatial_accleration(alpha, acc, sp_vec):
    alpha = _vector3(alpha, "alpha")
    acc = _vector3(acc, "acc")

    omega, vel = get_element_of_motion_vector(sp_vec)

    return np.concatenate([
        alpha, 
        acc - np.cross(omega, vel)
    ])

# for check
def _spatial_vector6(vector: npt.ArrayLike) -> FloatArray:
    result = np.asarray(vector, dtype=np.float64)
    if result.shape != (6,):
        raise ValueError(f"spatial vector must have shape (6,), got {result.shape}")
    return result

def spatial_motion_cross_matrix(sp_velocity):
    sp_vel = _spatial_vector6(sp_velocity)
    omega, v = get_element_of_motion_vector(sp_vel)

    skew_om = get_skew_matrix(omega)
    skew_v = get_skew_matrix(v)
    return np.block([
        [skew_om, np.zeros((3,3))],
        [skew_v,  skew_om]
    ])

def spatial_force_cross_matrix(sp_velocity):
    return -spatial_motion_cross_matrix(sp_velocity).T


def get_spatial_motion_transform_matrix(rot_mat:npt.ArrayLike, r_op:npt.ArrayLike):
    r_op = _vector3(r_op, "r_op")
    skew_r = get_skew_matrix(r_op)
    rot_mat = _rotation_matrix(rot_mat)
    return np.block([
                    [rot_mat, np.zeros((3,3))],
                    [-skew_r @ rot_mat, rot_mat]
                    ])

def get_spatial_force_transform_matrix(rot_mat:npt.ArrayLike, r_op:npt.ArrayLike):
    r_op = _vector3(r_op, "r_op")
    skew_r = get_skew_matrix(r_op)
    rot_mat = _rotation_matrix(rot_mat)
    return np.block([
                    [rot_mat, -skew_r @ rot_mat],
                    [np.zeros((3,3)), rot_mat]
                    ])

def get_spatial_inertia(Ig:np.array, m:float, r_og:np.array):

    r = get_skew_matrix(r_og)

    return (np.block([
        [Ig - m * r @ r, m * r],
        [-m * r , m * np.eye(3)]
    ])
    )

# for check
def _spatial_inertia(vector: npt.ArrayLike) -> FloatArray:
    result = np.asarray(vector, dtype=np.float64)
    if result.shape != (6,6):
        raise ValueError(f"spatial vector must have shape (6,6), got {result.shape}")
    return result


def calculete_net_spatial_newton_euler_spatial_force(sp_I:npt.ArrayLike, sp_acc:npt.ArrayLike, sp_vel:npt.ArrayLike):
    sp_acc = _spatial_vector6(sp_acc)
    sp_vel = _spatial_vector6(sp_vel)
    sp_I = _spatial_inertia(sp_I)

    net_force = sp_I @ sp_acc + spatial_force_cross_matrix(sp_vel)@sp_I@sp_vel

    return net_force
