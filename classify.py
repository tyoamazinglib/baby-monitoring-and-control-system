import os
import sys, getopt
import signal
import time
from edge_impulse_linux.audio import AudioImpulseRunner
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import vlc
import time

runner = None
whitenoise = vlc.MediaPlayer("/home/tyo/linux-sdk-python/examples/audio/mixkit-big-waterfall-loop-2515.wav")
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

data_false = {
  'status_cry' : False
}

data_true = {
  'status_cry' : True
}

def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def help():
    print('python classify.py <path_to_model.eim> <audio_device_ID, optional>' )

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) == 0:
        help()
        sys.exit(2)

    model = args[0]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            #Let the library choose an audio interface suitable for this model, or pass device ID parameter to manually select a specific audio interface
            selected_device_id = None
            if len(args) >= 2:
                selected_device_id=int(args[1])
                print("Device ID "+ str(selected_device_id) + " has been provided as an argument.")

            for res, audio in runner.classifier(device_id=selected_device_id):
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    print('%s: %.2f\t' % (label, score), end='')
                    #print(res['result']['classification']['cry'])
                    if res['result']['classification']['cry'] > 0.99:
                        whitenoise.play()
                        doc_ref = db.collection('cry_status').document('cry')
                        doc_ref.set(data_true)
                        
                    else:
                        whitenoise.stop()
                        doc_ref = db.collection('cry_status').document('cry')
                        doc_ref.set(data_false)
                print('', flush=True)

        finally:
            if (runner):
                runner.stop()

if __name__ == '__main__':
    main(sys.argv[1:])
