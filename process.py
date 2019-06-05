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
    
    return
def distance(frame, index1, index2):
    dist = math.sqrt(pow((frame[index1,0]-frame[index2,0]),2) + pow((frame[index1,1]-frame[index2,1]),2))
    return dist

def computeRobotStatus(relativeData, armLength, neckLength):
    robotStatus = []
    for frame in relativeData:
        headPitch = distance(frame, [0, 1])>(neckLength*0.3)?20:0
        headYaw = (frame)
        hipRoll = computeHipRoll(frame)
        lElbowRoll = computeElbowRoll(frame,)
        lElbowYaw = computeElbowYaw(frame)
        lShoulderPitch = computeShoulderPitch()
        lShoulderRoll = computeShoulderRoll()
        rElbowRoll = computeElbowRoll(frame,)
        rElbowYaw = computeElbowYaw(frame)
        rShoulderPitch = computeShoulderPitch()
        rShoulderRoll = computeShoulderRoll()
        status = [{'headPitch':headPitch,'headYaw':headYaw,'hipRoll':hipRoll,'lElbowRoll':lElbowRoll,\
                'lElbowYaw':lElbowYaw,'lShoulderPitch':lShoulderPitch,'lShoulderRoll':lShoulderRoll,'rElbowRoll':rElbowRoll,\
                'rElbowYaw':rElbowYaw,'rShoulderPitch':rShoulderPitch,'rShoudlerRoll':rShoulderRoll}]
        robotStatus.append(status)
    return robotStatus   

def main():
    origData = np.load('data.npy')
    relativeData = computeRelativePosition(origData)
    armLength, neckLength = computeArmLen(relativeData)
    print('armLength：', armLength, 'neckLength:', neckLength)
    robotStatus = computeRobotStatus(relativeData, armLength, neckLength)
               
if __name__ == "__main__":
    main()
    print('done')