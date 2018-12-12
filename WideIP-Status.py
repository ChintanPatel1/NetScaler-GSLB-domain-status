#------------------------------
# Name:        GSLB WIP Status
# Purpose:     This Python3 script will fetch the Wide-IP (domain) and check its status against the prod vserver and its backup vservers. The input files to this script should be the output of 'sh run | grep domainName' and the output of 'sh gslb vserver' commands ran on the NetScaler GSLB. The output file will be a .csv file containing the name "WideIP_Status" appened with current datetime.
#
# Author:      CHINTAN PATEL
#------------------------------

#!/usr/bin/env python
import sys, csv, os, time, datetime

# Open files

vs_wip_file = input("Enter the file name that contans output of 'sh run | grep domainName': ")
try:
    my_file1=open(vs_wip_file)
except:
    print('File not found! Please try again')
    sys.exit(1)
	
vs_file = input("Enter the file name that contains output of 'sh gslb vserver': ")
try:
    my_file2=open(vs_file)
except:
    print('File not found! Please try again')
    sys.exit(1)
	
print('Please wait..')

# Send prod vserver and corrosponding WIP from my_file1 to a list.
vs_wip_list = []
for line1 in my_file1:
    line1=line1.strip()
    line1=line1.split()
    if len(line1) != 8:
        continue
    vs = line1[3]
    wip = line1[5]
    vs_wip_list.append([vs, wip])

# Send vserver, status and backup vserver from my_file2 to second list.

vs_status_list = []
cc = -1
for line2 in my_file2:
    line2 = line2.strip()
    line2 = line2.split()
    if len(line2) == 0:
        continue
    elif (len(line2) == 6 and line2[4] == 'State:'):
        vs_status_list.append([line2[1], line2[5]])
        cc = cc+1
    elif (line2[0] == 'Backup:'):
        vs_status_list[cc].append(line2[0])
        vs_status_list[cc].append(line2[1])

my_file2.close()
my_file1.close()

# Define a function to return the status of a vservers and its backup-vserver from vs_status_list.

def prod_vs_status(x):
    i=0
    value = ""
    while i < len(vs_status_list):
        first_vserver = vs_status_list[i][0]
        if x == first_vserver:
            value = True
        else:
            value = False

        if value == True and len(vs_status_list[i]) == 2:
            return [vs_status_list[i][1], 'NA']
            break
        elif value == True and len(vs_status_list[i]) == 4:
            return [vs_status_list[i][1], vs_status_list[i][3]]
        else:
            i=i+1

# Fetch the prod vserver values from vs_wip_list and send it to def prod_vs_status(x) to get the final vserver (backup of backup and so on) status.

currentdatetime = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
mycsvfile = "WideIP_Status-" + currentdatetime + ".csv"
print('Sending data to csv file...')
with open (mycsvfile, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['WideIP', 'Status'])

    z=0
    while z < len(vs_wip_list):
        prod_vs = vs_wip_list[z][0]
        status = prod_vs_status(prod_vs)
		
        if status[0] == 'UP':
            writer.writerow([vs_wip_list[z][1], 'UP'])
            z = z+1
			
        elif status[0] == 'DOWN' and status[1] == 'NA':
            writer.writerow([vs_wip_list[z][1], 'DOWN'])
            z = z+1
			
        else:
            cob_cob = status[1]
            while cob_cob != 'NA':
                status1 = prod_vs_status(cob_cob)
                cob_cob = status1[1]
                final_status = status1[0]
            if final_status == 'UP':
                writer.writerow([vs_wip_list[z][1], 'UP'])
            else:
                writer.writerow([vs_wip_list[z][1], 'DOWN'])
            z = z+1
csvFile.close()
print('\nDONE!\nPlease check the "WideIP_Status...csv" file.')