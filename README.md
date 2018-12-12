This Python3 script will fetch the Wide-IPs (domains) and check its status against the prod vserver and its backup vservers. If any of the vserver bound to the WideIP is UP, the script will mark that WIP as UP. If all the vservers bound to a WIP is DOWN, then the script will mark that WIP as DOWN.

Run below commands on the NetScaler GSLB load balancer and save the output on two separate files.
sh run | grep domainName
sh gslb vserver

The input files to this script should be the output of 'sh run | grep domainName' and the output of 'sh gslb vserver' commands that we ran on the NetScaler GSLB.

The output file will be a .csv file containing the WideIPs (domains) and its status (UP/DOWN).
The output filename will start with the word "WideIP_Status" appened with current datetime.
