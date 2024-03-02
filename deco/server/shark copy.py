import pyshark
import os
# Set up live capture on a specific network interface, filtering for port 8000
# capture = pyshark.LiveCapture(interface='en0')
capture = pyshark.LiveCapture(interface='lo0',
                                bpf_filter='tcp port 8000',
                                override_prefs={'ssl.keylog_file': os.path.abspath('sslkeys_google.log')},
                               debug=True,
                              )




# Start the capture
for packet in capture.sniff_continuously():
    print('Just arrived:', packet)