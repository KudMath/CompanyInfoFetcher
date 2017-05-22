import behanceUsers
from datetime import datetime
import time

BehanceUsers = behanceUsers.BehanceUsers
print "Starting Benhance parsing", str(datetime.now())

behanceUsers = BehanceUsers()
var = raw_input("Do you want to force the update of old users: y/[n] ?\n")
if(var == "y"):
    behanceUsers.startingOrdinal=True

var2 = raw_input("Do you want to skip some users: y/[n] ?\n")
if(var2 == "y"):
    var3 = raw_input("How many?\n")
    behanceUsers.startingOrdinal=int(var3)

behanceUsers.beginContinuousFetch()
