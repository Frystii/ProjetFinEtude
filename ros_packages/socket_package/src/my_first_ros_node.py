#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import socket

# paramètres de la socket
HOST = "0.0.0.0"
PORT = 5000

def main():
    rospy.init_node("speech_recognition_server", anonymous=True)
    pub_go_to = rospy.Publisher("/go_to_position", String, queue_size=10)
    pub_save = rospy.Publisher("/save_position", String, queue_size=10)

    # initialisation de la socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    rospy.loginfo("ecoute sur le port 5000")
    
    conn, addr = server_socket.accept()

    try:
        while not rospy.is_shutdown():
            data = conn.recv(1024).decode("utf-8")
            
            if data:
                words = data.split(" ")
                # si la phrase contient save alors on publie sur le topic /save_position
                if words[0] == "save":
                    pub_save.publish(words[1])
                # si la phrase contient go to alors on publie sur le topic /go_to_position
                elif words[0] == "go" and words[1] == "to":
                    pub_go_to.publish(words[2])
                rospy.loginfo(data)
    except Exception as e:
        pass
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
