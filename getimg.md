# Get Image from Raspberry pi
### 1. Initialize the RaspberryPi with its camera
Assuming that you have already configured your Raspberry Pi 3B+ and its camera module. We are going to use its internal camera package to simply grab the image and download to our PC.
### 2. Login on your Raspberry Pi with SSH and take shots
For example, use putty.exe on Windows environment and login on to your Pi under the same network.
```
  cd aaronrasp/documents
  mkdir ./SIimg
  cd ./SIimg
  raspistill -ss 100 -q 100 -t 5000 -tl 1000 -v -o img%04d.jpg
```
It will run for 5s and take each photos at 1s intervals with 100ms as shutter speed. Final outputs expect to be 6 pics.
### 3. download the images to your PC
It's super easy to use psftp.exe to transfer files.
- Login on in psftp.exe to your raspberry pi with `open Pi's_ip`
- Change to your files' directory `cd aaronrasp/documents/SIimg`
- Change your local directory on PC `lcd your_directory`
- `put file's_name` to upload `get file's_name` to download. Here we use `get -r ../SIimg` to download all the images

