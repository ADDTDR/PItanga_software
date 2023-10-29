```bash
sudo nano /etc/systemd/system/pitanga.service
```

add 
```conf
[Unit]
Description=PitangaService
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/ad/mdlh_ht16k33_python/ht16k33.py
WorkingDirectory=/home/ad/mdlh_ht16k33_python
Restart=always
User=ad
Group=ad

[Install]
WantedBy=multi-user.target

```

```bash 
sudo systemctl daemon-reload 
sudo systemctl start pitanga.service
sudo systemctl enable pitanga.service
```


on orangepi zero 
/home/adre/ht16k33_python