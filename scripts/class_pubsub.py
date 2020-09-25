#!/usr/bin/python

import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from rospy.numpy_msg import numpy_msg 

class LIDAR_RYCSV:
    
    def __init__(self):

        self.nameTopicSub = "/scan"
        self.nameTopicPub = "/scan_fixed"
        self.newMsg = LaserScan() # LaserScan msg

        # Subscribers
        rospy.Subscriber(self.nameTopicSub, numpy_msg(LaserScan), self.Lidar_Callback, queue_size=10 )

        # Publisher
        self.pub = rospy.Publisher(self.nameTopicPub, numpy_msg(LaserScan), queue_size=10)

        # Polling con callback
        rate = rospy.Rate(20) # 20 Hz
        rospy.loginfo(type(np.array([1,1])))
        while (not rospy.is_shutdown()):

            self.pub.publish(self.newMsg)
            rate.sleep()

    #--------------------------------------------------------------------------------------#
    # Callback o interrupcion
    def Lidar_Callback(self, lidar_scan):
        
        new_msgLaserScan = lidar_scan
        new_msgRanges    = lidar_scan.ranges.copy()

        #new_msgLaserScan.ranges > 10 m   == 0
        #new_msgLaserScan.ranges < 0.5 m  == 0

        #rospy.loginfo(new_msgRanges.shape)
        for i in range(new_msgRanges.shape[0]):
            if new_msgRanges[i]>10 or new_msgRanges[i]<0.5:
                new_msgRanges[i]=0


        #new_msgRanges = np.array([0 if (new_msgRanges[i]>10 or new_msgRanges[i]<0.5) else new_msgRanges[i] for i in range(new_msgRanges.shape[0])])
        #new_msgRanges = np.array([0 if (i>10 or i<0.5) else i for i in new_msgRanges],dtype=np.float)
        new_msgLaserScan.ranges = new_msgRanges
        self.newMsg = new_msgLaserScan