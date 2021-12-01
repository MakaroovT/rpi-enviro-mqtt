import paho.mqtt.client as mqttClient
import time
import datetime
import os

# 要连接的服务器与端口号
broker_address = "10.10.10.15"  # Broker address
port = 1883  # Broker port
# 要订阅的主题
subscribe = "nissin/env-data"
# 打印还是保存,打印哪种数据
save2file = True
jsonorhex = True


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:
        print("Connection failed")


def on_message(client, userdata, message):
    if save2file:
        today = datetime.date.today()  # Get OS time
        year = today.year  # Get year to built folder
        folder_path = "C:/" + str(year) + "/"  # Set folder path
        if not os.path.exists(folder_path):  # Determine whether the folder exists, if it does not exist create it
            os.makedirs(folder_path)
        with open(folder_path + format(today) + '.txt', 'a', encoding='UTF-8') as f:
            if jsonorhex:
                f.write(str(message.payload,
                                                                 encoding='utf-8') + "\n")
            else:
                f.write(message.payload.hex().upper() + "\n")
            f.close()  # close data
            print('データをファイルに保存しました')
            time.sleep(5)
    else:
        if jsonorhex:
            print(str(message.payload,
                                                           encoding='utf-8') + "\n\n")
        else:
            print(message.payload.hex().upper() + "\n\n")


Connected = False  # global variable for the state of the connection

client = mqttClient.Client("clientid1")  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(broker_address, port, 5)  # connect
client.subscribe(subscribe)  # subscribe
client.loop_forever()  # then keep listening forever
