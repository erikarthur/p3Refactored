apt-get -qqy update
apt-get -qqy install python-flask 
apt-get -qqy install python-pip
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install redis
pip install passlib
pip install itsdangerous
pip install flask-httpauth
pip install oauth2client

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

