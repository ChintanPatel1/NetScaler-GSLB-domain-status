# NetScaler-GSLB-domain-status
# Citrix-NetScaler GSLB domin (Wide-IP) Status

#!/usr/bin/env python
import sys
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
# Send prod vserver and corrosponding WIP from my_file1 to a list
vs_wip_list = []
for line1 in my_file1:
    line1=line1.strip()
    line1=line1.split()
    if len(line1) != 8:
        continue
    vs = line1[3]
    wip = line1[5]
    vs_wip_list.append([vs, wip])
#print(vs_wip_list)

# Send vserver, status and backup vserver from my_file2 to second list

vs_status_list = []
cc = -1
for line2 in my_file2:
    line2 = line2.strip()
    line2 = line2.split()
    if (len(line2) == 6 and line2[4] == 'State:'):
#        vs_status_list.append([])
        vs_status_list.append([line2[1], line2[5]])
        cc = cc+1
    elif (line2[0] == 'Backup:'):
        vs_status_list[cc].append(line2[0])
        vs_status_list[cc].append(line2[1])
    else:
        continue
#print(vs_status_list)
my_file2.close()
my_file1.close()

# Define a function

def prod_vs_status(x):
    i=0
    while i < len(vs_status_list):
        value = x in vs_status_list[i][0]
#        print(value)
        if value == True and len(vs_status_list[i]) == 2:
            return [vs_status_list[i][1], 'NA']     # retuen vserver status and no backup vserver
            break
        elif value == True and len(vs_status_list[i]) == 4:
            return [vs_status_list[i][1], vs_status_list[i][3]]     # return vserver status and the backup vserver
        else:
            i=i+1

# Fetch the prod vserver values from vs_wip_list and send it to def prod_vs_status(x) to get the final vserver (backup of backup and so on) status

WIP_STATUS = []      # create an empty list to store WIP and its status
z=0
while z < len(vs_wip_list):
    prod_vs = vs_wip_list[z][0]
    status = prod_vs_status(prod_vs)
    if status[0] == 'UP':
        WIP_STATUS.append([vs_wip_list[z][1], 'UP'])
        z = z+1
    elif status[0] == 'DOWN' and status[1] == 'NA':
        WIP_STATUS.append([vs_wip_list[z][1], 'DOWN'])
        z = z+1
    else:
        cob_cob = status[1]
        while cob_cob != 'NA':
            status1 = prod_vs_status(cob_cob)
            cob_cob = status1[1]
            final_status = status1[0]
        if final_status == 'UP':
            WIP_STATUS.append([vs_wip_list[z][1], 'UP'])
        else:
            WIP_STATUS.append([vs_wip_list[z][1], 'DOWN'])
        z =z+1

print(WIP_STATUS)
