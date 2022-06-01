#
#SPA Group 181 - SPA Assignment 2
#This script generates the random customer data and sends it to kafka topic as pipe delimited string
#
#Importing libraries
import random
import sys
import math
from datetime import datetime
from kafka import KafkaProducer
import json
import time

#
#Assigning initial latitude and longitude values of shop
#
shop_latitude = 20.00
shop_longitude = 80.00

#
#User defined function to generate random customer data
#
def generate_random_data(lat, lon):
    customer = random.randint(1,300) #Randomly generate customer id between 1 and 300
    phone_number = random.randint(9000000000, 9999999999) #Randomly generate 10 digit phone number starts with 9
    #Generating nearby latitute and longitude values of shop
    dec_lat = lat+random.random()*3
    dec_lon = lon+random.random()*3
    curr_time = datetime.now() #Current date time generation
    dt_string = curr_time.strftime("%d/%m/%Y %H:%M:%S")
    #Concatenating all the variables in pipe delimted string variable
    str_output = str(customer)+'|'+str(phone_number)+'|'+str(dec_lat)+'|'+str(dec_lon)+'|'+dt_string
    return str_output

#Creating kafka producer object
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
while 1 == 1:
    #Sending customer messages to customer topic
    producer.send('customer',generate_random_data(shop_latitude, shop_longitude))
    time.sleep(10)
    producer.flush()