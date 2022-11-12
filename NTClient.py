import sys
import time
from networktables import NetworkTable, NetworkTableEntry, NetworkTables, Value

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

ip = sys.argv[1]

NetworkTables.initialize(server=ip)




def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

def valueChanged(table: NetworkTable, key: str, entry: NetworkTableEntry, value: Value, isNew: int):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    return 0
sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(valueChanged)

i = 0
while True:
    print("robotTime:", sd.getNumber("robotTime", -1))

    sd.putNumber("dsTime", i)
    time.sleep(1)
    i += 1
    print('################################')
