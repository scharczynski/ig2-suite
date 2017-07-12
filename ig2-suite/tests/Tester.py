import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util

class Tester(object):
    
    def __init__(self, path):
        self.path = path #path to i2g and config param upto the actual name
        #self.proc = ''
        #print self.path
        self.proc = pexpect.spawn(self.path)


    
    def kill_pexpect(self):
        self.proc.close(force=True)
        util.blowout_pvs()
    



