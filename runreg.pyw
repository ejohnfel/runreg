import os, sys, re
from winreg import *
import argparse

#
# Script to Add, modify or remove, HKCU\Software\Windows\CurrentVersion\Run Entries
#
# The intent was to be able to install the PuTTY agent as something executed from RUN
#

TestArgs = [ "add","PuTTY_Pageant",r"%userprofile%\Documents\Shortcuts\PuTTY Agent.lnk" ]

Keyname = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

def Exists(key,valuename):
    """Check if valuename Exists"""

    success = False
    
    try:
        value,key_type = QueryValueEx(key,valuename)
        success = True
    except:
        success = False

    return success

def ProcessEnv(item):
    """Expand any environment Variables In Provided String"""
    
    return os.path.expandvars(item)

def Add(key,valuename,value):
    """Add new Run Key"""

    if type(value) == list and len(value) > 0:
        value = value[0]
    elif type(value) == list and len(value) == 0:
        value = ""

    value = ProcessEnv(value)

    if value:
        if os.path.exists(value):
            success = Exists(key,valuename)

        if not success:
             breakpoint()
             SetValueEx(key,valuename,0,REG_SZ,value)
        else:
            print(f"Item to execute does not exist: {value}")
    else:
        print("No value (path) was supplied")

def Remove(key,valuename):
    """Remove Valuename Key"""

    success = Exists(key,valuename)
    
    if success:
        DeleteValue(key,valuename)

    return success

def Modify(key,valuename,values):
    """Modify Existing Valuename's value"""

    success = Exists(key,valuename)

    if type(value) == list and len(value) > 0:
        value = value[0]
    elif type(value) == list and len(value) == 0:
        value = ""

    if success:
        SetValueEx(key,valuename,0,REG_SZ,ProcessEnv(value))

    return success
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Modify HKCU Run Key")

    parser.add_argument("command",help="Command, add|remove")
    parser.add_argument("valuename",help="Entry name")
    parser.add_argument("value",nargs="*",help="When adding or modifying, the thing to be executed, in absolute path")

    args = parser.parse_args()

    with OpenKey(HKEY_CURRENT_USER,Keyname,access=KEY_ALL_ACCESS) as key:
        if args.command == "add":
            Add(key,args.valuename,args.value)
        elif args.command in [ "remove", "del", "rm" ]:
            Remove(key,args.valuename)
        elif args.command in [ "modify", "mod" ]:
            Modify(key,args.valuename,args.value)
        else:
            print(f"Did not understand the command, {args.command}")
