#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time, sys
from std_msgs.msg import UInt16
from std_srvs.srv import Trigger, TriggerResponse

class WallStopTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/wall_stop',nodes, "node does not exist")

    def set_sensor_values(self,lf,ls,rs,rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (rf,rs,ls,lf))

    def get_freqs(self):
        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf:
            left = int(lf.readline().rstrip())
            right = int(rf.readline().rstrip())
        return left,right

    def test_io(self):
        self.set_sensor_values(400,100,100,0)
        time.sleep(0.3)
        left, right = self.get_freqs()
        self.assertTrue(left == 0 and right == 0,"can't stop")

        self.set_sensor_values(400,0,0,99)
        time.sleep(0.3)
        left, right = self.get_freqs()
        self.assertTrue(left != 0 and right != 0,"can't move again")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_wall_stop')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_stop',WallStopTest)
