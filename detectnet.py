#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import sys
import argparse

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "babymo",
  "private_key_id": "78bba2edbdf122bc328ddfee3535a31c9c8052ef",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCVBD0lXutpBfDt\ngrZES8c/ajSLXix4iJaLcIfosjLztmirKhplD7Ct3oDGW7qG+8o+p75H2n8bLJei\nrthl6rC1HYuuzSPgW7MPW6Q9fFAGM81p3n8BtMiVihEyDwTq5RYr5GGzAuyVDMQS\nowtQz8G18TN56eLkzTfDspNx1KpUNLaoAFLisIssQ0sx2uM9paEiFZRAdIpkE7hR\nSQp/9Aj2xOT2I91q496KBVooZxg7Yb1pvQyoZ1d1gXLhZkBjh0/yxCp6l+I1HaKe\nJc6v4JgXxj7whLCz1p1DOWq+apSEYNQJ0VXdrjIfZ7KThUr0VGEdeA/3XOfkna43\nv4IpMXuRAgMBAAECggEAHpmU+9JSyYl2iLM9fedItkk3GoJfY+36ag5U3lAPffPQ\naQuXiXawG3gUHgdylWrphDW6cXNZBAnDZpz8Y2tO15ZGW4IVEqqJ6cayAo0/OpLT\nJOETWBSZVvnX351tb1XVGHTIqjOYxN+u+LvB5FmRR+0MmsWQOdc5Uwad1/Npeapc\nOaZ8DiJm3nw7DPRylHwj4dLhUAMfPkX+6vLrY6UdQag7AXxI2dp6Bv2WjNWD4oxP\nVKp8ylvhpvAlGDGklpgLqJRlFdSryAgAWvzfohFjsOAXCJpt9vxOdHRP58qbVeXo\n/Y1TsvKVCinZWVHMxgtsOE9w0E4LiedflrTA98aspQKBgQDF+CRHVkLCjXigaqgY\nz3ryQlGEeop4SsG5TtUB2UaMvC5SQZAgiRTSTFNsw47hw9O/yFZjA9kvIEPpj18y\nmGxWtNvHdQaCEH0mlxF+9oyUQMVwwOGzulJE9zLbI81ArrQ9UlUOV067Fb3hmmGZ\nDBPT0J4JGl/RLDg1737ht+ucTQKBgQDAsp+SzQ3IJZjyRUjHs69c36CyOi5bSjoz\nOjYXEaQfkeMtpiXUNeVwhzlrRaMOE4fZSdgMDcjT1W6dI+JMC3S3iSZ1dbNba/EN\nOgDCPZAJGqMVU5g6y24IXAcpryibl5leXjnTBDJVmKXm9cKWjRQO3Nz5Em9dV6A3\nWikN9sPuVQKBgQDFFAQ5qBwJxgBh4gu5t0LzzSWNttgGbJVyPpI6puxeyi9q3631\nVcIOoMEkM4IYKnSwJWYqZ/hbu8kfyATDP44Kuz1X0J5L+NI+CoH2XMcSB3EGkF2g\nKEoiMdzE311DmSgBK+dUwYG1KS3AW4nxbF6IrNPGyCS+/UBwIR204v2AuQKBgQDA\nV4uAdL008pJgAVhMPcbk5TL5s6lh5g2B5LDpBerUuEIS5q0LzWBfmhpuQOwouMX4\n1gSYw4maKIhowdC4Jxcxu+xvgjStJGlP0n2/ZMPI0pXGS9K/nR8PqQxdR0E5TXEB\nCPye7KlxVxUCHH1G2TsUOtE2rHgMq9J4bb5c+dtIoQKBgQCTi+qYT1rrv20b3TJz\npfdLJzWLHmT9+A6RZ10uyWn0H8Hw9FbjjWvGKP0QuEtwi1FBW3UYjPwGTmGW/HeF\noKjasvzqtYmPfU33Z770DOHykH5+I+b3CqwkAv4zvdfEMB/WaMisPRpS2kesAw+F\nAV9AH8EyRr/TuzzhU3M7DqZoXw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-q8x6x@babymo.iam.gserviceaccount.com",
  "client_id": "116142140333015421400",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-q8x6x%40babymo.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

app = firebase_admin.initialize_app(cred)

db = firestore.client()

data_true = {
    'status_sids' : True
}

data_false = {
    'status_sids' : False
}
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    for detection in detections:
        # print(net.GetClassDesc(detection.ClassID))
        if (net.GetClassDesc(detection.ClassID) == 'covered_obstacle') or (net.GetClassDesc(detection.ClassID) == 'danger') or (net.GetClassDesc(detection.ClassID) == 'prone'):
            doc_ref = db.collection('status').document('cry_sids')
            doc_ref.set(data_true)
        else:
            doc_ref = db.collection('status').document('cry_sids')
            doc_ref.set(data_false)

    print("detected {:d} objects in image".format(len(detections)))

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():        
       print(detections)
       break
