# LND-iot-app-launcher
An easy way to spin up a BTC Lightning node on an Odroid, and easily portable to other embedded linux platforms.

This project makes heavy use of the [Balena](balena.io) platform for managing fleets of embedded linux devices.
![Balena Logo](https://www.balena.io/blog/content/images/2017/10/balena_logo.jpg)


The goal of this project is to be able to create a Bitcoin Lightning node on Odroid devices, in around 24 hours. However, unlike other node projects, this will be a basic installation LND with some small steps to connect Python to the LND gRPC. This install is meant to be basic, so LND developers will have an easier time debugging issues, and not have to deal with setup problems.

## Example Python Projects to Extend Node Functionality
1. [M-D-Br/FlaskBitcoinDashboard](https://github.com/M-D-Br/FlaskBitcoinDashboard)
1. [bitromortac/lndmanage](https://github.com/bitromortac/lndmanage)

## Bill Of Materials
* Odroid XU4 or Raspberry Pi 3B+
* MicroSD Card: \~4gb: 
 * [Digi-Key: MicroSD 4GB AF4GUD3A-OEM](https://www.digikey.com/product-detail/en/atp-electronics-inc/AF4GUD3A-OEM/AF4GUD3A-OEM-ND/)
* Power Supply
 * [Amazon: CanaKit 5V Power Supply](https://www.amazon.com/gp/product/B00MARDJZ4/)
* 2.5" Hard Drive Enclosure
 * [Amazon: Hard Drive Enclosure](https://www.amazon.com/gp/product/B00OJ3UJ2S/)
* >500gb SSD
 * [Purse.io/Pay With Crypto: 512GB SSD](https://purse.io/product/B07997QV4Z)

## Get THE Blockchain
1. Download

## Initial Installation

1. Install Linux or boot from a Linux usb-key.
1. Create Balena.io account, the free tier should be fine.
1. Once inside dashboard.balena-cloud.com, click "Create Application". 
	1. ![Create Application](https://i.imgur.com/HIi6NsY.png)
	1. ![Create Application2](https://i.imgur.com/yV7NvfK.png)
1. Now you are ready to create a new device and download the image, click "Add Device".
	1. ![Add Device](https://i.imgur.com/yiTAGVH.png)
	1. Click "Download BalenaOS" and download and decompress image.
1. Download Balena Etcher in order to burn images to MicroSD cards.
1. Follow the steps to burn the MicroSD card using Etcher, you'll probably need a MicroSD to SD or MicroSD to USB adapter.


## Device Configuration
1. Navigate to your device visible on the Balena Dashboard. ![Dashboard](https://i.imgur.com/ZubjE8L.png)
1. Select the "Device Service Variables" tab, these are environment variables for a given device. 
1. Create environment variables like in the picture, be sure to use proper names that match the release images. ![Environment](https://i.imgur.com/c4pQVYp.png)
1. Place your ~>500gb SSD into its enclosure and connect it to your linux machines usb port.
	1. Use ```ls /dev/sd*``` before and after plugging in the drive, in order to determine which device is the one you plugged in.
1. Obtain the UUID of the drive, this will be used to mount the blockchain and LND data directories stored on this device.
	1. Use the target drive letter here: ```sudo blkid /dev/sda```
1. Make a fork of this repo, and clone it to your machine.
	1. Note: You need to fork it since Balena uses a build pattern of adding a new remote and then you push up your image with ```git push balena master```


## Aliases

Useful alias' for using the node:
### User Machine
This uses the balena cli to ssh to your node from anywhere in the world.
* alias "nodroid"="balena ssh {{uuid}}"

### Node
This is a handy alias for using litecoin
* alias "lncli"="lncli --chain=litecoin"

This project is still very early, and without much knowledge could be too much for beginners. However when it is completed my hope is this can compete with many of the other node launcher tools, and be one of the easiest ways to start a node. Looking for feedback!