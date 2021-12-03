import logging
import paho.mqtt.client as mqtt
import time
import datetime
import os


broker_address = "10.10.10.15"  
port = 1883  
subscribe = "nissin/env-data"
save2file = True
jsonorhex = True


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  
        Connected = True  

    else:
        print("Connection failed")


def on_message(client, userdata, message):
    if save2file:
        try:
            today = datetime.date.today()  
            year = today.year  
            folder_path = "C:/" + str(year) + "/"  
            if not os.path.exists(folder_path):  
                os.makedirs(folder_path)
            with open(folder_path + format(today) + '.txt', 'a', encoding='UTF-8') as f:
                if jsonorhex:
                    f.write(str(message.payload,
                                encoding='utf-8') + "\n")
                else:
                    f.write(message.payload.hex().upper() + "\n")
                f.close()
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'データをファイルに保存しました')  
        except Exception as e:
            logging.error('Caught exception error: ' + str(e))
    else:
            if jsonorhex:
                print(str(message.payload,
                          encoding='utf-8') + "\n\n")
            else:
                print(message.payload.hex().upper() + "\n\n")
    
    time.sleep(5)


Connected = False  
client = mqtt.Client()  
client.on_connect = on_connect 
client.on_message = on_message  
client.connect(broker_address, port, 5) 
client.subscribe(subscribe)  
client.loop_forever()  
