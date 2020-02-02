yum install -y python3
yum install -y python3-pip
pip3 install Flask
pip3 install Marshmallow
pip3 install pymongo
pip3 install passlib
pip3 install flask-restplus
pip3 install requests

mkdir -p /var/PalosLanesV2/Skyrim
cd /var/PalosLanesV2/Skyrim
aws s3 cp s3://chicagolandbowlingservice.com-bootstrap/Skyrim . --recursive
echo "[Unit]
Description=PalosLanes
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/bin/python3 /var/PalosLanesV2/Skyrim/app.py

[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/PalosLanes.service

systemctl enable PalosLanes
systemctl start PalosLanes
