# Vision-based-Navigation

## Finding the tf of the camera 

### 1. Calibrate the camera
Add the images (10-14) with the chessboard to the calibration folder. Note the K and D matrices and update it in the camera_pose.py script. \
```
python3 camera_calibration.py calibration/
```
### 2. Getting the camera coordinate with respect to ARUCO marker
Keep the camera in the desired location and run the camera_pose.py script. Note down the tvec and rvec values. This is the camera pose with respect to the marker.
```
python3 camera_pose.py 
```
### 3. Finding the Lidar to Marker transform 
Physcially measure the translation and rotation of the marker with respect to the lidar.
### 4. Adding the tfs in the launch file


## Installing and running spatio-temporal voxel layer

### 1. Installing the package from binaries or souce 
### 2. Adding the config parameters to costmap.yaml
### 3. Adding the plugin in local_costmap.yaml and/or global_costmap.yaml
### 4. Adding/Checking the map to camera_aligned_to_depth_color_frame
### 5. Use NavStack as usual.

