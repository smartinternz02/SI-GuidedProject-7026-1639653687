import cv2
import boto3
import datetime
import requests
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

count=0

class VideoCamera(object):    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        #count=0
        global count
        success, image = self.video.read()
        is_success, im_buf_arr = cv2.imencode(".jpg", image)
        image1 = im_buf_arr.tobytes()
        client=boto3.client('rekognition',
                        aws_access_key_id="AKIAT6SBFGZSOUOAHIU4",
                        aws_secret_access_key="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",
                        aws_session_token="FwoGZXIvYXdzEFkaDGsQ1aEAfFSJ6yR5PCLEAe1ho0XFubj1OwnDRHVfhIUQ7JO46/9XzuNxHkMl3gen5gtmUlWPTFTfqt73eg0lzLdJeIAX7wO+GTrUaYzSJsJdZzeOr0EqHpR3GIoOhihvTlSRyZDNka9U+66Rs1yXoWQn5PHMli/DMGtxm2uxCEd73YpucbBE//UvX0L4uQLEtaO/Nn/paDaHOJcxXDnVvZBg+BI/HrnNfJdPnY+nj5xQIU0Ks9L+QRhPxR2SloQjoiw0ZKn+G/vWjhWh+ZHstauoKUYo96St+gUyLdVLZSDrt3+wSwayVF74lthBvcoFIl637IVBx4zzMEJvMyJdRQoJ6XVHGX8uSQ==",
                        region_name='us-east-2')
        response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-2:271793337956:project/detect_mask/1641196447554',Image={
            'Bytes':image1})
        print(response['CustomLabels'])
        
        if not len(response['CustomLabels']):
            count=count+1
            date = str(datetime.datetime.now()).split(" ")[0]
            #print(date)
            url = "https://zw6ycp08i7.execute-api.us-east-2.amazonaws.com/countmask?date="+date+"&count="+str(count)
            resp = requests.get(url)
            f = open("countfile.txt", "w")
            f.write(str(count))
            f.close()
            #print(count)

        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_rects:
        	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        	break
        ret, jpeg = cv2.imencode('.jpg', image)
        #cv2.putText(image, text = str(count), org=(10,40), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(1,0,0))
        cv2.imshow('image',image)
        return jpeg.tobytes()
