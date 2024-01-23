#!/usr/bin/env python3

import rospy 
import tty, sys, termios
from std_msgs.msg import String 
import select

class TeleOperation:
    def __init__(self, node_name, topic_publish = 'keys', timeout = 2, verbose = False ):
        rospy.init_node(node_name)
        self.key_pub = rospy.Publisher(topic_publish, String, queue_size = 1)

        self.fileno = sys.stdin.fileno() 
        self.old_setting = termios.tcgetattr(self.fileno)

        tty.setraw(self.fileno)
        tty.setcbreak(self.fileno)

        self.timeout = timeout
        self.verbose = verbose
    
    def broadcast(self):
        while not rospy.is_shutdown():
            try:
                tty.setcbreak(self.fileno)
                if select.select([sys.stdin], [], [], self.timeout)[0]:
                    key = sys.stdin.read(1)
                    self.key_pub.publish(key)
                    if self.verbose:
                        print('[+] pressed {key}'.format(key=key))
            except Exception as e :
                print('[-] Error broadcasting key')
            finally:
                termios.tcsetattr(self.fileno, termios.TCSADRAIN, self.old_setting)
        print('[+] Closing Teleop')

if __name__ == "__main__":
    teleop = TeleOperation('key_teleop', verbose=True)
    teleop.broadcast()
