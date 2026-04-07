import serial
import time
import pydirectinput
serialCom = serial.Serial('COM8', 9600)

#Resets the Arduino at the start
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)
wPressed = aPressed = sPressed = dPressed = False
# pressThreshold = 10
holdThreshold = 7.5
pressed = False
while(1):

    binarySentence = serialCom.readline()
    decodedSentence = binarySentence.decode('utf-8').strip('\r\n')
    print(decodedSentence)
    decodedSentence = decodedSentence.split()
    movementTypes = [decodedSentence[0], decodedSentence[2], decodedSentence[4], decodedSentence[6]]
    movementValues = [decodedSentence[1], decodedSentence[3], decodedSentence[5], decodedSentence[7]]
    #Last word of the sentence
    for index, value in enumerate(movementValues):
        movementValues[index] = abs(float(value))
    if movementValues[0] >= holdThreshold and wPressed is False:
        pydirectinput.keyDown('W')
        wPressed = True
    elif movementValues[0] < holdThreshold and wPressed is True:
        pydirectinput.keyUp('W')
        wPressed = False
    if movementValues[1] >= holdThreshold and aPressed is False:
        pydirectinput.keyDown('A')
        aPressed = True
    elif movementValues[1] < holdThreshold and aPressed is True:
        pydirectinput.keyUp('A')
        aPressed = False
    if movementValues[2] >= holdThreshold and sPressed is False:
        pydirectinput.keyDown('S')
        sPressed = True
    elif movementValues[2] < holdThreshold and sPressed is True:
        pydirectinput.keyUp('S')
        sPressed = False
    if movementValues[3] >= holdThreshold and dPressed is False:
        pydirectinput.keyDown('D')
        dPressed = True
    elif movementValues[3] < holdThreshold and dPressed is True:
        pydirectinput.keyUp('D')
        dPressed = False
    #     wLastValue = movementValue
    # elif movementType == 'A':
    #     print(movementValue - aLastValue)
    #     if movementValue - aLastValue > pressThreshold:
    #         keyboard.send('A')
    #     aLastValue = movementValue
    # elif movementType == 'S':
    #     if movementValue - sLastValue > pressThreshold:
    #         keyboard.send('S')
    #     sLastValue = movementValue
    # elif movementType == 'D':
    #     if movementValue - dLastValue > pressThreshold:
    #         keyboard.send('D')
    #     dLastValue = movementValue
