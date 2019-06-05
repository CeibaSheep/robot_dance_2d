import json
import numpy as np

index = './data/tq_2_second_0000000000'
name = '_keypoints.json'
data_arr = []
for i in range(0,61):
    if i<10:
        path = index+'0'+str(i)+name
    else:
        path = index+str(i)+name
    with open(path) as pose_frame:
        pose = json.load(pose_frame)
        pose_keypoints_2d = pose['people'][0].get("pose_keypoints_2d")
        pose_keypoints_2d = np.reshape(pose_keypoints_2d, (25,3))
        valid_keypoints = pose_keypoints_2d[0:9,:]
        data_arr.append(valid_keypoints)

# one = {"position": data_arr}
# with open('json_data.json', 'w') as f:
#     f.write(json.dumps(data_arr))  

np.save('data.npy', data_arr)

# jsonData = json.dumps(one)
# print(jsonData)
# fileObject = open('json_data.json', 'w')
# fileObject.write(jsonData)
# fileObject.close()

haha = np.load('data.npy')
# print(haha)