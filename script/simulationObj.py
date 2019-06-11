#!/usr/bin/env python
# coding: utf-8

import time
import cv2
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
from qibullet import Camera
import pepper_kinematics as pk
from detection import detection


def main():
    path = '../images/detection.png'
    
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM, Camera.K_720p )
    pybullet.setGravity(0, 0, -9.81)
    pybullet.setRealTimeSimulation(1)

    pepper.setAngles(pk.left_arm_tags, pk.left_arm_work_pose, 1.0)
    pepper.setAngles(pk.right_arm_tags, pk.right_arm_initial_pose, 1.0)
    time.sleep(1.0)

    elements = [["table/table.urdf", [1, -1, 0], [0, 0, 0], 1], ["../objects/totem_avion.urdf", [1, -0.75, 0.65], [0, 0, 0.9], 1],
               ["../objects/totem_banane.urdf", [1.18, -0.75, 0.65], [0, 0, 0], 1], ["../objects/totem_raquette.urdf", [0.82, -0.75, 0.65], [0, 0, 0], 1]]
    
    for e in elements:
        pybullet.loadURDF(
            e[0],
            basePosition=e[1],
            baseOrientation=pybullet.getQuaternionFromEuler(e[2]),
            globalScaling=e[3],
            physicsClientId=client)

    pepper.setAngles('HeadPitch', -0.34, 1.0)
    pepper.moveTo(1, -0.2, -3.14/2)
    img = pepper.getCameraFrame()
    cv2.imwrite(path, img)
    pepper.unsubscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM) 	
    print "photo prise"
    
    pepper.moveTo(0.2, 0, 0)

    obj = detection()
    result = obj.detect(path)
    print "------------------"
    print result

    
    '''
    for name in pepper.joint_dict.items():
        print(name)
    '''
    
    pepper.setAngles('LHand', 1, 1.0)

    current_angles = pepper.getAnglesPosition(pk.left_arm_tags)
    current_angles[4] = 0.17
    current_position, current_orientation = pk.left_arm_get_position(current_angles)
    
    target_position = current_position
    target_position[0] = target_position[0] + 0.05
    target_position[1] = target_position[1] + 0.03
    target_position[2] = target_position[2]
    target_orientation = current_orientation # This is not supported yet

    target_angles = pk.left_arm_set_position(current_angles, target_position, target_orientation)
    if target_angles:
        pepper.setAngles(pk.left_arm_tags, target_angles.tolist(), 1.0)
    while(1):
        pass

if __name__ == "__main__":
	main()
