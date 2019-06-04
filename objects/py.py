#!/usr/bin/env python
# coding: utf-8

import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager


def main():
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    pybullet.setAdditionalSearchPath("C:\Users\Propriétaire\Desktop\4 ETI\Projet Majeur\projet\objects")

    pybullet.loadURDF(
        "totem_avion.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)
    pepper.goToPosture("Stand", 0.6)

    pybullet.loadURDF(
        "totem_pomme.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)
    
    pybullet.loadURDF(
        "totem_banane.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)

    pybullet.loadURDF(
        "totem_banane.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)

    pybullet.loadURDF(
        "totem_banane.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)

    pybullet.loadURDF(
        "totem_banane.urdf",
        basePosition=[1, -1, 0.5],
        globalScaling=10.0,
        physicsClientId=client)

if __name__ == "__main__":
    main()