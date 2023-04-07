#!/usr/bin/env python
#Quick and Dirty Python Interface to Powershell from Python
#Requires pexpect module.  Try "pip install pexpect"
import pexpect
from pexpect.popen_spawn import PopenSpawn
import re
import time

class pxpowershell:
    def __init__(self, *args, **kwargs):
        self.cmd = "powershell.exe"
        self.unique_prompt = "XYZPYEXPECTZYX"
        self.orig_prompt = ""
        self.process = ""
    def __init__(self):
        self.cmd = "powershell.exe"
        self.unique_prompt = "XYZPYEXPECTZYX"
        self.orig_prompt = ""
        self.process = ""
    
    def start_process(self):
        self.process =  pexpect.popen_spawn.PopenSpawn(self.cmd)
        time.sleep(1)
        init_banner = self.process.read_nonblocking(4096, 2)
        try:
            prompt = re.findall(b'PS [A-Z]:', init_banner, re.MULTILINE)[0]
        except Exception as e:
            raise(Exception("Unable to determine powershell prompt. {0}".format(e)))
        
        self.process.sendline("Get-Content function:\prompt")
        self.process.expect(prompt)
        #The first 32 characters will be the command we sent in
        self.orig_prompt = self.process.before[32:]
        self.process.sendline('Function prompt{{"{0}"}}'.format(self.unique_prompt))
        self.process.expect(self.unique_prompt)
        self.process.expect(self.unique_prompt)
    def restore_prompt(self):
        self.process.sendline('Function prompt{{"{0}"}}'.format(self.orig_prompt))
    def run(self,pscommand):
        self.process.sendline(pscommand)
        self.process.expect(self.unique_prompt)
        return self.process.before[len(pscommand)+2:]
    def stop_process(self):
        self.process.kill(9)
'''
if __name__ == "__main__":
    #Quick demo
    x = pxpowershell()
    x.start_process()
    result = x.run("Connect-ExchangeOnline -CertificateThumbPrint 'DB86D49593A711E8E0320EDC22124688B4AE2D1C' -AppID '4cc74730-5cb1-4a55-9557-e3d0b1e793ab' -Organization 'thelastoneleft.us'")
    print(result.decode())
    result = x.run("Add-MailboxPermission -Identity 'AdeleV@0tkwt.onmicrosoft.com' -User 'testadmin@thelastoneleft.us' -AccessRights FullAccess -InheritanceType All")
    print(result.decode())
    x.stop_process()

'''
