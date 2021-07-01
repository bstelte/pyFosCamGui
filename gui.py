#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from tkinter import *
from PIL import ImageTk, Image
from foscontrol import Cam
import sys
import time
import cv2

try:  # PY3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

class App:


    def getpic(self):
        self.img = None
        try:
            (self.img, fnm) = self.do.snapPicture()
        except:
            print("no connection")
        # Possible errors/exceptions:
        #
        # urllib.error.URLError (e.g. no route to host)
        # ssl.CertificateError (e.g. wrong or no ssl certificate)
        # img == None (e.g. wrong password)

        if self.img is not None:
            print('Writing picture')
            open('test.jpg', 'wb').write(self.img)
            #time.sleep(0.1)
            #self.loopCapture()
        else:
            print('No picture')       


    def loopCapture(self):
        # Get the latest frame and convert image format
        self.OGimage = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.OGimage = Image.fromarray(self.OGimage) # to PIL format
        self.image = self.OGimage.resize((960, 540), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        #self.img = Image.open("test.jpg")
        #resize
        #basewidth=1000
        #wpercent = (basewidth/float(self.img.size[0]))
        #hsize = int((float(self.img.size[1])*float(wpercent)))
        #self.img = self.img.resize((basewidth,hsize), Image.ANTIALIAS)
        #self.tkimg[0] = ImageTk.PhotoImage(self.img)
        #self.label.config(image=self.tkimg[0])

        self.window.after(self.interval, self.loopCapture)

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()      

        self.window = master        

        self.interval = 10 # Interval in ms to get the latest frame

        #self.label = Label(frame)
        #self.label.pack()

        # Create canvas for image
        self.canvas = Canvas(self.window, width=960, height=540)
        self.canvas.pack()
        # Update image on canvas
        root.after(self.interval, self.loopCapture)

        self.img = None
        self.tkimg = [None]  
        self.button = Button(frame, 
                             text="QUIT", fg="red",
                             command=frame.quit)
        self.button.pack(side=LEFT)
        #self.slogan = Button(frame,
        #                     text="Reload",
        #                     command=self.loopCapture)
        #self.slogan.pack(side=LEFT)
        self.glogan = Button(frame,
                             text="savePic",
                             command=self.getpic)
        self.glogan.pack(side=LEFT)
        self.rotleft = Button(frame,
                             text="Left",
                             command=self.rotleft)
        self.rotleft.pack(side=LEFT)
        self.rotright = Button(frame,
                             text="Right",
                             command=self.rotright)
        self.rotright.pack(side=LEFT)
        self.rotup = Button(frame,
                             text="Up",
                             command=self.rotup)
        self.rotup.pack(side=LEFT)
        self.rotdown = Button(frame,
                             text="Down",
                             command=self.rotdown)
        self.rotdown.pack(side=LEFT)
        self.rotzoomin = Button(frame,
                             text="zoomIn",
                             command=self.zoomin)
        self.rotzoomin.pack(side=LEFT)
        self.rotzoomout = Button(frame,
                             text="zoomOut",
                             command=self.zoomout)
        self.rotzoomout.pack(side=LEFT)
        config = ConfigParser()

        # see cam.cfg.example
        config.read(['cam.cfg'])
        prot = config.get('general', 'protocol')
        host = config.get('general', 'host')
        port = config.get('general', 'port')
        user = config.get('general', 'user')
        passwd = config.get('general', 'password')

        if sys.hexversion < 0x03040300:
            # parameter context not available
            ctx = None
        else:
            # disable cert checking
            # see also http://tuxpool.blogspot.de/2016/05/accessing-servers-with-self-signed.html
            import ssl

            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        # connection to the camera
        self.do = Cam(prot, host, port, user, passwd, context=ctx)
        print("DevInfo:")
        print(self.do.getDevInfo())
        print("Image Setting:")
        print(self.do.getImageSetting())
        print("Video Parameter:")
        print(self.do.getVideoStreamParam())
        print("Network Parameter:")
        print(self.do.getIPInfo())

        self.video = self.do.getRTSPStream()
        print("RTSP URL is ",self.video)
        self.cap = cv2.VideoCapture(self.video)

        self.getpic()
        #self.loopCapture()

    def rotleft(self):
        self.do.ptzMoveLeft()
        time.sleep(0.3)
        self.do.ptzStopRun()
        #time.sleep(0.1)
        #self.getpic()

    def rotright(self):
        self.do.ptzMoveRight()
        time.sleep(0.3)
        self.do.ptzStopRun()
        #time.sleep(0.1)
        #self.getpic()

    def rotup(self):
        self.do.ptzMoveUp()
        time.sleep(0.3)
        self.do.ptzStopRun()
        #time.sleep(0.1)
        #self.getpic()

    def rotdown(self):
        self.do.ptzMoveDown()
        time.sleep(0.3)
        self.do.ptzStopRun()
        #time.sleep(0.1)
        #self.getpic()

    def zoomin(self):
        self.do.zoomIn()
        time.sleep(0.3)
        self.do.zoomStop()
        #time.sleep(0.1)
        #self.getpic()

    def zoomout(self):
        self.do.zoomOut()
        time.sleep(0.3)
        self.do.zoomStop()
        #time.sleep(0.1)
        #self.getpic()

    def write_slogan(self):
        print("Ready")

    

root = Tk()
app = App(root)
root.mainloop()
