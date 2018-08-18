############################################################################################
#
# The MIT License (MIT)
# 
# TASS Facenet Classifier Client
# Copyright (C) 2018 Adam Milton-Barker (AdamMiltonBarker.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Title:         TASS Facenet Classifier Client
# Description:   Python client to send images to the IDC & TASS classifier endpoint
# Configuration: required/confs.json
# Last Modified: 2018-08-09
#
# Example Usage:
#
#   $ python3.5 Client.py
#
############################################################################################

print("")
print("")
print("!! Welcome to TASS Facenet Classifier Client, please wait while the program initiates !!")
print("")

import os, sys

print("-- Running on Python "+sys.version)

import requests, json, cv2, time
from tools.Helpers import Helpers

print("-- Imported Required Modules")

class Client():

    def __init__(self):

        self.Helpers = Helpers()
        self._configs = self.Helpers.loadConfigs()

        self.addr = "http://"+self._configs["Cameras"][0]["Stream"]+':'+str(self._configs["Cameras"][0]["StreamPort"])
        self.TASSapiUrl = self.addr + '/api/TASS/infer'

        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}

        print("-- Client Initiated")

        self.testTASS()

    def testTASS(self): 

        print("-- Using TASS Facenet Classification")
        print("")

        testingDir  = self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["TestingPath"]

        for test in os.listdir(testingDir):

            print("-- Testing Dir: "+testingDir)
            
            if test.endswith('.jpg') or test.endswith('.jpeg') or test.endswith('.png') or test.endswith('.gif'):
                
                print("-- Sending "+testingDir+test)
                self.sendImage(testingDir+test,"TASS")
                print("")
                    
    def sendImage(self, image, model):

        img = cv2.imread(image)
        _, img_encoded = cv2.imencode('.png', img)
        response = requests.post(self.TASSapiUrl, data=img_encoded.tostring(), headers=self.headers)

        print(json.loads(response.text))


Client = Client()