#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class-o-vision -
(Pi Camera / Google Cloud Vision API / Smartlogic taxonomy interface)
"""

import os
import io
import json
import requests
import xml.etree.ElementTree as ET
import webbrowser
from time import sleep

from google.cloud import vision
from google.cloud.vision import types
from picamera import PiCamera


# Add service account to OS environ path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    r'service_account_key/REMOVED.json'

# Settings
TIMER = 4
SENSITIVITY = 2

# Raspberry Pi Camera==========================================================
camera = PiCamera()
camera.resolution = (1920, 1440)
camera.start_preview(fullscreen=False, window=(
    100, 100, 700, 900), vflip=True, hflip=True)
sleep(TIMER)
camera.capture('photo.jpg')
camera.stop_preview()


# Google Cloud Vision API function=============================================
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    # Prints the complete text
    try:
        print(str(texts[0].description))
        # Outputs text to output_string, the * acts as a multiplier to boost
        # classification
        output_string = str(texts[0].description)*SENSITIVITY
    except:
        print('Text not detected')
        output_string = ""

    return output_string


# Call the Google Cloud API function
doc_text = detect_text('photo.jpg')

# Smartlogic taxonomy API function=============================================
API_KEY = "REMOVED"


def classification(doc_text, API_KEY):
    """Sends text from document_request() to classification server."""
    try:
        # Get an access token==================================================
        baseUrl = "https://cloud.smartlogic.com"
        apiKey = API_KEY
        tokenRequest = {"grant_type": "apikey",
                        "key": apiKey,
                        "Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(baseUrl + "/token", tokenRequest)
        accessToken = r.json()['access_token']

        # Specify classification parameters====================================
        request = {"body": f"""<?xml version="1.0" encoding="UTF-8" ?>
            <request op="CLASSIFY">
            <document>
                <body type="TEXT">
                {doc_text}
                </body>
                <path/>
                <singlearticle/>
                <threshold>48</threshold>
                <clustering type="RMS" threshold="20"/>
                <META NAME="example">short</META>
                <operation_mode>CAT</operation_mode>
                <feedback/>
            </document>
            </request>"""}

        # Send the message including the authorization header==================
        csUrl = "https://cloud.smartlogic.com/REMOVED"
        header = {"Authorization": "bearer " + accessToken,
                  "Content_type": "form-data"}
        r = requests.post(csUrl, data=request, headers=header)

        # Parse the root text with element tree
        root = ET.fromstring(r.text)

        # Loop through XML and find META tags
        terms = []
        for term in root.iter('META'):
            if term.attrib['name'] == 'Generic_UPWARD':
                terms.append([term.attrib['value'],
                              term.attrib['score']])

        # This divides the list of terms in half to remove duplicates
        # Hacky! - reconsider this
        cleaned_term_list = terms[:int(len(terms) / 2)]

        return cleaned_term_list

    except:
        return False


# Call Sitecore classification function
class_output = classification(doc_text, API_KEY)

if len(class_output) == 0:
    list_content = "<li>No matching topics</li>"
else:
    terms = class_output
    li = []
    for term in terms:
        term[1] = '(' + term[1] + ')'
        x = ' '.join(term)
        li.append(x)

    li_html = []
    for counter, item in enumerate(li):
        item = f'<li class="fadeInAnimated" id="delay{str(counter+1)}">' + \
            item + '</li>'
        li_html.append(item)

    list_content = '\n'.join(li_html)

# Write to HTML file===========================================================
# TODO Dynamically generate CSS rules
f = open('html_out.html', 'w')
html_head = """<!DOCTYPE html>
<html lang="en">

<head>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Slab|Michroma&display=swap" rel="stylesheet" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <style>
        body {
            margin: 0;
            box-sizing: border-box;
        }
        
        html {
            padding: 0;
            margin: 0;
            font-family: "Josefin Slab", serif;
            font-size: 40px;
        }
        
        .wrapper {
            margin: auto;
            width: max-content;
            min-height: 100vh;
            background-color: black;
            color: white;
        }
        
        .ocr {
            background-color: white;
            color: black;
        }
        
        #ocr-text {
            padding: 0 50px;
        }
        
        .outer-wrap {
            min-height: 100vh;
            background-color: black;
        }
        
        .title {
            text-align: center;
            border-bottom: 1px solid white;
            margin: 0;
            padding: 30px 0 20px 0;
        }
        
        ul {
            padding: 10px;
        }
        
        li {
            list-style-type: none;
            margin: 15px;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        .fadeInAnimated {
            opacity: 0;
            animation: fadeIn 2s forwards;
            /* forwards (animation-fill-mode) retains the style from the last keyframe when the animation ends */
        }
        
        #delay1 {
            animation-delay: 1s;
        }
        
        #delay2 {
            animation-delay: 2s;
        }
        
        #delay3 {
            animation-delay: 3s;
        }
        
        #delay3 {
            animation-delay: 3s;
        }
        
        #delay4 {
            animation-delay: 4s;
        }
        
        #delay5 {
            animation-delay: 5s;
        }
        
        #delay6 {
            animation-delay: 6s;
        }
        
        #delay7 {
            animation-delay: 7s;
        }
        
        #delay8 {
            animation-delay: 8s;
        }
        
        #delay9 {
            animation-delay: 9s;
        }
        
        #delay10 {
            animation-delay: 10s;
        }
        
        #delay11 {
            animation-delay: 11s;
        }
        
        #delay12 {
            animation-delay: 12s;
        }
        
        #delay13 {
            animation-delay: 13s;
        }
        
        #delay14 {
            animation-delay: 14s;
        }
        
        #delay15 {
            animation-delay: 15s;
        }
        
        #delay16 {
            animation-delay: 16s;
        }
        
        #delay17 {
            animation-delay: 17s;
        }
        
        #delay18 {
            animation-delay: 18s;
        }
        
        #delay19 {
            animation-delay: 19s;
        }
        
        #delay20 {
            animation-delay: 20s;
        }
        
        #delay21 {
            animation-delay: 21s;
        }
        
        #delay22 {
            animation-delay: 22s;
        }
        
        #delay23 {
            animation-delay: 23s;
        }
        
        #delay24 {
            animation-delay: 24s;
        }
        
        #delay25 {
            animation-delay: 25s;
        }
        
        #delay26 {
            animation-delay: 26s;
        }
        
        #delay27 {
            animation-delay: 27s;
        }
        
        #delay28 {
            animation-delay: 28s;
        }
        
        #delay29 {
            animation-delay: 29s;
        }
        
        #delay30 {
            animation-delay: 30s;
        }
    </style>
    <title>CLASS-O-VISION</title>
</head>"""

html_body = f"""<body>
    <div class="outer-wrap">
        <div class="wrapper">
            <h2 class="title">CLASS-O-VISION</h2
      <ul>
{list_content}
      </ul>
    </div>
</div>
    <div class="ocr">
        <h2 class="title">OCR TEXT</h2>

        </div>
        <div id="ocr-text">
            {doc_text}
        </div>
</body>

</html>"""

html_out = html_head + html_body
f.write(html_out)
f.close()

# Open browser
webbrowser.open('html_out.html')
