#
#SPA Group 181 - SPA Assignment 2
#This script recieves the customer data from the kafka topic by using kafka consumer and process the data
#and send the processed data to different kafka topic using kafka producer
#
#Importing libraries
import pandas as pd
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from io import StringIO
from kafka import KafkaConsumer, TopicPartition
import json
import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

register_df=pd.read_csv('pizza_customers.csv')

KAFKA_TOPIC_NAME_CONS = "customer"
KAFKA_OUTPUT_TOPIC_NAME_CONS = "outcustomer"
KAFKA_BOOTSTRAP_SERVERS_CONS = "localhost:9092"


tp = TopicPartition(KAFKA_TOPIC_NAME_CONS,0)
#Recieving messages from customer topic using consumer object, If no records recieved for 10 mins then it will close automatically
consumer = KafkaConsumer('customer',group_id='group1',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',consumer_timeout_ms=60000)

lastOffset = consumer.end_offsets([tp])[tp]

print("start consuming")
while True:

    df = pd.DataFrame([])

    for message in consumer:
        consumer.commit() #Commit the message once the data recieved from the topic

        #
        #Removing the double quotes after recieving the messsage
        #
        full_string=''.join(str(x) for x in message.value.decode('utf_8'))
        full_string=full_string.replace('"','')

        #
        #Convert pipe delimited string to dataframe and adding column names
        #
        consumer_df=pd.DataFrame([x.split('|') for x in full_string.split('\n')])
        consumer_df.columns = ['customer', 'phone_number', 'latitude', 'longitude', 'dtime']

        consumer_df["customer"] = consumer_df["customer"].astype(str).astype(int)
        consumer_df["phone_number"] = consumer_df["phone_number"].astype(str)
        consumer_df["latitude"] = consumer_df["latitude"].astype(str).astype(float)
        consumer_df["longitude"] = consumer_df["longitude"].astype(str).astype(float)
        consumer_df["dtime"] = consumer_df["dtime"].astype(str)

        #
        #Lookup the regisetered dataset and verifies customer exists or not
        #
        merged_df=consumer_df.merge(register_df, left_on='customer', right_on='CustomerID', how='inner',indicator=True)

        #
        #Categorize the customer and assign a flag to them
        #if income<=40 and score <=40 then flag="low_income_low_spend"
        #if income<=40 and score >60 then flag="low_income_high_spend"
        #if income>40 and score <=70 and score>40 and score<=60 then flag="medium_income_medium_spend"
        #if income>70 and income <=40 then income<="high_income_low_spend"
        #if income>70 and score >60 then flag="high_income_high_spend"
        #After assign the flag, send customer data along with flag to out_customer topic
        #
        if merged_df.empty:
            continue
        elif (merged_df["Annual Income (k$)"] <= 40).all() and (merged_df["Spending Score (1-100)"]).all() <= 40:
            flag="low_income_low_spend"
            str_output = merged_df["customer"].iloc[0].astype(str) + '|' + merged_df["phone_number"].iloc[0] + '|' + flag
            producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(KAFKA_OUTPUT_TOPIC_NAME_CONS, str_output)
            producer.flush()
        elif (merged_df["Annual Income (k$)"] <= 40).all() and (merged_df["Spending Score (1-100)"] > 60).all():
            flag="low_income_high_spend"
            str_output = merged_df["customer"].iloc[0].astype(str) + '|' + merged_df["phone_number"].iloc[0] + '|' + flag
            producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(KAFKA_OUTPUT_TOPIC_NAME_CONS, str_output)
            producer.flush()
        elif (merged_df["Annual Income (k$)"] > 40).all() and (merged_df["Annual Income (k$)"] <= 70).all() and (merged_df["Spending Score (1-100)"] > 40).all() and (merged_df["Spending Score (1-100)"] <= 60).all():
            flag="medium_income_medium_spend"
            str_output = merged_df["customer"].iloc[0].astype(str) + '|' + merged_df["phone_number"].iloc[0] + '|' + flag
            producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(KAFKA_OUTPUT_TOPIC_NAME_CONS, str_output)
            producer.flush()
        elif (merged_df["Annual Income (k$)"] > 70).all() and (merged_df["Spending Score (1-100)"] <= 40).all():
            flag="high_income_low_spend"
            str_output = merged_df["customer"].iloc[0].astype(str) + '|' + merged_df["phone_number"].iloc[0] + '|' + flag
            producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(KAFKA_OUTPUT_TOPIC_NAME_CONS, str_output)
            producer.flush()
        elif (merged_df["Annual Income (k$)"] > 70).all() and (merged_df["Spending Score (1-100)"] > 60).all():
            flag="high_income_high_spend"
            str_output = merged_df["customer"].iloc[0].astype(str) + '|' + merged_df["phone_number"].iloc[0] + '|' + flag
            producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send(KAFKA_OUTPUT_TOPIC_NAME_CONS, str_output)
            producer.flush()

    consumer.close()
    break