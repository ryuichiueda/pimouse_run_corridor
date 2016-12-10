#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from std_msgs.msg import UInt16

class WallStopTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/wall_stop',nodes, "node does not exist")

    def set_sensor_values(self,lf,ls,rs,rf):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("%d %d %d %d\n" % (lf,ls,rs,rf))

    def get_freqs(self):
        with open("/dev/rtmotor_raw_l0","r") as lf,\
             open("/dev/rtmotor_raw_r0","r") as rf,
            left = int(lf.readline().strip())
            right = int(lf.readline().strip())

        return left,right

    def test_io(self):
        set_sensor_values(400,0,100,0)
        time.sleep(0.1)
        left, right = get_freqs()
        self.assertTrue(left == 0 and right == 0,"can't stop")

        set_sensor_values(400,0,0,99)
        time.sleep(0.1)
        left, right = get_freqs()
        self.assertTrue(left != 0 and right != 0,"can't move again")

if __name__ == '__main__':
    rospy.init_node('travis_test_wall_stop')
    rostest.rosrun('pimouse_run_corridor','travis_test_wall_stop',WallStopTest)
