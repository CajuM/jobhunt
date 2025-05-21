#!/bin/sh

# Renew DHCP lease from ISP
nmcli connection down Digi &>/dev/null
nmcli connection up Digi &>/dev/null

sleep 1

while ! ip -4 route 2>&1 | grep ^default &>/dev/null; do :; done
