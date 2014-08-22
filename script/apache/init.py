
import os

os.system('cp im /etc/apache2/sites-available/im.conf')
os.system('a2dissite *')
os.system('a2ensite im.conf')
os.system('apachectl restart')

