#
#SPA Group 181 - SPA Assignment 2
#This script recieves processed data from the kafka topic by using kafka consumer
#and send SMS based on the business logic
#
#Importing libraries
import pandas as pd
from kafka import KafkaConsumer
KAFKA_OUTPUT_TOPIC_NAME_CONS = "outcustomer"
KAFKA_BOOTSTRAP_SERVERS_CONS = "localhost:9092"

#UDF is created to send sms to the customer's phone number based on the flag derived after processing the data
def business_logic(flag,phone_number):
    if flag == 'low_income_low_spend':
        print("Phone_Number: "+phone_number+" - Hello Customer!! Buy a Pizza today and get 2 free coupons worth of Rs.99 each. Promo_Code:Get2Free")
    if flag == 'low_income_high_spend':
        print("Phone_Number: "+phone_number+" - Hello Customer!! Get 20% off on buying pizzas upto Rs.100. Promo_Code:Get20Off")
    if flag == 'medium_income_medium_spend':
        print("Phone_Number: "+phone_number+" - Hello Customer!! Visit our store today for our new exciting menus and get compliment drink. Promo_Code:Compldk")
    if flag == 'high_income_low_spend':
        print("Phone_Number: "+phone_number+" - Hello Customer!! Buy One Get Two pizza and get 2 free coupons worth of Rs.199 each (Conditions Apply).  Promo_Code:B1G2")
    if flag == 'high_income_high_spend':
        print("Phone_Number: "+phone_number+" - Hello Customer!! Get 10% off on buying pizzas upto Rs.50. Promo_Code:Get10Off")

#Consumer recieves the message from the out_customer topic
consumer = KafkaConsumer(KAFKA_OUTPUT_TOPIC_NAME_CONS,group_id='group1',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',consumer_timeout_ms=60000)

print("start consuming")
#Loop runs till no messages recieved for 10 minutes
while True:
    for message in consumer:
        consumer.commit()
        full_string = ''.join(str(x) for x in message.value.decode('utf_8'))
        full_string = full_string.replace('"', '')
        consumer_df = pd.DataFrame([x.split('|') for x in full_string.split('\n')])
        consumer_df.columns = ['customer', 'phone_number', 'flag']
        business_logic(consumer_df["flag"].iloc[0],consumer_df["phone_number"].iloc[0])
    consumer.close()
    break