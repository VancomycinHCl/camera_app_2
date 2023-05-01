# Raspberry Pi based time-lapse camera

> The tool is originally developed on the raspberry Pi, aiming at observing of tiny aquatic animal (gammarus) and save the result as video recording recurring
> 
> The whole project is based on PyQt5 and utilize bash command execute directly to complete recording.



## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [License](#license)


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



## License

[MIT](LICENSE) © Richard Littauer