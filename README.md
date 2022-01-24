# Pi-PWM-Fan-Controller
 Pi PWM Control for Ubuntu using python

Install packages to read gpio pins and run the program
```
sudo apt install python3-lgpio python3
```

Connect your PWM output to pin GPIO 13 according to https://pinout.xyz/ You can change this by editing the `FAN_PIN` variable under the configuration settings, This pin must be a PWM pin so GPIO 12, 13, 18 or 19. 

Currently the program doesn't read from the RPM pin and is using the speed and the max RPM to calculate the RPM. I'm using a NF-F12 5v PWM Noctua fan that has a 1500 max RPM. To change the RPM output to be correct edit the `MAX_FAN_SPEED` to be the your fan max rpm 

Install fan-control.service at 
```
/etc/systemd/system/fan-control.service
```
Don't forget to update the path with the correct path name ( use `pwd`)

Then enable the service to start on boot and start service
```
systemctl enable fan-control.service
systemctl start fan-control.service
```
