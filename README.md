# Controly poor documentation!

This will explain if you will want to add new module or device to the Controly!

## 1. Adding a new device
### 1. a) Code on device (on raspberry and arduino):
**On raspberry** all you will need is a copy of "Controly Device". In there change DEVICE_NAME variable in device_specific.py to the name of device (same as you will set it in the Controly website

**On arduino** you will run arduino code called "main.ino", but first you have to change **jsonUpdate** function in "jsonUpdateFunction.ino". Set this function so that will update every needed value with a value from json changes from Controly. You will also have to define every variable at the start of the "main.ino" file

### 1. b) Code on server (Controly website):
Just go to the Controly admin page, to the device section and click add new device. Fill out the form and enjoy!