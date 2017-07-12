import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random


class Pump_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
    
    def turn_on(self):
        command = PV('c_p0_command')
        state = PV('r_p0_state')
        c_on_off = PV('c_p0_on_off')
        r_on_off = PV('r_p0_on_off')
        c_normal = PV('c_p0_normal')
        c_faulted = PV('c_p0_faulted')
        c_freq = PV('c_p0_freq')

        if state.get() != 0.0:
            util.put_check(c_on_off, 0)

        util.put_check(c_on_off, 1)
        util.put_check(c_normal, 1)
        util.put_check(c_faulted, 0)
        util.put_check(c_freq, 490)
        return state.get()

    def turn_off(self):
        command = PV('c_p0_command')
        state = PV('r_p0_state')
        c_on_off = PV('c_p0_on_off')
        r_on_off = PV('r_p0_on_off')
        c_normal = PV('c_p0_normal')
        c_faulted = PV('c_p0_faulted')
        c_freq = PV('c_p0_freq')

        util.put_check(c_normal, 0)
        util.put_check(c_faulted, 0)
        util.put_check(c_freq, 1)
        print state.get()
        if state.get() in (0.0, 3.0, 5.0):
            util.put_check(c_on_off, 1)
        util.put_check(c_on_off, 0)

        return state.get()

    def state(self):
        command = PV('c_p0_command')
        state = PV('r_p0_state')
        c_on_off = PV('c_p0_on_off')
        r_on_off = PV('r_p0_on_off')
        c_normal = PV('c_p0_normal')
        c_faulted = PV('c_p0_faulted')
        c_freq = PV('c_p0_freq')

        util.put_check(c_on_off, 0)
        util.put_check(c_normal, 0)
        util.put_check(c_faulted, 0)
        util.put_check(c_freq, 490)
        return state.get()