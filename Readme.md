# Raspberry Pi based time-lapse camera

> The tool is originally developed on the raspberry Pi, aiming at observing of tiny aquatic animal (gammarus) and save the result as video recording recurring
> 
> The whole project is based on PyQt5 and utilize bash command execute directly to complete recording.



## Table of Contents

- [Requirement](#requirement)
- [Install](#install)
- [Usage](#usage)
- [Version History](#VersionHistory)




## Requirement

#### Software

> Raspberry Pi OS Bullseye (with desktop), Later than 2023-02

#### Hardware

> 1. Raspberry Pi 4B
> 
> 2. RaspCamera v3 NoIR

## Install

```sh
cd ~
git clone https://github.com/VancomycinHCl/camera_app_2.git
```

## Usage

It is recommended to run the script under the remote desktop when a physical screen is unavailable. To start the remote desktop, run the following command.
```sh
vncserver
```
Then you can loging into the desktop as local PC by software vncviewer.

To start the programme, execute the command below directly.
```sh
cd ~/camera_app
sudo chmod u+x ./run.sh
./run.sh
```

## Version History

* 0.2
    * Various bug fixes, especially in colorful log generator
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release
    * Add timetable function, so that users can set record event freely.

## Contributor

* VancomycinHCl - 2112484232@qq.com