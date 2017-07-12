import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester


class Memblock_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)


    def data_types(self):
        self.proc.expect(["ENABLED", pexpect.TIMEOUT, pexpect.EOF], timeout=10)
        
        test = []
        a_o, a_i, d_o, d_i, s_i, s_o, i_i, i_o = {}, {}, {}, {}, {}, {}, {}, {}

        for i in range(1,513):
            a_o[i] = PV('analog_out_'+str(i))
            a_i[i] = PV('analog_in_' + str(i))
            d_i[i] = PV('digital_in_' + str(i))
            d_o[i] = PV('digital_out_' + str(i))
            s_i[i] = PV('string_in_' + str(i))
            s_o[i] = PV('string_out_' + str(i))
            i_i[i] = PV('int_in_' + str(i))
            i_o[i] = PV('int_out_' + str(i))


        for x in range(1,513):
            test.append(util.put_check(a_o[x], x))

        for x in range(1,513):
            test.append(util.put_check(d_o[x], 1))

        for x in range(1,513):
            test.append(util.put_check(i_o[x], x))

        for x in range(1,513): 

            test.append(util.put_check(s_o[x], str(x)))

        for x in range(1,513):
            test.append(util.pv_check(a_i[x], 0))

        for x in range(1,513):
            test.append(util.pv_check(d_i[x], 0))

        for x in range(1,513):
            test.append(util.pv_check(i_i[x], 0))

        for x in range(1,513):
            test.append(util.pv_check(s_i[x], ''))

        if all(x == True for x in test):
            return True
        else:
            return False


        