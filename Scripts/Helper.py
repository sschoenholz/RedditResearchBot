#this is a script that will monitor the tracker to make sure that it restarts if it closes

import subprocess
import time
import Defines

status = open(Defines.HelperOutputFile,'w',0)

while True:
	status.write(str(time.time()) + '\t')
	
	subprocess.call(['python', Defines.ScriptFile])
	print 'System crashed... reboooting.'
	status.write(time.time() + '\n')

status.close()

