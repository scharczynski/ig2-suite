import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random


class Gauge_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)

    def get_state(self):
        
        #print str(util.isclose(1.79999995232, 1.8))

        state = PV('r_g0_state')
        outp = PV('g0_pressure')
        #outp.wait_for_connection()
        #print outp.get()
        util.put_check(outp, 1.8)
        print outp.get()
        return state.get()