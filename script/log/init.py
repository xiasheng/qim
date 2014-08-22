
import os

# create log file
log_filename = 'im.log'
log_dir = '/var/log/django'
log_file = os.path.join(log_dir, log_filename)

if not os.path.exists(log_dir):
    os.mkdir(log_dir, 0777)
    
if not os.path.exists(log_file):
    os.mknod(log_file)
    os.chmod(log_file, 0777)


# init memcached
#os.system('killall memcached') 
#os.system('memcached -d')

