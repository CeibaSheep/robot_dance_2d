# -*- coding: utf-8 -*-
import numpy as np
import math

def computeRelativePosition(origData):
    relativePosition = []
    for frame in origData:
        origNode = frame[8,0:2]
        axisValue = frame[:,0:2] - origNode
        cValue = frame[:,2]
        relativePosition.append(np.insert(axisValue, 2, values = cValue, axis = 1))
    return relativePosition

def computeArmLen(relativeData):
    armArr = []
    neckLength = []
    lShoulder = 2
    lWrist = 4
    rShoulder = 5
    rWrist = 7
    nose = 0
    neck = 1
    for frame in relativeData:
        leftArm = math.sqrt(pow((frame[lShoulder,0]-frame[lWrist,0]),2) + pow((frame[lShoulder,1]-frame[lWrist,1]),2))
        rightArm = math.sqrt(pow((frame[rShoulder,0]-frame[rWrist,0]),2) + pow((frame[rShoulder,1]-frame[rWrist,1]),2))
        armArr.append([leftArm, rightArm])
        zeroToOne = math.sqrt(pow((frame[nose,0]-frame[neck,0]),2) + pow((frame[nose,1]-frame[neck,1]),2))
        neckLength.append(zeroToOne)
    return np.array(armArr).max(), np.array(neckLength).max()

def computeAngle(frame, indexList = []):
    if len(indexList) == 3:
        v1 = [frame[indexList[0],0]-frame[indexList[1],0], frame[indexList[0],1]-frame[indexList[1],1]]
        v2 = [frame[indexList[1],0]-frame[indexList[2],0], frame[indexList[1],1]-frame[indexList[2],1]]
    else:
        v1 = [frame[indexList[0],0]-frame[indexList[1],0], frame[indexList[0],1]-frame[indexList[1],1]]
        v2 = [frame[indexList[2],0]-frame[indexList[3],0], frame[indexList[2],1]-frame[indexList[3],1]]
    
    vecProduct = v1[0]*v2[0] + v1[1]*v2[1]
    v1Value = math.sqrt(pow(v1[0],2) + pow(v1[1],2))
    v2Value = math.sqrt(pow(v2[0],2) + pow(v2[1],2))
    cosValue = vecProduct / (v1Value * v2Value)
    # print ('cosValue:', cosValue)
    return cosValue

def distance(frame, index1, index2):
    dist = math.sqrt(pow((frame[index1,0]-frame[index2,0]),2) + pow((frame[index1,1]-frame[index2,1]),2))
    return dist

def getRollAngle(name, cos):
    if name == 'le' or name == 'rs':
        if cos > 0.5:
            return -30
        else:
            return -85
    elif name == 'ls' or name == 're':
        if cos > 0.5:
            return 30
        else:
            return 85

def getYawOrPitchAngle(frame, index1, index2, cos):
    if cos > 0.5 and cos < 0.94: # 60degree
        if frame[index1, 0] < frame[index2, 0]:
            return 90
        else:
            return -90
    elif cos >= 0.938: #20 degree
        return 0
    elif cos <=0.5:
        if frame[index1, 0] < frame[index2, 0]:
            return 45
        else:
            return -45

def computeRobotStatus(relativeData, armLength, neckLength):
    robotStatus = []
    for frame in relativeData:
        # headPitch
        headPitch = distance(frame, 0, 1)
        if headPitch > (neckLength*0.8):
            headPitch = 0
        else:
            headPitch = 20
        #headYaw
        headYawCos = computeAngle(frame, [0, 1, 8])
        print('headYawAngle', headYawCos)
        if headYawCos < 0.94: # 20degree
            if frame[0,0] > frame[1,0]: # turn left
                headYaw = 45
            else:
                headYaw = -45 # turn right
        else:
            headYaw = 0
        #hiproll
        if frame[1, 0] >= 10: # error = 10
            hipRoll = 20 # left
        elif frame[1, 0] <= -10:
            hipRoll = -20
        elif frame[1, 0]<10 and frame[1,0]>-10:
            hipRoll = 0
        #lElbowRoll
        # cos = computeAngle(frame, [5, 6, 7])
        # lElbowRoll = getRollAngle('le', cos)
        # #lElbowYaw
        # cos = computeAngle(frame, [6, 7, 1, 8])
        # lElbowYaw = getYawOrPitchAngle(frame, 6, 7, cos)
        # #lShoulderPitch
        # cos = computeAngle(frame, [5, 6, 1, 8])
        # lShoulderPitch = getYawOrPitchAngle(frame, 5, 6, cos)
        # #lShoulderRoll
        # cos = distance(frame, 5, 7)/armLength
        # lShoulderRoll = getRollAngle('ls', cos)
        # #rElbowRoll
        # cos = computeAngle(frame, [2, 3, 4])
        # rElbowRoll = getRollAngle('re', cos)
        # #rElbowYaw
        # cos = computeAngle(frame, [3, 4, 1, 8])
        # rElbowYaw = getYawOrPitchAngle(frame, 3, 4, cos)
        # # rShoulderPitch
        # cos = computeAngle(frame, [2, 3, 1, 8])
        # rShoulderPitch = getYawOrPitchAngle(frame, 2, 3, cos)
        # # rShoulderRoll
        # cos = distance(frame, 2, 4)/armLength
        # rShoulderRoll = getRollAngle('rs', cos)
        # # status = [{'headPitch':headPitch,'headYaw':headYaw,'hipRoll':hipRoll,'lElbowRoll':lElbowRoll,\
        # #         'lElbowYaw':lElbowYaw,'lShoulderPitch':lShoulderPitch,'lShoulderRoll':lShoulderRoll,'rElbowRoll':rElbowRoll,\
        # #         'rElbowYaw':rElbowYaw,'rShoulderPitch':rShoulderPitch,'rShoudlerRoll':rShoulderRoll}]
        # status = [headPitch,headYaw,0,hipRoll,0,lElbowRoll,lElbowYaw,90,lShoulderPitch, lShoulderRoll,0, rElbowRoll, rElbowYaw, 90, rShoulderPitch, rShoulderRoll,0]
        # robotStatus.append(status)
    return robotStatus

def main():
    origData = np.load('data.npy')
    relativeData = computeRelativePosition(origData)
    armLength, neckLength = computeArmLen(relativeData)
    # print('armLength：', armLength, 'neckLength:', neckLength)
    robotStatus = computeRobotStatus(relativeData, armLength, neckLength)
    np.save('robotStatus.npy', robotStatus)
               
if __name__ == "__main__":
    main()
    print('done')