#!/usr/bin/env python
# coding: utf-8

import time
import cv2
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
import pepper_kinematics as pk


def main():
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM)
    pybullet.setGravity(0, 0, -9.81)
    pybullet.setRealTimeSimulation(1)
    pepper.setAngles(pk.left_arm_tags, pk.left_arm_work_pose, 1.0)
    time.sleep(1.0)
    elements = [["table/table.urdf", [1, -1, 0], 1]]
    
    for e in elements:
        pybullet.loadURDF(
            e[0],
            basePosition=e[1],
            globalScaling=e[2],
            physicsClientId=client)
    '''
    pepper.moveTo(1, 0, -3.14/2, _async=True)
    time.sleep(6)

    for name in pepper.joint_dict.items():
        if "Finger" not in name and "Thumb" not in name:
            print(name)
    '''

    current_angles = pepper.getAnglesPosition(pk.left_arm_tags)
    current_position, current_orientation = pk.left_arm_get_position(current_angles)

    target_position = current_position
    target_position[1] = target_position[1] + 0.5 # 5 cm toward left
    target_orientation = current_orientation # This is not supported yet


    target_angles = pk.left_arm_set_position(current_angles, target_position, target_orientation)
    if target_angles.any():
        pepper.setAngles(pk.left_arm_tags, target_angles.tolist(), 1.0)

    while True:
        img = pepper.getCameraFrame()
        cv2.imshow("bottom camera", img)
        cv2.waitKey(1)


if __name__ == "__main__":
	main()
