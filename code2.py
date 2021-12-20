import cv2
import numpy as np
min_width_react = 80 #min_width_reactangle
min_height_react = 80 #min_width_reactangle
offset = 6 # Error pixel 
delay = 60 # FPS of Video
count_line_position = 550

detect = []
counter = 0

#Initialize Substructor

cap = cv2.VideoCapture(r"D:Learning\AI\Project\Vehicle counter\cars.mp4")
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

def center_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx,cy


#Get Black/White detector 
while True:
    ret,frame1 = cap.read()
    #Show greyscale(not including anything below :DETECT,COUNTING)
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(grey, (3,3),5)
    #Show blur(not including anything below)
    #cv2.imshow('blur',blur)

   # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE,kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE,kernel)
    counterShape,h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     
    #show the line to detect vehicle in normal
    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)
    #show the line to detect vehicle in greyscale
    cv2.line(grey,(25,count_line_position),(1200,count_line_position),(255,127,0),3)

    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue
        
        # Put a rectangle and text to detect vehicle in normal video
        cv2.rectangle(frame1, (x,y),(x+w,y-20),(0,0,255),cv2.FILLED)
        cv2.rectangle(frame1, (x,y),(x+w,y+h),(0,0,255),2)
        cv2.putText(frame1,"Vehicle "+str(counter),(x,y-10),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)

        # Put a rectangle and text to detect vehicle in grayscale
        cv2.rectangle(grey, (x,y),(x+w,y-20),(0,0,255),cv2.FILLED)
        cv2.rectangle(grey, (x,y),(x+w,y+h),(0,0,255),2)
       # cv2.putText(grey,"Vehicle "+str(counter),(x,y-10),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)

    


        center = center_handle(x,y,w,h)
        detect.append(center)

        #Show the circle in grey scale 
        cv2.circle(frame1,center,4, (0,0,255),-1)

        #Show the circle in grey scale 
        cv2.circle(grey,center,4, (0,0,255),-1)


        #for (x,y) in detect:
          #  if y<(count_line_position+offset) and y>(count_line_position-offset):
             #   counter+=1
            #Show the line in normal if a car move into   
          #  cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)

            #Show the line in greyscale if a car move into
           # cv2.line(grey,(25,count_line_position),(1200,count_line_position),(0,127,255),3)


           # detect.remove((x,y))
            

    #Put text in normal video
    #cv2.putText(frame1,"Vehicle Counter: "+str(counter),(450,70),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5)       

    #Put text in greyscale video
    #cv2.putText(grey,"Vehicle Counter: "+str(counter),(450,70),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5) 

    #cv2.imshow('Detecter',dilatada) 

    # Show the video in normal
    cv2.imshow('Video Original',frame1)

    #Show the video in greyscale
    cv2.imshow('Video in gray',grey)

    if cv2.waitKey(1) == 14:
        break

cv2.destroyAllWindows()
cap.release()