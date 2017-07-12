import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, camonitor
import time
import re
from util import epics_util as util
from tests.Tester import Tester


class Config_Tester(Tester):

    def __init__(self, path, test_name):
        Tester.__init__(self, path)
        self.path += str(test_name)
        print self.path
        self.proc = pexpect.spawn(self.path)

       

    def bad_defaults(self):
        
        self.proc.expect(['\[EXCEPTION[^:]*string', pexpect.EOF], timeout=5)
        error = self.proc.after
        return error

    def broken_xml(self):
        self.proc.expect('\[EXCEPTION] Error parsing XML file')
        found = self.proc.after
        return found

    def buffering_low(self):
        status = PV('status')
        if not util.check_device('C1', self.proc) and status.get() in range(0,3):
            print "device not connected"
            return False

        count3 = PV('in_counts_3')
        low_3 = PV('low_limit_3')
        low_4 = PV('low_limit_4')
        trig_buffer = PV('trig_buffer')
        init = PV('initiate')
        poll(evt=1.e-5, iot=0.01)
        data3 = []

        def getCount3(pvname, value, **kw):
            data3.append(value)

        if util.put_check(low_3, 0.0) and util.put_check(low_4, 0.0) and util.put_check(trig_buffer, 1000) and util.put_fuzzy('analog_out_period', 10e-5, 0.05):
            pass
        else:
            print "setting not taking place"
            return False, False

        count3.add_callback(getCount3)
        init.put(1)
        t0 = time.time()
        while time.time() - t0 < 3:

            poll(evt=1.e-5, iot=0.01)

        time.sleep(2)

        return len(data3)

    def buffering(self):
        status = PV('status')
        if not util.check_device('C1', self.proc) and status.get() in range(0,3):
            print "device not connected"
            return False
        count3 = PV('in_counts_3')
        count4 = PV('in_counts_4')
        low_3 = PV('low_limit_3')
        low_4 = PV('low_limit_4')
        trig_buffer = PV('trig_buffer')
        init = PV('initiate')
        poll(evt=1.e-5, iot=0.01)
        data3 = []
        data4 = []

        def getCount3(pvname, value, **kw):
            data3.append(value)

        def getCount4(pvname, value, **kw):
            data4.append(value)

        if util.put_check(low_3, 0.0) and util.put_check(low_4, 0.0) and util.put_check(trig_buffer, 1000) and util.put_fuzzy('analog_out_period', 10e-5, 0.05):
            pass
        else:
            print "setting not taking place"
            return False, False

        t0 = time.time()
        # while caget('trig_buffer')!=1000 and caget('trig_mode')!=1:
        #    if time.time() - t0 > 20:
        #        return "buffer or mode never set"
        #    else:
        #        pass

        #util.put_check('initiate', 1)
        time.sleep(1)
        count3.add_callback(getCount3)
        count4.add_callback(getCount4)
        init.put(1)

        while time.time() - t0 < 3:

            poll(evt=1.e-5, iot=0.01)

        # time.sleep(2)
        end = self.proc.expect(
            ['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)
        #print proc.before

        return len(data3), len(data4)


    def channel_limits(self):
        self.proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

        data1 = []
        data2 = []
        data3 = []

        test1 = PV('test1')
        test2 = PV('test2')
        test3 = PV('test3')
        poll(evt=1.e-5, iot=0.01)
        test1.put('-1')
        time.sleep(0.1)
        data1.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test1.put('6')
        time.sleep(0.1)
        data1.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test1.put('5')
        time.sleep(0.1)
        data1.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test2.put('-11')
        time.sleep(0.1)
        data2.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test2.put('-1')
        time.sleep(0.1)
        data2.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test2.put('-3')
        time.sleep(0.1)
        data2.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test3.put('10')
        time.sleep(0.1)
        data3.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test3.put('-10')
        time.sleep(0.1)
        data3.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

        test3.put('0')
        time.sleep(0.1)
        data3.append(self.proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=5))


        return [x+y+z for x,y,z in zip(data1, data2, data3)]

    def check(self, value1, value2, tolerance):
        mod_plus = value1 + value1*tolerance
        mod_minus = value1 - value1*tolerance

        return (mod_plus >= value2 or mod_minus <= value2)

    
    def channel_scaling(self):  
        status = PV('status')
        if not util.check_device('A1', self.proc) and status.get() in range(0,3):
            print "device not connected"
            print status.get()
            print util.check_device('A1', self.proc)
            return False
        normal = PV('cleanIn1')
        linear = PV('linearIn1')
        log = PV('logIn1')
        both_scaled = PV('bothScaled')
        init = PV('initiate')
        poll(evt=1.e-5, iot=0.01)

        init.put(1)
        poll(evt=1.e-5, iot=0.01)
        time.sleep(2)

        base = normal.get()
        lin = linear.get()
        logged = log.get()
        both = both_scaled.get()

        print base, lin, logged, both

        return (self.check( lin, base*2 + 10, 0.01) and self.check( logged, 10**base, 0.01) and self.check(both, 10 ** (base*2 +10), 0.01))



    def defaults(self):
        self.proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)
        a,b,c = caget('testA'), caget('testB'), caget('testC')
        return (a,b,c)

    def monitor_only(self):
        status = PV('status')
        if not util.check_device('C1', self.proc) and status.get() in range(0,3):
            print "device not connected"
            return False

        count3 = PV('in_counts_3')
        count4 = PV('in_counts_4')
        trig_mode = PV('trig_mode')
        low_3 = PV('low_limit_3')
        low_4 = PV('low_limit_4')
        trig_buffer = PV('trig_buffer')
        init = PV('initiate')
        poll(evt=1.e-5, iot=0.01)
        data3 = []
        data4 = []

        util.put_check(trig_mode, 1)
        util.put_check(low_3, 0.0)
        util.put_check(low_4, 0.0)
        util.put_check(trig_buffer, 1000)
        util.put_fuzzy('analog_out_period', 10e-5, 0.01)

        def getCount3(pvname, value, **kw):
            data3.append(value)

        def getCount4(pvname, value, **kw):
            data4.append(value)

        count3.add_callback(getCount3)
        count4.add_callback(getCount4)

        init.put(1)
        time.sleep(3)

        return len(data3), len(data4)

    def same_name(self):
        self.proc.expect('\[EXCEPTION[^:]*exists')

        error = self.proc.after
        before = self.proc.before
    
        #print " after "+ error

        expr = re.compile('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}')
        clean = re.sub(expr, '', error).lstrip()
        return clean

    def same_wire(self):
        self.proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=0.25)

        t1 = PV('wire1')
        t2 = PV('wire2')

        camonitor('wire1')
        camonitor('wire2')

        t1.put(65, wait=True)
        time.sleep(1)


        return(caget('wire1'), caget('wire2'))
