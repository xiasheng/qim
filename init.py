import os,sys

# init db
print '-----init django database-----'
os.system('cd script/db;python init.py')

# init log conf
print '-----init django log-----'
os.system('cd script/log;python init.py')

# init django model
print '-----init django model-----'
os.system('python manage.py sqlall models')
os.system('python manage.py syncdb')

# init apache
print '-----init apache-----'
os.system('cd script/apache;python init.py')
