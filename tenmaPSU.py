'''
A script for automation of lab power supply "Tenma 72-2540"

Idea is to slap this module in appropriate projects where required

serial.tools.list_ports is used to find the lab power supply, allowing
automatic connection to the appropriate COM Port it is connected to

Voltage settings are limited to 0-31V, 2 decimal places
Current settings are limited to 0-5.1A, 3 decimal places

Setting to a value outside of the range will result in voltage/current being set to upper/lower limit on PSU side

For example:

    Set Voltage to 32V, Voltage is set to 31V
    Set Current to -5A, Current is set to 0A

TBD: 

    Testing of multiple serial ports
        Not sure how multiple serial ports receive/transmit will work 

Current output measurement seems to be pretty terribad, 0.011A reading can be shown as 0.004A on PSU
Will have to do further testing to check for current limits, whether will allow for >5.1A output while meter is showing <5.1A

If OCP is enabled and PSU goes into C.C. , it prevents output.

Relevant data:

Datasheet: https://www.farnell.com/datasheets/3217055.pdf

USB VID of Tenma 72-2540 = USB VID:PID=0416:5011

IDN query return = TENMA 72-2540 V5.5 SN:05243173

'''

import serial
import serial.tools.list_ports
import time

Delay = 0.25
def ListCOMPorts():

    '''
    ConnectedItems = list(serial.tools.list_ports.comports())
    
    for port in ConnectedItems:

        if(port[2].startswith("USB VID:PID=0416:5011")):

            PowerSupplyCOMPort = port[0]

    try:                        # Pretty craptacular way of checking whether variable has been assigned, needs to be redone
        PowerSupplyCOMPort  

    except:
        raise Exception("Power Supply not detected, check connection")

    return(PowerSupplyCOMPort)

    '''
    #Better Alternative?

    ConnectedItems = list(serial.tools.list_ports.comports())

    PowerSupplyCOMPort = None

    for port in ConnectedItems:

        if(port[2].startswith("USB VID:PID=0416:5011")):

            PowerSupplyCOMPort = port[0]

    if PowerSupplyCOMPort == None:
        raise Exception("Power Supply not detected, check connection")

    return(PowerSupplyCOMPort)
    
    

def ConnectToCOMPort(COMPort):

    global ser

    try:
        ser = serial.Serial(

            port = COMPort,
            baudrate = 9600,
            timeout = 0.1

        )
        
        ser.write("*IDN?".encode())

        if(ser.readline().decode() == "TENMA 72-2540 V5.5 SN:05243173"):
            pass    # Idea with this is that if a wrong IDN is returned it'll fail out with the try except

        print("Serial port at " + COMPort + " successfully opened")
        
    except:
        # Need to do some error catching or something
        print("Was unable to open Serial Port")


'''
Voltage/Current Setting Functions
The TENMA 72-2540 is a 1 channel power supply
With a multichannel power supply there could be use of concatenation to select the appropriate channels
But for now the default '1' channel will be used
'''

def SetOutputVoltage(Voltage):

    VoltageString = "VSET1:" + str(Voltage)
    print("Voltage String: " + VoltageString)

    ser.write(VoltageString.encode())
    time.sleep(Delay)

def SetOutputCurrent(Current):

    CurrentString = "ISET1:" + str(Current)
    print("Current String: " + CurrentString)

    ser.write(CurrentString.encode())
    time.sleep(Delay)

def SetOutputVoltageAndCurrent(Voltage, Current):

    VoltageString = "VSET1:" + str(Voltage)
    CurrentString = "ISET1:" + str(Current)
    
    ser.write(VoltageString.encode())
    time.sleep(Delay)
    ser.write(CurrentString.encode())
    time.sleep(Delay)
def SwitchOutputOn():

    ser.write("OUT1".encode())  # Not too sure how this would work with multiple channels
    time.sleep(Delay)

def SwitchOutputOff():

    ser.write("OUT0".encode())  # Not too sure how this would work with multiple channels
    time.sleep(Delay)

def SwitchOVPOn():

    ser.write("OVP1".encode())
    time.sleep(Delay)

def SwitchOVPOff():

    ser.write("OVP0".encode())
    time.sleep(Delay)


def SwitchOCPOn():

    ser.write("OCP1".encode())
    time.sleep(Delay)

def SwitchOCPOff():

    ser.write("OCP0".encode())
    time.sleep(Delay)

def SwitchProtectionsOn():

    ser.write("OVP1".encode())
    time.sleep(0.00001)# Need to figure out the timing for this, without sleep both protections do not switch on
    ser.write("OCP1".encode())
    time.sleep(0.00001)

'''
Queries
'''

def GetVoltage():

    ser.write("VOUT1?".encode())
    print(ser.readline().decode())

def GetCurrent():
    # Current reading is extremely inaccurate, would not use
    ser.write("IOUT1?".encode())
    time.sleep(Delay)
    print(ser.readline().decode())

def Status():

    ser.write("STATUS?".encode())
    print(ser.readline())
    # Needs work, returns a binary value?

def ConnectToPSU(): # Wrapper for connection to PSU

    COMPOrt = ListCOMPorts
    ConnectToCOMPort(COMPOrt)

'''
Standard boilerplate code
Maybe have a function with the list COMPort and connection to do it in 1 func
'''
if __name__ == "__main__":

    COMPort = ListCOMPorts()
    print("Power Supply is connected to " + COMPort)
    ConnectToCOMPort(COMPort)

    SwitchProtectionsOn()   # Switch on protections if they aren't on already
    '''
    Tests of Queries and Commands
    '''
    SetOutputVoltageAndCurrent(5,1)

    SwitchOutputOn()

    GetVoltage()

    print("End")