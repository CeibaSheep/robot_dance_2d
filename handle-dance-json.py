import os
import json
import numpy as np

    
def calRelativeCooridinateFromJsonInputData(input_json_file):
    with open(input_json_file) as json_file:
        raw_data = json.load(json_file)
        # extract all the 25 pose keypoints features
        pose_keypoint = raw_data['people'][0]['pose_keypoints_2d']
        # because there are 25 key points and every points have three elements(x,y,c) 
        # so I changed the list to a np array with shape of 25*3
        a = np.array(pose_keypoint).reshape(25,3)
        # extract key pionts: 0,1,2,3,4,5,6,7,8
        useful_keypoints = a[0:9,:]
        # make keypoint 8 as origin 
        origin = a[8,:]
        relative_keypoints = np.hstack((useful_keypoints[:,0:2] - origin[0:2], useful_keypoints[:,2].reshape(9,1)))
        return relative_keypoints

def calBigArmLength(all_frames_relative_keypoints):
    """
    calculate euclidean distance of key point 5 and 6, to get the big arm length.
    then find the largest one in all frames, set it to the returned big arm length.
    """
    big_arm_length = []
    frames = all_frames_relative_keypoints.shape[0]
    for i in range(frames):
        key5 = all_frames_relative_keypoints[i,5,0:2]
        key6 = all_frames_relative_keypoints[i,6,0:2]
        big_arm_length.append(np.linalg.norm(key5 - key6))
    return max(big_arm_length)

#path = "/home/gl/Desktop/skeleton/single_dance_2_second/"
path = "/home/gl/Desktop/skeleton/data/"
files = []
# r is root, d is directories, f is files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

all_frames_relative_keypoints = []

for f in files:
    relative_keypoints = calRelativeCooridinateFromJsonInputData(f)
    all_frames_relative_keypoints.append(relative_keypoints)
    
all_frames_relative_keypoints = np.array(all_frames_relative_keypoints)
big_arm_length = calBigArmLength(all_frames_relative_keypoints)
np.save("zengjiandian_all_frames_relative_keypoints.npy", all_frames_relative_keypoints)
    