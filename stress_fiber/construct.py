# encoding: utf-8
"""
Make a world
CDW 2019
"""

import itertools
import numpy as np

from . import space
from .actin import Actin
from .anchor import Anchor
from .alpha_actinin import AlphaActinin

np.random.seed()  # Ensure proper seeding


def create_test_world(radius, span, n_actin, n_actinin):
    """Create a world of given radius with n_actin and n_actinin per tract"""
    tractspace = space.TractSpace(radius)
    for tract in tractspace.all_tracts:
        actins = []
        anchors = []
        for _ in range(n_actin):
            rise = 2.77
            pairs = np.random.randint(4, span // rise - 4)
            x = np.random.rand() * (span - pairs * rise)
            actins.append(Actin(x, pairs, tract))
            # Anchor first and last tenth
            if x < span*0.1:
                anchors.append(Anchor(x, actins[-1].pairs[0]))
            x_end = actins[-1].pairs_x[-1]
            if x_end > span*0.9:
                anchors.append(Anchor(x_end, actins[-1].pairs[-1]))
        actinins = []
        for _ in range(n_actinin):
            actinins.append(AlphaActinin(np.random.rand() * (span - 10), tract))
        tract.mols["actin"] = actins
        tract.mols["anchor"] = anchors
        tract.mols["actinin"] = actinins
    world = World(tractspace)
    return world


class World:
    """Keep track of a tract space, simulation time, and metadata"""

    def __init__(self, tractspace):
        """Save the tractspace, initiate record keeping"""
        self.tractspace = tractspace
        self.time = 0

    def step(self):
        """Step forward one tick"""
        self.time += 1
        for tract in np.random.permutation(self.tractspace.all_tracts):
            all_mols = list(itertools.chain(*tract.mols.values()))
            for mol in np.random.permutation(all_mols):
                mol.step()
