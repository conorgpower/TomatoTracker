from picamera import PiCamera
from time import sleep

# (1) CAPTURE IMAGE
def captureImage():
    camera = PiCamera()

    # Alpha makes preview transparets for debuging
    camera.start_preview(alpha=200)

    #Sleep to allow camera brightness to adjust
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    image_directory = '/home/pi/Desktop/image.jpg'
    return image_directory

# (2) CLASSIFY IMAGE
import cv2
import tensorflow as tf

categories = ['Tomato_Septoria_leaf_spot', 
              'Potato___Early_blight',
              'Pepper__bell___healthy']

def prepare(image_directory):
    image_size = 256
    image_array = cv2.imread(image_directory)
    image_array = cv2.resize(image_array, (256, 256))
    return image_array.reshape(-3, image_size, image_size, 3)

def classify(image_directory):
    model = tf.keras.models.load_model("/home/pi/Desktop/TomatoTracker/my_model")

    prediction_image = model.predict([prepare(image_directory)])
    prediction_category = categories[int(prediction_image[0][0])]
    return prediction_category


# (3) UPLOAD TO AWS
import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# (4) SEND SMTP NOTIFICATION

import pathlib
import smtplib
import private as prv
from email.mime.image import MIMEImage

def sendEmail(prediction_category, image_url):
    try:
        sent_from = 'tomatotracker.business@gmail.com'
        to = ['tomatotracker.business@gmail.com']
        subject = 'Toato Tracker Message'
        body = """Hey,\n
                It seem that an instance of {prediction_category} has been found by the camera?\n 
                You can view the image here:\n{image_url}.\n\n
                - TomatoTracker"""

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        smtp_result = 'Email sent!'
        print (smtp_result)
        return smtp_result
    except:
        smtp_result = 'Something went wrong...'
        print (smtp_result)
        return smtp_result

# (5) EXECUTE PROGRAM

from datetime import datetime

def main():
    # Image that would be used in case of capturing live image
    image_directory = captureImage()

    # Image used for demonstration purposes
    image_directory = '/home/pi/Desktop/TomatoTracker/input/plantdisease/PlantDisease/Potato___Early_blight/001187a0-57ab-4329-baff-e7246a9edeb0___RS_Early.B 8178.JPG'
    
    # Classify Image
    prediction_category = classify(image_directory)
    
    # Upload Image to AWS S3 Bucket
    timestamp = datetime.now().timestamp()
    image_name = f'{prediction_category}-{timestamp}.jpg'
    upload_file(image_directory, 'tomato-tracker-images', image_name)

    # Send SMPT Email Notification
    image_url = f'https://tomato-tracker-images.s3-eu-west-1.amazonaws.com/{prediction_category}-{timestamp}.jpg'
    smtp_result = sendEmail(prediction_category, image_url)

    if (smtp_result == 'Email sent!'):
        print("PROCESS SUCCESSFULLY COMPLETED!")
    else:
        print("PROCESS FAILED!")

main()