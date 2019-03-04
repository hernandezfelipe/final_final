import cv2
import os
import numpy as np
import psutil
import easygui
from tweet import post_picture
from time import sleep, time
from datetime import datetime
from audio import bark
from url import get_url
from model import predict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("a", nargs='?', default="empty")
args = parser.parse_args()

 
p = psutil.Process(os.getpid())
p.nice(19)  # set>>> p.nice()10

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
   
cam = cv2.VideoCapture(0)    


path = os.getcwd()

bark_time = 0.45

run_time = bark_time + 0.05

wait = 0
WAIT_TURNS = int(60.0 / run_time)

SCORE_THRESHOLD = 0.90 # > 
SOUND_THRESHOLD = 0.90
time_init = time()
time_end = 0

pic_enabled = True

old_sound = 0

command_delay = 0

command = "Init"

pic_ok = "O"

loop = int(20. / run_time)

while True:

    score = 0
    
    pic_ok = "O"
            
    now = datetime.now()         
    time_taken = time() 
    
    current_sound = bark(bark_time)
    
    #current_sound = 0
    
    
    dif = current_sound - old_sound
    
    if dif >= 0:
    
        sound = dif
        
    else:
    
        sound = 0    
     
    print("Sound:", '{:04f}'.format(sound))
    
    
    s, img = cam.read()
    
    if args.a == 'nocam':
    
        pass
        
    else:
   
        cv2.imshow("Cam", img)
        cv2.waitKey(1)             
    
    time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
    
    if sound > SOUND_THRESHOLD:
      
        score = predict(img)    
    
        print("Score:", '{:04f}'.format(score), "Sound:", '{:04f}'.format(sound))
             
                  
        if now.hour < 20 and now.hour > 6:
          
            if score > SCORE_THRESHOLD and wait == 0:
                
                cv2.imwrite(path+"/auto_tweet.png",img)
                
                pic_id = str(now.month) + str(now.day) + str(now.hour) +  str(now.minute) + str(now.second)
         
                print("Salvo em "+path+"/output/tiao"+str(pic_id)+".png")
                cv2.imwrite(path+"/output/tiao"+str(pic_id)+".png", img)
                
                pic_ok = "X"

                wait = WAIT_TURNS
                
                try:
                
                    print("Postando foto")
                    
                    if pic_enabled:
                        
                        post_picture(path+"/auto_tweet.png")
                        pass
                        
                except:
                
                    print("Corrigir")
                           
            
    if wait > 0:
    
        wait -= 1                        
                    
                                        
        f = open("report.txt", 'a')

        f.write("W: "+ str(wait).zfill(2) + " " + str(time_id) + " S: " + '{:04f}'.format(score) + " V: " + '{:04f}'.format(sound) + " " + pic_ok + "\n")

        f.close()           



    command_delay = (command_delay + 1) % loop
    
    if command_delay == 0:
                
        try:
            command = get_url()          
            if command == "reboot" or command == "Reboot":
                os.system("reboot")        
            elif command == "shutdown" or command == "Shutdown":
                os.system("shutdown now")
            elif command == "enable" or command == "Enable":
                pic_enabled = True            
            elif command == "disable" or command == "Disable":
                pic_enabled = False            
        except:    
            pass
     
    time_end = time()  
     
       
    print('{:04f}'.format(time_end - time_taken), "Sec", "Cmd:", command, "-", str(command_delay).zfill(2), "Time:", time_id, "W:", str(wait).zfill(3)) 
    
    f = open("last_run.txt","w")
    f.write(time_id+"\n")
    f.close()
    
    old_sound = sound
