# MQTT package downlode - paho-mqtt
# sudo pip install paho-mqtt 
## 동시에 publish(데이터[출판]) / subscribe(데이터 수신[구독]) 처리:

from threading import Thread, Timer
import time     # time.sleep()
import json
import datetime as dt

import paho.mqtt.client as mqtt
# DHT11 온습도 센서
import Adafruit_DHT as dht
#GPIO
import RPi.GPIO as GPIO

# GPIO, DHT 설정
sensor = dht.DHT11
rcv_pin = 10
green = 22
servo_pin = 18

GPIO.setwarnings(False) # 오류메시지 제거
# green led init
GPIO.setmode(GPIO.BCM)
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, GPIO.HIGH)   # = True
# servo init
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3)    # 각도 0도 DutyCycle 3 ~ 20

# 내가 데이터를 보내는 객체
class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)       # 스레드 초기화
        self.host = '210.119.12.74' # 본인 pc ip
        self.port = 1883            # 회사에서는 안씀
        self.clientId = 'IOT74'
        self.count = 0
        print('publisher 스레드 시작')
        self.client = mqtt.Client(clent_id = self.clientId)  # 설계대로

    def run(self):
        self.client.connect(self.host, self.port)
        #self.client.username_pw_set()   # id/pwd로 로그인할때 필요
        self.publish_data_auto()
    
    def publish_data_auto(self):
        humid, temp = dht.read_retry(sensor, rcv_pin)
        curr = dt.datetime.now().strftime('%T-%m-%d %H:%M:%S')      # 2023-0-14 10:30:15
        origin_data = { 'DEV_ID' : self.clientId,       #self. -> 멤버변수
                        'CURR_DT' : curr,               # 지역변수
                        'TYPE' : 'TEMPHUMID',
                        'STAT' : f'{temp}|{humid}'}     # real data
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='pknu/rpi/control/', payload=pub_data)
        print(f'Data published #{self.count}')
        self.count += 1
        Timer(2.0, self.publish_data_auto).start()  # 2초마다 출판

# 다른곳 데이터 받아오는 객체
class subscriber(Thread):
    def __init__(self):
         Thread.__init__(self)
         self.host = '210.119.12.74'    # Broker IP
         #self.host = 'https://'
         self.port = 1883
         self.clientId = 'IOT74_SUB'
         self.topic = 'SYS/monitor/control/'
         print('subscriber 스레드 시작')
         self.client = mqtt.Client(client_id=self.clientId)

    def run(self):     # Thread.start() 함수를 실행하면 실행되는 함수
        self.client.on_connect = self.onConnect     # 접속 성공 시그널 처리
        self.client.on_message = self.onMessage     # 접속 후 메시지 수신되면 처리
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic=self.topic)
        self.client.loop_forever()

    def onConnect(self, mqttc, obj, flags, rc):
         print(f'subscriber 연결됨 rc > {rc}')

    def onMessage(self, mqtt, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}')
        data = json.loads(rcv_msg)  # json data로 형변환
        stat = data['STAT']
        print(f'현재 STAT : {stat}')
        if (stat == 'OPEN'):
            GPIO.output(green, GPIO.LOW)
            pwm.ChangeDutyCycle(12) # 90도
        elif (stat == 'CLOSE'):
            GPIO.output(green, GPIO.HIGH)
            pwm.ChangeDutyCycle(3) # 90도

        time.sleep(1.0)

if __name__ == '__main__':
    thPub = publisher()     # publisher 객체 생성
    tbSub = subscriber()    # subscriber 객체 생성
    thPub.start()           #run() 자동실행
    thPub.start()

