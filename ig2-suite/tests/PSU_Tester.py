import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random
import itertools

class PSU_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
        print self.path
        

    def set_command_voltage(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        print self.proc.after
        print self.proc.before
        if connect == 2:

            command_v = PV('c_psu_control_voltage')
            value = random.random()*1000
            command_v.put(value)
            poll(evt=1.0, iot=1.0)
            command = command_v.get()
            print command_v.info
            print command
            print command_v.get()
            #teardown
            #command_v.disconnect()
            #util.blowout_pvs()
            # epics.ca.clear_channel(command_v.chid)
            # ctx = epics.ca.current_context()
            # pvs = []
            # for x in epics.ca._cache[ctx]:
            #     pvs.append(x)
            # for pv in pvs:
            # import itertools
# for element in itertools.product(*somelists):
#     print(element)    epics.ca._cache[ctx].pop(pv)
            #print epics.ca._cache[ctx]
            #epics.ca._cache[ctx].pop('c_psu_control_voltage')

            return command, value
        else:
            return -1

    def set_command_current(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect == 2:

            command_i = PV('c_psu_control_current')
            value = random.random()
            command_i.put(value)
            poll(evt=1.0, iot=1.0)

            return command_i.get(), value
        else:
            return -1

    def get_voltage_readback(self):

        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect == 2:

            
            #enable = PV('c_psu_enable')
            #resistance = PV('c_psu_resistance')
            readback_current = PV('r_psu_current')
            readback_voltage = PV('r_psu_voltage')
        
            # setpoint_current = PV('analog_in_current_setpoint')
            # setpoint_voltage = PV('analog_in_voltage_setpoint')
            command_v = PV('c_psu_control_voltage')
            poll(evt=1.0, iot=1.0)
            command_v.put(400)
            
            poll(evt=1.0, iot=1.0)
            change = self.proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)

            r_curr = readback_current.get()
            r_volt = readback_voltage.get()
            # set_curr = setpoint_current.get()
            # set_volt = setpoint_voltage.get()

            return r_volt
        else:
            return -1

    def get_current_readback(self):

        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect == 2:

            
            #enable = PV('c_psu_enable')
            resistance = PV('c_psu_resistance')
            readback_current = PV('r_psu_current')
            readback_voltage = PV('r_psu_voltage')
        
            # setpoint_current = PV('analog_in_current_setpoint')
            # setpoint_voltage = PV('analog_in_voltage_setpoint')
            command_v = PV('c_psu_control_voltage')
            poll(evt=1.0, iot=1.0)
            command_v.put(400)
            
            poll(evt=1.0, iot=1.0)
            change = self.proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)

        
            r_curr = readback_current.get()
            r_volt = readback_voltage.get()
            target = 400/resistance.get()
            # set_curr = setpoint_current.get()
            # set_volt = setpoint_voltage.get()

            return r_curr, target
        else:
            return -1

    def get_high_voltage_readbacks(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect != 2:
            return -1
        channels = [PV('r_psu_pwm_demand'), PV('r_psu_fault'), PV('r_psu_fault_message'), PV('r_psu_acc_output'),
            PV('r_psu_temperature'), PV('r_mux_1'), PV('r_mux_2'), PV('r_mux_3'), PV('r_mux_4')]
        data = []
        data = list(map(lambda x: x.get()!=None, channels))
        print data
        return data

    def enable(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect != 2:
            return -1
        
        command_enable = PV('c_psu_enable')
        readback_enable = PV('r_psu_enable')

        command_enable.put(0)
        poll(evt=0.1, iot=0.1)
        disabled = command_enable.get()

        command_enable.put(1)

        poll(evt=0.1, iot=0.1)

        return disabled, readback_enable.get()


    def disable(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect != 2:
            return -1
        
        command_enable = PV('c_psu_enable')
        readback_enable = PV('r_psu_enable')

        if readback_enable.get() != 1:
            command_enable.put(1)
        poll(evt=0.1, iot=0.1)
        enabled = readback_enable.get()
        command_enable.put(0)

        poll(evt=0.1, iot=0.1)

        return enabled, readback_enable.get()
        
    def clear_error(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect != 2:
            return -1

        command_enable = PV('c_psu_enable')
        readback_enable = PV('r_psu_enable')
        fault_message = PV('r_psu_fault_message')
        mux_1 = PV('c_mux_1')
        mux_1.put(1)
        #get psu into fault state
        error = fault_message.get()
        command_enable.put(0)
        poll(evt=0.1, iot=0.1)
        command_enable.put(1)
        poll(evt=0.1, iot=0.1)

        return fault.get(), error

    def fault_codes(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect != 2:
            return -1

        cmux_0, cmux_1, cmux_2, cmux_3 = PV('c_mux_0'), PV('c_mux_1'), PV('c_mux_2'), PV('c_mux_3')
        fault_message = PV('r_psu_fault_message')

        faults = []
        perms = itertools.product([0,1], repeat=4)
        for i,j,k,c in list(perms):
            #print i,j,k,c
            cmux_0.put(i)
            poll(evt=0.1, iot=0.1)
            cmux_1.put(j)
            poll(evt=0.1, iot=0.1)
            cmux_2.put(k)
            poll(evt=0.1, iot=0.1)
            cmux_3.put(c)
            poll(evt=0.1, iot=0.1)
            faults.append(fault_message.get())
            #print cmux_1.get(), cmux_2.get(), cmux_3.get(), cmux_4.get()

        return faults