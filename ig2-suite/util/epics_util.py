from epics import caget, caput, poll, PV, ca
import time
import pexpect


def pv_check(pv, value):
    poll(evt=1.e-5, iot=0.01)
    # if pvname.get() is None:
    #     pv = PV(pvname)
    # else:
    #     pv = pvname

    if isclose(pv.get(), value):
        print "value is correct: " + str(pv.get())
        return True
    else:
        t0 = time.time()
        pv.put(value)
        poll(evt=1.e-5, iot=0.01)
        while not isclose(pv.get(), value):
            poll(evt=1.e-5, iot=0.01)
            current = pv.get()
            if time.time() - t0 > 10:
                #raise ValueError("setting " + pvname + " timed out, set value was " + str(value) + " actual value was: " + str(caget(pvname)))
                print ("setting " + pv.pvname + " timed out, set value was " + str(value) + " actual value was: " + str(current))
                return False
            else:
                pass
        print "value is " + str(pv.get())
        return True

def caput_check(name, value):
    t0 = time.time()
    
    while caget(name) != value:
        caput(name, value)
        poll(evt=1.e-5, iot=0.01)
        if time.time() - t0 > 10:
            print "did not set"
            return False
    return True

def put_check(pv, value):
    # if pvname.get() is None:
    #     pv = PV(pvname)
    # else:
    #     pv = pvname

    pv.put(value)
    poll(evt=0.5, iot=0.25)
    return pv_check(pv, value)

def check_fuzzy(pvname, value, envelope):
    pv_value = caget(pvname)
    under  = -1*value*envelope + value
    over = value*envelope + value

    t0 = time.time()
    while pv_value < under or pv_value > over:
        if time.time() - t0 > 10:
            raise ValueError("setting " + pvname + " timed out, value was " + str(value))
            return False
        else:
            if pv_value >= under or pv_value <= over:
                return True
    return True

def put_fuzzy(pvname, value, envelope):
    caput(pvname, value)
    return check_fuzzy(pvname, value, envelope)

def check_device(device_name, proc):
    connect = proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success: '+str(device_name)], timeout=15)
    
    if connect == 2:
        return True
    else:
        print proc.after
        print proc.before
        return False
        
        
def blowout_pvs():
    #epics.ca.clear_channel(pv_name.chid) 
    ca.finalize_libca()
    # ctx = ca.current_context()
    # pvs = []
    # for x in ca._cache[ctx]:
    #     pvs.append(x)
    # for pv in pvs:
    #     ca._cache[ctx].pop(pv)


def isclose(a, b, rel_tol=1e-05, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)