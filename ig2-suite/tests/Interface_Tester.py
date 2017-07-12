import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester


class Interface_Tester(Tester):

    def __init__(self, path, test_name):
        
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)


    def channel_name_propagation(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'started'], timeout=5)

        test1 = PV('name1')
        test2 = PV('name2')
        test3 = PV('name3')

        return [test1.pvname == test1.value, test2.pvname == test2.value, test3.pvname == test3.value]

    def disconnected_devices(self):
        devices = {'loop1': 0, 'loop2': 0, 'loop3': 0, 'loop4': 0}
        for x in devices.keys():
            connect = self.proc.expect(
                ['Error: could not connect to.*', pexpect.TIMEOUT, pexpect.EOF], timeout=15)
            print self.proc.before
            print self.proc.after
                
            if connect == 0:
                last = self.proc.after.rsplit(None, 1)[-1]
                print last
                if last in devices.keys():
                    devices[last] = 1

        return devices

    def epics_version(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'EPICS ENVIRONMENT 2_6_7 ENABLED'], timeout=5)
        return self.proc.after
