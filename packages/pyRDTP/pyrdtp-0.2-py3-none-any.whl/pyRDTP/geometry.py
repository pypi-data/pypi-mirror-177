"""Geometry operations with molecules"""

import math
import numpy as np

DIM_DICT = {'x': 0, 'y': 1, 'z': 2}  # Axis translation


def pbc_norm(point1, point2, box_size):
    """This functions determines if two points belong to the same box using the
    minimum image convention in a box of n dimensions.

    Args:
        point1 (:obj`np.ndarray` 1d n): Array containing the coordinates of
            one of the points to compare.
        point2 (:obj`np.ndarray` 1d n): Array containing the coordinates of
            the second point to compare.
        box_size (:obj`np.ndarray` 1d n): Array containing the norm of the
            vectors that define the box.

    Returns:
        float with the norm of the minimum distance between the two
            points.
    """
    diff_vec = point2 - point1
    for dimension, value in enumerate(diff_vec):
        if abs(value) > 0.5:
            if point2[dimension] < point1[dimension]:
                point2[dimension] += 0.5
            else:
                point2[dimension] -= 0.5
    diff_vec = point2 - point1
    new_norm = np.linalg.norm(diff_vec.dot(box_size))
    return new_norm


def rotation_matrix(axis, angle):
    """Generates a clockwise rotation matrix using the Euler-Rodrigues formula.

    Args:
        axis (:obj`tuple` of 3 floats): Coordinates of the axis.
        angle (float): Rotation angle, in radians.

    Returns:
        :obj`np.ndarray` 3x3 rotation matrix for the given axis/angle.

    Raises:
        TypeError if the angle value is not a float.
    """

    try:
        angle = float(angle)
        axis = np.asarray(axis, dtype=float)
    except ValueError:
        raise TypeError('could not convert angle argument to float')
    else:
        axis = axis/math.sqrt(np.dot(axis, axis))  # Convert to unit vec

        a_value = math.cos(angle / 2.)
        b_value, c_value, d_value = axis * math.sin(angle / 2.)

        aa_value, bb_value = a_value**2, b_value**2
        cc_value, dd_value = c_value**2, d_value**2

        diag = np.ones(3)
        diag[0] = aa_value + bb_value - cc_value - dd_value  # Diagonal
        diag[1] = aa_value + cc_value - bb_value - dd_value  # ...
        diag[2] = aa_value + dd_value - bb_value - cc_value  # ...

        ab_value, ac_value = a_value * b_value, a_value * c_value
        ad_value, bc_value = a_value * d_value, b_value * c_value
        bd_value, cd_value = b_value * d_value, c_value * d_value

        matrix = [[diag[0], 2*(bc_value-ad_value), 2*(bd_value+ac_value)],
                  [2*(bc_value+ad_value), diag[1], 2*(cd_value-ab_value)],
                  [2*(bd_value-ac_value), 2*(cd_value+ab_value), diag[2]]]
        matrix = np.asarray(matrix, dtype=float)

        return matrix


def rotation_xyz_axis(matrix, center, **rotations):
    """Generates a clockwise rotation matrix for the x, y, z axes
    centered in a point.

    Args:
        center(:obj`tuple` len 3): Coords of the central point.
        **coords = Axis and rotation angles.

    Returns:
        :obj`np.darray` 3x3 rotation matrix.
    """

    if len(center) != 3:
        raise NotImplementedError('3 dimensional vector expected')
    elif not set(rotations.keys()).issubset(DIM_DICT.keys()):
        raise NotImplementedError('rotations keys must be x, y, z')
    else:
        for dimension, angle in rotations.items():
            print(dimension, angle)
            move_vector = np.zeros(3) - center
            matrix = matrix - move_vector
            rotate_axis = np.zeros(3)
            rotate_axis[DIM_DICT[dimension]] = 1.
            matrix.dot(rotation_matrix(rotate_axis, angle))
            matrix = matrix + move_vector
    return matrix


def plane_fit(points):
    """
    Given an array, points, of shape (n, d) representing the points in
    d-dimensional space, fit an d-dimensional plane to the points using
    SVD.

    Args:
        points (array like of shape (n, d)): Points in the d-dimensional space.

    Returns:
        Two values. The first one is the point cloud centroid and the second
        one the normal of the plane.

    Notes:
        Response from stack overflow:
    """
    import numpy as np
    from numpy.linalg import svd
    # Collapse trialing dimensions
    new_points = np.reshape(points, (np.shape(points)[0], -1)).T
    ctr = new_points.mean(axis=1)
    x_points = new_points - ctr[:,np.newaxis]
    m_mat = np.dot(x_points, x_points.T) # Could also use np.cov(x) here.
    return ctr, svd(m_mat)[0][:,-1]


def unit_vector(vector):
    """Returns the unit vector of the vector.

    Args:
        vector (vector-like of n dimensions): Vector that will be used to
            calculate the unit.

    Returns:
        obj:`np.ndarray` of floats and dimension n with the unit vector.

    """
    return vector / np.linalg.norm(vector)


def angle_between(vector_1, vector_2):
    """Calculate the angle between two vectors

    Args:
        vector_1, vector_2 (vector-like of n dimensions): Vectors between which
            the angle will be computed.

    Returns:
        Angle between the vectors.
    """
    vector_u1 = unit_vector(vector_1)
    vector_u2 = unit_vector(vector_2)
    return np.arccos(np.clip(np.dot(vector_u1, vector_u2), -1.0, 1.0))
