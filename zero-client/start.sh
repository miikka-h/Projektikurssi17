
#!/bin/bash -eu

# Bash options:
# "-e" - exit the script if some command fails.
# "-u" - exit the script if uninitialized variable is used.

# TODO: Check that script is running as root.

# Kernel module configuration is based on tutorial in the Linux kernel documentation.
# https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt

cd /

export CONFIGFS_HOME="/configfs_dir"

if [[ ! -d "$CONFIGFS_HOME" ]] ; then
    mkdir "$CONFIGFS_HOME"
fi

modprobe libcomposite
mount none $CONFIGFS_HOME -t configfs

mkdir $CONFIGFS_HOME/usb_gadget/g1

cd $CONFIGFS_HOME/usb_gadget/g1

echo 0x5 > idVendor
echo 0x5 > idProduct

mkdir strings/0x409

echo 12345 > strings/0x409/serialnumber
echo "some_manufacturer" > strings/0x409/manufacturer
echo "USB multi-device" > strings/0x409/product

# Create configuration

mkdir configs/c.1

mkdir configs/c.1/strings/0x409

echo test_configuration > configs/c.1/strings/0x409/configuration


# Setup hid usb function, with keyboard settings

mkdir functions/hid.usb0

# report_lenght depends from USB HID Description
echo 8 > functions/hid.usb0/report_length

echo 1 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass

cd functions/hid.usb0

# TODO: Copy hid description bytes from this script or set python script
#       file path to variable.
python3 /copy-usb-hid-description.py

cd ../..

ln -s functions/hid.usb0 configs/c.1


if [[ "$#" = "1" && "$1" = "--enable-usb-ethernet-gadget" ]] ; then
    # Setup ethernet usb function

    mkdir functions/ecm.usb0

    # Set MAC addresses because otherwise they would be random
    echo 16:c4:b2:24:c0:03 > functions/ecm.usb0/dev_addr
    echo fa:4d:9e:fa:5a:d6 > functions/ecm.usb0/host_addr

    ln -s functions/ecm.usb0 configs/c.1
fi


# Start usb gadget mode

echo 20980000.usb > UDC


# Start Raspberry Pi Zero keyboard client.
cd /
python3 zero-client.py "192.168.0.1" "25001"