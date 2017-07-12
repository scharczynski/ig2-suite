import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random


class Valve_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
    
    def open_valve(self):
        command = PV('c_v1_command')
        state = PV('r_v1_state')
        c_open_close = PV('c_v1_open_close')
        r_open_close = PV('r_v1_open_close')
        poll(evt=1.e-5, iot=0.01)
        if state.get() == 1.0:
            util.put_check(c_open_close, 0)

        #c_open_close.put(1)
        util.put_check(c_open_close, 1)
        poll(evt=1.e-5, iot=0.01)
        return state.get()
    
    def close_valve(self):
        command = PV('c_v1_command')
        state = PV('r_v1_state')
        c_open_close = PV('c_v1_open_close')
        r_open_close = PV('r_v1_open_close')
        if state.get() == 0:
            #c_open_close.put(1)
            util.put_check(c_open_close, 1)
        #c_open_close.put(0)
        util.put_check(c_open_close, 0)
        poll(evt=1.e-5, iot=0.01)
        return state.get()

    def get_state(self):
        state = PV('r_v1_state')
        c_open_close = PV('c_v1_open_close')
        return c_open_close.get(), state.get()