
import os
from datetime import date
from datetime import datetime
import numpy as np
import cv2
from threading import Thread
import time
import sys
#from utils import ARUCO_DICT
import argparse
import time
import math
# import matplotlib.pyplot as plt
import random
import subprocess as sp
import shlex

from scipy.spatial.transform import Rotation as R

# Example tvec,rvec [[[0.35928761 1.3310449  3.63792386]]] [[[ 1.24638884 -1.23109941  1.14374023]]]


class MinimalPublisher():

    def __init__(self):
        # super().__init__('minimal_publisher')
        self.cc=0
        
        
    
    def get_frame(self,capture):
        return capture.read()

    def pose_esitmation(self,frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
        parameters = cv2.aruco.DetectorParameters_create()


        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
            cameraMatrix=matrix_coefficients,
            distCoeff=distortion_coefficients)

        tvec=[0]
        tv_arr=[]
        rv_arr=[]

        
        if len(corners) > 0:
            for i in range(0, len(ids)):

                # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.355, matrix_coefficients,
                                                                           distortion_coefficients) #cl
                print("For Camera to Marker, tvec, rvec are - ")
                print("T-vec:",tvec)
                print("R-vec:",rvec)
                x,y,z  = np.squeeze(tvec)                
                tvec1,rvec1 = [[x], [y], [z]], np.squeeze(rvec)
                r = R.from_rotvec(rvec1)

                R_mat = r.as_matrix()
                R_mat = np.append(R_mat, tvec1, axis=1)
                Transformation_matrix = np.append(R_mat, [[0,0,0,1]], axis=0)

                Inv = np.linalg.inv(Transformation_matrix)

                inv_tvec = Inv[:3,3]
                inv_R_mat = R.from_matrix(Inv[0:3,0:3])
                inv_rvec = inv_R_mat.as_rotvec()

                print("For Marker to Camera, calculated inverses are - ")
                print("Inv-T-vec:",inv_tvec)
                print("Inv-R-vec:",inv_rvec)
                
                ##############for draw
                cv2.aruco.drawDetectedMarkers(frame, corners)

                #Draw Axis

                cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec,tvec, 1)
                ###############for draw
                tv_arr.append(tvec)
                rv_arr.append(rvec)
            
        return frame,tv_arr,rv_arr



def main(args=None):
    aruco_dict_type = cv2.aruco.DICT_4X4_1000
    #define intrinsics,distrortion from camera_calibration file

    # k = np.array([[903.68519476,   0.0, 673.79186407],[0.0,908.6285383,366.90826658],[0.0,0.0,1.0]])
    # d = np.array([[ 0.1694113,  -0.48083569,  0.00117894,  0.00718526,  0.02905604]])

    k = np.array([[635.94094132,0.0,646.71074174],[0.0,636.25013219, 368.82371914],[0.0,0.0,1.0]])
    d = np.array([[-0.05501613,  0.08585717, -0.00044321,  0.00239813 ,-0.04214102]])



    # k=np.array([[631.6736450195312, 0.0, 629.6350708007812], [0.0, 
    # 630.770263671875, 381.8550720214844], [0.0, 0.0, 1.0]]) #ch
    # d=np.array([[-0.05571040138602257, 0.06658679246902466, 
    # -0.000520356756169349, -0.0002876412181649357, -0.021140484139323235]]) #ch
    #the rvec and tvec obtained from the api,using the initial reference frame.
    # rvec_prev=np.array([[ 2.06805926 , 0.68096472 ,-0.408]]) #ch
    # tvec_prev=np.array([[-0.02987605, -0.17564143,  2.7215575]]) #ch #bot at 13.8m
    # #####find the transformation matrix to use later
    # rot_mat=cv2.Rodrigues(rvec_prev)
    # rot_mat_inv=np.linalg.inv(rot_mat[0])

    # transformation_mat= np.c_[rot_mat[0],tvec_prev.T]
    # transformation_mat=np.r_[transformation_mat,[np.array([0,0,0,1])]]
    # transformation_mat_inv=np.linalg.inv(transformation_mat)

    #########frame capture
    video = cv2.VideoCapture(6)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #clforvideo
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    
    status = 0
    frame = None

    count=0


    minimal_publisher = MinimalPublisher()



    while True:
        status_cam1, frame = minimal_publisher.get_frame(video)
        if not status_cam1:
            break
        count+=1
        output,tv_arr,rv_arr= minimal_publisher.pose_esitmation(frame, aruco_dict_type, k, d)
 
        ####################################
        cv2.namedWindow("output", cv2.WINDOW_NORMAL) 
        cv2.imshow('output', output)

        key = cv2.waitKey(1) & 0xFF
        

        if key==ord('q'):
            break
        #####################################


if __name__ == '__main__':
    main()
