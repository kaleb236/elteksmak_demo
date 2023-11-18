import os
import sys
import json
import rclpy

from ament_index_python.packages import get_package_share_directory

from rclpy.node import Node

from geometry_msgs.msg import PoseStamped

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from PyQt5.QtCore import QThread, pyqtSignal

class PoseSubscriber(QThread):
    pos = pyqtSignal(PoseStamped)

    def run(self):
        rclpy.init()
        node = Node('pose_subscriber')
        sub = node.create_subscription(PoseStamped, 'current_pose', self.sub_callback, 10)
        sub
        rclpy.spin(node)

    def sub_callback(self, pose):
        self.pos.emit(pose)

class SaveWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.pose_sub = PoseSubscriber()
        self.pose_sub.pos.connect(self.pose_callback)
        self.pose_sub.start()
        self.current_pose = PoseStamped()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Save pose')
        self.setGeometry(100,100,400,200)

        layout = QVBoxLayout()

        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)

        self.save_button = QPushButton('Save', self)
        layout.addWidget(self.save_button)

        self.label = QLabel()
        self.label.setMaximumHeight(16)
        layout.addWidget(self.label)

        self.save_button.clicked.connect(self.on_clicked)

        self.setLayout(layout)
    
    def on_clicked(self):
        input_text = self.line_edit.text()
        self.label.setText(input_text)
        self.save_pose(f'Station{input_text}')
        # print(input_text)

    
    def save_pose(self, station_name):
        pose = self.current_pose.pose
        # station_path = get_package_share_directory('elteksmak_demo')
        station_path = '/home/ovali/new_ws/src/elteksmak_demo'
        f = open(os.path.join(station_path, 'data', 'stations.json'))
        data = json.load(f)
        f.close
        data[station_name] = {
            "position": {
                "x": pose.position.x,
                "y": pose.position.y,
                "z": pose.position.z
            },
            "orientation": {
                "w": pose.orientation.w,
                "x": pose.orientation.x,
                "y": pose.orientation.y,
                "z": pose.orientation.z
            }
        }
        with open(os.path.join(station_path, 'data', 'stations.json'), "w") as outfile:
            json.dump(data, outfile)

    
    def pose_callback(self, pose):
        self.current_pose = pose
        print(self.current_pose)

def main():
    app = QApplication(sys.argv)
    window = SaveWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()