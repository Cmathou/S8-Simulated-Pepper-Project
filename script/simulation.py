#!/usr/bin/env python
# coding: utf-8

import time
import cv2
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager


def main():
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)
    
    elements = [["table/table.urdf", [1, -1, 0], 1]]
    
    for e in elements:
        pybullet.loadURDF(
            e[0],
            basePosition=e[1],
            globalScaling=e[2],
            physicsClientId=client)

    pepper.moveTo(1, 0, -3.14/2, _async=True)

    while True:
        img = pepper.getCameraFrame()
        cv2.imshow("bottom camera", img)
        cv2.waitKey(1)


if __name__ == "__main__":
	main()
