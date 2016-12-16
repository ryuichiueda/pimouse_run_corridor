#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallStop():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback_sensors)
        self.sensors = LightSensorValues()

    def callback_sensors(self,messages):
        self.sensors = messages

    def decision(self,sensor_sum_all):
        linear = 0.0 if sensor_sum_all >= 500 else 0.2
        angular = 0.0
        return linear, angular

    def run(self):
        rate = rospy.Rate(10)
        d = Twist()
        while not rospy.is_shutdown():
            d.linear.x, d.angular.z = self.decision(self.sensors.sum_all)
            self.cmd_vel.publish(d)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('wall_trace')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')

    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    if not rospy.ServiceProxy('/motor_on',Trigger).call().success:
        rospy.logerr("motors are not empowered")
        sys.exit(1)

    WallStop().run()
