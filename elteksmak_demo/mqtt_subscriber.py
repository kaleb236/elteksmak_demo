import os
import json
import paho.mqtt.client as mqtt

import rclpy

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from .robot_navigator import BasicNavigator

rclpy.init()
navigator = BasicNavigator('mqtt_navigator')
navigator.waitUntilNav2Active()
SUBSCRIBED_TOPIC = 'nct/stations'
PUBLISH_TOPIC = 'nct/feedback'


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(SUBSCRIBED_TOPIC)

def on_message(client, userdata, msg):
    station = msg.payload.decode("ascii").split(':')[1]
    if station in get_stations():
        station_pose = get_stations()[station]
        print(station_pose)
        sent = send_goal(station_pose)
        if sent:
            client.publish(PUBLISH_TOPIC, 'Goal sent')

def get_stations():
    station_path = '/home/ovali/new_ws/src/elteksmak_demo'
    f = open(os.path.join(station_path, 'data', 'stations.json'))
    data = json.load(f)
    return data

def send_goal(pose):
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = pose["position"]["x"]
    goal_pose.pose.position.y = pose["position"]["y"]
    goal_pose.pose.position.z = pose["position"]["z"]
    goal_pose.pose.orientation.w = pose["orientation"]["w"]
    goal_pose.pose.orientation.x = pose["orientation"]["x"]
    goal_pose.pose.orientation.y = pose["orientation"]["y"]
    goal_pose.pose.orientation.z = pose["orientation"]["z"]
    succ = navigator.goToPose(goal_pose)
    return succ

def main():
    client = mqtt.Client("mqtt-test", transport="websockets") 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('broker.emqx.io', 8083)
    client.loop_forever() 

if __name__ == '__main__':
    main()
