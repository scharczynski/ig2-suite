import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random

class HC80_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
        #self.connected = util.check_device('A1', self.proc) and self.status.get() in range(0,4)
        self.v1, self.v2, self.v3, self.v4 = PV('digital_in_v1'), PV('digital_in_v2'), PV('digital_in_v3'), PV('digital_in_v4')
        self.state = PV('r_helium_controller_state{serial}')
        self.mfc1, self.mfc2 = PV('r_helium_controller_mfc_purge:{serial}'), PV('r_helium_controller_mfc_maintain:{serial}')
        self.enable = PV('c_helium_controller_enable:{serial}')
        self.vent = PV("c_helium_controller_button_vent:{serial}")
        self.operate = PV("c_helium_controller_button_operate:{serial}")
        self.sleep = PV('c_helium_controller_button_sleep:{serial}')
        self.o2_percent = PV("r_helium_controller_oxygen_percent:{serial}")
        self.o2_threshold = PV("c_helium_controller_oxygen_percent_threshold:{serial}")
        
    def get_state_pvs(self):


        return [self.v1.get(), self.v2.get(), self.v3.get(), self.v4.get(), self.mfc1.get(), self.mfc2.get()]

    #enter safe state and check that configuration is right
    def safe_state(self):
        if not self.connected:
            return -1

        
        #cycle device to put it in init, which is a safe state
        self.enable.put(0)
        self.enable.put(1)
    
        if state.get(): #is safe state
            return self.get_state_pvs()
        else:
            print "not in safe state"
            return False

    #enter vent state and check that is in safe state
    def vent_state(self):
        if not self.connected:
            return -1
        
        self.vent.put(1)
        time.sleep(0.5)
        if self.state.get(): #is vent state
            return self.get_state_pvs()
        else:
            return False
    
    #enter flush state and verify it flushes and config is right
    def flush_state(self):
        if not self.connected:
            return -1
        

        self.operate.put(1)
        if self.state.get(): #is flush state of operate
            return self.get_state_pvs()
        else:
            return False

    #enter maintainence state and verify correct
    def maintainence_state(self):
        if not self.connected:
            return -1

        self.operate.put(1)

        while in flush state and time not exceed:
            return self.get_state_pvs()
        return False 

    #enter hibernate state and verify correct
    def hibernate_state(self):
        if not self.connected:
            return -1
        
        
        self.sleep.put(1)

        if self.state.get(): #is hibernate of sleep
            return self.get_state_pvs()
        else:
            return False
    #enter init state and verify correct
    def initialize_state(self):
        if not self.connected:
            return -1

        self.enable.put(0)
        self.enable.put(1)
        if self.state.get(): #is init
            return self.get_state_pvs()
        else:
            return False
    
    #enter operate state and verify correct
    def operate_state(self):
        if not self.connected:
            return -1

        self.operate.put(1)


    #from init state verify correct transition to vent
    def init_to_vent(self):
        if not self.connected:
            return -1

        wait = PV("c_helium_controller_init_wait_time:{serial}")

        wait_time = wait.get()
        self.enable.put(0)
        self.enable.put(1)

        if self.state.get() not in init:
            return False
        while time.time - t0 < wait_time:
            pass
        return self.state.get() in vent
            


    #from init state verify correct transition to operate
    def init_to_operate(self):
        if not self.connected:
            return -1
        #set some thresholds that are easily reached during init
        self.enable.put(0)
        self.enable.put(1)
        t0 = time.time()
        if self.state.get() not in init:
            return False
        while time.time() - t0 < wait_time:
            pass
        return self.state.get() in operate
            
    #from operate_flush verify correct transition to operate_maintainence
    def flush_to_maintainence(self):
        if not self.connected:
            return -1
        self.operate.put(1)
        t0 = time.time()
        if self.state.get() not in operate_flush:
            return False
        while self.state.get() in operate_flush:
            if self.o2_percent < self.o2_threshold:
                print 'should be exiting'
        return self.state.get() in maintainence   
    
    #from sleep_hibernate verify correct transition to sleep_maintainence
    def hibernate_to_maintainence(self):
        if not self.connected:
            return -1
        self.operate.put(1)
        while self.state.get() not in maintainence:
            pass
        
        self.sleep.put(1)
        if self.state.get() not in sleep_hibernate:
            return False
        while self.state.get() in sleep_hibernate:
            if self.o2_percent > self.o2_threshold:
                print "should be entering maint"
        return self.state.get() in maintaincence
        
    #---interlock type tests

    #exceed chamber pressure verify interlock tripped
    def exceed_pressure(self):
    
    #chamber pressure too low verify interlock tripped
    def under_pressure(self):
    
    #oxygen lvl too high verify interlock tripped
    def oxygen_exceed(self):

    
    def remote_dc(self):
         
    #helium pressure too high or low, verify interlock trips
    def supply_bad(self):
    
    #try to get bad mfc readback, verify interlock trips
    def mfc_bad_readback(self):
        
        
    #----software tests



        

        