from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
from util import epics_util as util

class M10_tests:
    results = []

    def __init__(self):
        self.results = []

    def test_io():
        proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_io.xml")
        proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

        d_i = []
        a_i = []
        d_o = []
        a_o = []


        for i in range(0,4):
            d_o.append(util.put_check('digitalOut' + str(i+1), 1))
            d_i.append(util.pv_check('digitalIn'+ str(i+1), 1))
            

        for i in range(0,2):
            a_o.append(util.put_check('analogOut' + str(i+1), i))
            a_i.append(caget('analogIn'+ str(i+1)) != None)

    
        return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]


    def test_stopcount():
        proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_stopcount.xml")
        proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=10)
        print proc.after

        #util.pv_check('status', 0)
        
        stop = 1001
        data1 = []
        data2 = []

        def getData1(pvname, value, **kw):
            if value != 0:
                data1.append(value)

        def getData2(pvname, value, **kw):
            if value != 0:
                data2.append(value)

        analog1 = PV('analogIn1')
        stop_count = PV('outStopCount')
        init = PV('initiate')
        analog2 = PV('analogIn2')

        analog1.wait_for_connection()
        analog2.wait_for_connection()
        init.wait_for_connection()
        stop_count.wait_for_connection()

        analog1.add_callback(getData1)
        

        

        
        if util.put_check('outStopCount', stop):
            init.put(1)
            t0 = time.time()
            while time.time() -t0 < 30:           
                poll(evt=1.e-5, iot=0.01)
        else:
            print "Stopcount not set"
            return False

        buffered_run = len(data1)
        analog2.add_callback(getData2)

        time.sleep(2)
        if util.put_check('outStopCount', -1):
            init.put(1)
            t0 = time.time()
            while time.time() -t0 < 30:           
                poll(evt=1.e-5, iot=0.01)
        else:
            print "Stopcount not set 2nd time"
            return False

        unbuffered_run = len(data2)

        return buffered_run, unbuffered_run



