#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
 	
import psutil
import datetime

def getListOfProcessSortedBy(attribute = 'cpu_percent'):
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        cpu_percent = proc.cpu_percent(interval=0.1)
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid','cmdline', 'cpu_percent', 'name', 'username'])
            pinfo['vms'] = str(proc.memory_info().vms / (1024 * 1024 * 1024)) + ' GB'
            pinfo[attribute] = str(proc.cpu_percent(interval=0.1)) + '%' 
            # Append dict to list
            if cpu_percent > 1.0:
                listOfProcObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
 
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj[attribute], reverse=True)
 
    return listOfProcObjects
 
def getListOfProcess():
    
    print('*** Create a list of all running processes ***')
 
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
       # Get process detail as dictionary
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       # Append dict of process detail in list
       listOfProcessNames.append(pInfoDict)
 
    return listOfProcessNames
    # Iterate over the list of dictionary and print each elem
    # for elem in listOfProcessNames:
    #     print(elem)

def listProcNameID():
    print("*** Iterate over all running process and print process ID & Name ***")
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def writeFile(nFile = "proccess", txt = ""):
        f = open(nFile + ".txt","a+")
        f.write(txt)
        f.close()

def main():
    
    currentDT = datetime.datetime.now()
    nameFile = 'process_monitoring_' + currentDT.strftime("%Y-%m-%d")

    writeFile(nameFile, '*** Top process with highest cpu/memory usage ***\n')
    
    print('*** Top process with highest cpu/memory usage ***')
    listOfRunningProcess = getListOfProcessSortedBy('cpu_percent')

    for elem in listOfRunningProcess :
        print(elem)
        proc = str(elem) + "-" + "[" + currentDT.strftime("%Y-%m-%d %H:%M:%S") + "]" + "\n"
        print(proc)
        writeFile(nameFile, proc)
 
if __name__ == '__main__':
   main()