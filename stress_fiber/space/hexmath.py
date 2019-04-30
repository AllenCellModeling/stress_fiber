# encoding: utf-8
"""
Grid-scale computing. 

Support the calculation of adjacency and distance on a hexagonal grid given
various coordinate systems.
"""

import itertools
import numpy as np


class HexMath:
    """Hexagonal coordinate helper functions, assuming pointy side up.
    This draws heavily from the excellent reference:
        https://www.redblobgames.com/grids/hexagons/
    """

    def cube_to_axial(i, j, k):
        """Convert cube coordinates to axial coordinates"""
        q, r = i, k
        return q, r

    def axial_to_cube(q, r):
        """Convert axial coordinates to cube coordinates"""
        i, k = q, r
        j = -i - k
        return i, j, k

    def cube_to_offset(i, j, k):
        """Convert cube coordinates to offset coordinates, odd rows shifted by +1/2 col"""
        col = i + (k - (k & 1)) // 2
        row = k
        return col, row

    def offset_to_cart(col, row):
        """Convert offset coordinates (odd row shifted +1/2 col), into Cartesian coordinates"""
        x = np.sqrt(3) * (col + 0.5 * (row & 1))
        y = 3 / 2 * row
        return x, y

    def axial_to_cart(q, r):
        """Convert axial coordinates into cartesian coordinates"""
        x = np.sqrt(3) * q + np.sqrt(3) / 2 * r
        y = 3 / 2 * r
        return x, y

    def cube_to_cart(i, j, k):
        """Convert cube coordinates to cartesian"""
        col, row = HexMath.cube_to_offset(i, j, k)
        x, y = HexMath.offset_to_cart(col, row)
        return x, y

    def cube_distance(i_1, j_1, k_1, i_2, j_2, k_2):
        """Distance between two hexagons in cube coordinates"""
        a = np.array((i_1, j_1, k_1))
        b = np.array((i_2, j_2, k_2))
        dist = np.sum(np.abs(np.subtract(a, b))) / 2
        return dist

    def cube_within_radius(i, j, k, n, original=(0, 0, 0)):
        """Is this new location within a radius from an original (default origin)"""
        within_radius = HexMath.cube_distance(i, j, k, *original) <= n
        return within_radius

    def cube_validate(i, j, k):
        """Is this a valid cube coordinate?"""
        valid = (i + j + k) == 0
        return valid

    def cube_neighbors(i, j, k):
        """Give me a list of neighboring hexagons"""
        neighbors = [
            (i, j + 1, k - 1),
            (i + 1, j, k - 1),
            (i + 1, j - 1, k),
            (i, j - 1, k + 1),
            (i - 1, j, k + 1),
            (i - 1, j + 1, k),
        ]
        return neighbors

    def cube_to_array_indices(i, j, k, n):
        """Convert cube coordinates to array location for a grid of radius n"""
        x = i + n
        y = k + n
        return x, y

    def create_grid_array(n):
        """Create a list of hex locations for a grid of radius n"""
        # Create grid
        scan = list(range(-n, n + 1))
        grid = [[[] for q in scan] for r in scan]
        # Create tests to ensure location is within roi and valid
        within_radius = lambda i, j, k: HexMath.cube_within_radius(i, j, k, n)
        belongs = lambda ijk: within_radius(*ijk) and HexMath.cube_validate(*ijk)
        # Populate grid with coordinates
        for q, r in itertools.product(scan, scan):
            i, j, k = HexMath.axial_to_cube(q, r)
            if belongs((i, j, k)):
                x, y = HexMath.cube_to_array_indices(i, j, k, n)
                grid[x][y] = {"cube": (i, j, k)}
        grid = np.array(grid)
        return grid