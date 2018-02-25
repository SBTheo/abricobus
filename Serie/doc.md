# Liaison série arduino - RPi

# Pinout :
[RPi Pinout](https://fr.pinout.xyz/)

| RPi | Arduino |
| :-: | :-----: |
| TXD (8) | RXD |
| RXD (10) | TXD |
| GND (6) | GND |

# Code :

* [RPi : serialtest.py](./serialtest.py)
* [Arduino : scrolltext_16x32](../scrolltext_16x32.ino)

# RPi modification

## `/boot/config.txt`

Add :
```
dtoberlay=pi3-disable-bt
enable_uart=1
```

## `/boot/cmdline.txt`
Change :
```
console=tty1
```