# PCI Device library

Get device info + read from /dev/mem accordingly for the device MMIO memory allocation.

This project has intention to develop the right tools to develop many of the necessary stuff
from BCM43XX devices.

Library won't work for any other type of devices (PCIe, ...) only for PCI, as are the Network
devices from the Broadcom BCM43XX chipsets.

## Contributing

Right now I don't have the intention of accepting PRs from outside the people working in this project. (Me and my professors for the moment I guess 😬).

If anything, feel free to contact me.

## Contact Point

Albert Sáez <[albert.saez.nunez@estudiantat.upc.edu](mailto:albert.saez.nunez@estudiantat.upc.edu)>

## Compatibility

```
WARNING: This library only works for Unix(-ish) and Linux devices AND HAVE NO INTENTION OF MAKE IT WORK FOR OTHER YPE OF SYSTEMS
```

	* Tested on Python3.10.8 and Python3.9.2, so I guess anything +3.7.
	* Tested for Debian distributions (11 bullseye amd64).


I don't see the relevancy of this compatibility issues, however they are here as a warning. Feel free to try it in other environments and PR if you feel like it.

## Licensing

[MIT licensed](./LICENSE)
