########################################################################################################
#### Import files ->
import cv2, time
import tkinter as tk
import os

from tkinter import * 
from tkinter import messagebox 
from datetime import datetime

#####################################################################################################################
##############  COMMANDS / functions  

#####  start button command
def camera():
    first_frame = None 
    status_list = [None,None]
    times = []
    image =0

    try :
        camera = cv2.VideoCapture(0)
        #video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
        try:
            os.remove("data.doc")
        except:
            pass
            
        while True:
            status = False
            
            return_value, frame = camera.read()

            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(21,21),0)
            
            if first_frame is None:
                first_frame = gray
                continue

            current_frame = cv2.absdiff(first_frame,gray)
            thresh_frame = cv2.threshold(current_frame,30,255,cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame,None, iterations=2)
            
            (cnts,_) = cv2.findContours(thresh_frame.copy(),
                                        cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

            for contour in cnts:
                if cv2.contourArea(contour) < 5000 :
                    continue
                status = True
                (x,y,w,h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
            
            status_list.append(status)

            
            if status_list[-1] == True and status_list[-2] == False:
                cv2.imwrite("image%04i.jpg"%image, frame)
                image += 1
                times.append(datetime.now())

            if status_list[-1] == False and status_list[-2] == True:
                times.append(datetime.now())

            
            cv2.imshow("grey frame",gray)
            cv2.imshow("current frame",current_frame)
            cv2.imshow("threshold frame",thresh_frame)
            cv2.imshow("color frame",frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                if status == True:
                    times.append(datetime.now())
                break
    except:
        tk.messagebox.showerror(title="CAM MOTION DETECTOR", message="Camera Not found")

    with open("data.doc","a") as data:
        for i in range(0,len(times),2):
            data.write(f'[start: {times[i]},end: {times[i+1]}]\n')

    camera.release()
    cv2.destroyAllWindows()

##### log button command
def log():
    try :
        os.system("start data.doc")
    except:
        tk.messagebox.showerror(title=None, message="Logs Not created yet.", **options)

##### image button command
def images():
    import subprocess
    subprocess.Popen(f'explorer /select,"{os.getcwd()}"')

#####  about button command
def about():     
    about_win = tk.Toplevel()
    about_win.iconbitmap(r"icons/icon.ico")
    about_win.geometry('300x400')
    about_win.resizable(width=False,height=False)
    about_win.title("ABOUT")
    
    about_img = tk.PhotoImage(file='icons/icon.png')        
    about_con = tk.Label(about_win,image=about_img)
    about_con .image = about_img
    about_con.pack(side=tk.TOP,pady=10)

    about_title = tk.Label(about_win,text="CAM MOTION DETECTOR\n")               
    about_title.pack(side=tk.TOP,pady=10)
    
    about_des = tk.Label(about_win,text="Version : 1.0.0\n \
Created By : SHUBHAM MAURYA")               
    about_des.pack(fill=tk.X)

##################################################################################################################################
############# GUI PROGRAMING  #############

################# ROOT SETTING 
root = Tk()
root.geometry('600x400')
root.title("CAM MOTION DETECTOR")
root.configure(bg="white") 
root.resizable(width=False,height=False)
root.iconbitmap(r"icons/icon.ico")


################ BUTTONS
##### info button 
info_button_image = tk.PhotoImage(file='icons/info.png')
info_button = tk.Button(root,width=40,height=40,bg="white",image=info_button_image,command = about)
info_button.place(x=540,y=15)

##### start button
start_button_image = tk.PhotoImage(file='icons/run2.png')
start_button = tk.Button(root,width=100,height=40,bg="white",fg="green",text ="START",image=start_button_image, compound="left", command = camera)
start_button.place(x=250,y=100)

##### log button 
log_button_image = tk.PhotoImage(file='icons/logs2.png')
log_button = tk.Button(root,width=140,height=40,bg="white",fg="#39A0FB",text ="CHECK LOGS",image=log_button_image, compound="left", command = log)
log_button.place(x=130,y=180)

##### image button 
images_button_image = tk.PhotoImage(file='icons/images.png')
images_button = tk.Button(root,width=140,height=40,bg="white",fg="#546E7A",text ="IMAGES",image=images_button_image, compound="left", command = images)
images_button.place(x=330,y=180)

##### Note 
label = tk.Label( root,bg="white",fg="red",height=2,text="*Press 'q' to quit the camera window", relief=RAISED )
label.pack(side=tk.BOTTOM,fill=tk.X)

### ending 
root.mainloop()