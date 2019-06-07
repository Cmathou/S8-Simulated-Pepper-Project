#!/usr/bin/env python
# coding: utf-8

import time
import argparse
import qi
import cv2
import pybullet
import pybullet_data
from qibullet import PepperVirtual
from qibullet import SimulationManager
from qibullet import Camera
import pepper_kinematics as pk
from detection import detection


def arm_pos(pepper, x, y, z, s):
    current_angles = pepper.getAnglesPosition(pk.left_arm_tags)
    current_position, current_orientation = pk.left_arm_get_position(current_angles)
    
    target_position = current_position
    target_position[0] = target_position[0] + x
    target_position[1] = target_position[1] + y
    target_position[2] = target_position[2] + z
    target_orientation = current_orientation # This is not supported yet

    target_angles = pk.left_arm_set_position(current_angles, target_position, target_orientation)
    if target_angles.any():
        pepper.setAngles(pk.left_arm_tags, target_angles.tolist(), s)

def main(session):
    path = '../images/detection.png'
    
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
    '''
    ALMemory = session.service("ALMemory")
    ALMemory.declareEvent('item')
    while(1):
        print ALMemory.getData('item')
        time.sleep(2)
    '''
    
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    pepper.subscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM, Camera.K_720p )
    pybullet.setGravity(0, 0, -9.81)
    pybullet.setRealTimeSimulation(1)

    pepper.setAngles(pk.left_arm_tags, pk.left_arm_work_pose, 1.0)
    #pepper.setAngles(pk.right_arm_tags, pk.right_arm_initial_pose, 1.0)
    pepper.setAngles('RShoulderPitch', 3.14/2, 1.0)
    time.sleep(1.0)
    
    config = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    elements = [["table/table.urdf", [1, -1, 0], [0, 0, 0], 1], ["../objects/totem_avion.urdf", [1, -0.65, 0.65], [0, 0, 1.57], 1],
               ["../objects/totem_banane.urdf", [1.18, -0.65, 0.65], [0, 0, 0], 1], ["../objects/totem_raquette.urdf", [0.82, -0.65, 0.65], [0, 0, 0], 1]]

    for e in elements:
        pybullet.loadURDF(
            e[0],
            basePosition=e[1],
            baseOrientation=pybullet.getQuaternionFromEuler(e[2]),
            globalScaling=e[3],
            physicsClientId=client)

    pepper.setAngles('HeadPitch', -0.34, 1.0)
    pepper.moveTo(1, -0.15, -3.14/2)

    
    img = pepper.getCameraFrame()
    cv2.imwrite(path, img)
    pepper.unsubscribeCamera(PepperVirtual.ID_CAMERA_BOTTOM) 	
    print "photo prise"
    obj = detection()
    result = obj.detect(path)
    print "------------------"
    print result
    
    '''
    for name in pepper.joint_dict.items():
        print(name)
    '''
    
    arm_pos(pepper, -0.10, 0.04, -0.08, 1.0)
    
    
    pepper.setAngles('LHand', 1, 1.0)
    pepper.setAngles('LWristYaw', 0.10, 1.0)
    pepper.moveTo(0.21, 0, 0)

    arm_pos(pepper, 0.11, 0, 0, 0.5)
    
    time.sleep(5)
    pepper.setAngles('LHand', 0, 0.5)
    time.sleep(1)

    arm_pos(pepper, 0, 0, 0.05, 1.0)
    
    while(1):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
