# wan-ranger
This tool was build to make IP-host discovery faster
it is using multiprocessing to create multiple threads to check all 254 Hosts of any /24 Network at once. It is also capable of checking a /16 Network for all available hosts.

# how to use

python3 wanranger.py VAR1 VAR2

VAR1 --> The IP-Range you want to scan (for /24 -> 192.168.1.0 | for /16 ->192.168.0.0)
VAR2 --> yes/no for saving the output of the scans to a file in the same directory.

-- The Program currently sees a 0 as HOSTS so if you would want to scan the Network 192.168.0.0/24 You just need to CTRL + C the scan after its done with the first one. 

# requirements

The project tries to install the required packages itself.
If this doesn't work then you need to install multiprocessing & termcolor manually using pip
