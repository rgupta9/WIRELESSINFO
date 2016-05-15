#! /usr/bin/python

# This work is licensed under the GNU General Public License v3.0
#
# Dependencies pexpect (Python Expect).

import pexpect
import pickle
from time import sleep

# Please place your seed device in the to_crawl list.
# modify the to_crawl list. i.e. to_crawl = ['yourrouter1']

user = raw_input('Username? ')
passwd = raw_input('Password? ')
globalswitch_ip = raw_input('Wireless Controller? ')


def apdump(switch_ip,switch_un,switch_pw):
	
#	cdpout = [switch_ip]
	child = pexpect.spawn('telnet %s' % (switch_ip))
	child.logfile = open("./mylog", "w")
	loginresult = child.expect(['[Uu]ser'])
	child.timeout = 10
	if loginresult == 0:
		child.sendline(switch_un)
		child.expect('[Pp]assword:')
		child.sendline(switch_pw)
               	child.expect('>')
               	child.sendline('config paging disable')
              	child.expect('>')
		child.sendline('show ap summary')
		child.expect('>')
               	child.logfile.close()
	else:
		exit

	routerFile = open('./mylog', 'r')
	datalist = routerFile.read()
	routerFile.close()
	return datalist

logstring = apdump(globalswitch_ip,user,passwd)
loglist = logstring.split()

aplist = []
for count,i in enumerate(loglist):
	if 'AIR-' in i:
		aplist.append(loglist[count - 2])

child = pexpect.spawn('telnet %s' % (globalswitch_ip))
# child.logfile = open("./aplog", "w")
child.expect(['[Uu]ser'])
child.sendline(user)
child.expect('[Pp]assword:')
child.sendline(passwd)
child.expect('>')
child.timeout = 10
aplargelist = []
while aplist:
	child.logfile = open("./aplog", "w")
	aptarget = aplist.pop()
	child.sendline('config paging disable')
	child.expect('>')
	child.sendline('show ap config general %s' % (aptarget))
	child.expect('>')
        child.sendline('show ap cdp neighbors ap-name %s' % (aptarget))
        child.expect('>')
	child.logfile.close()

        APFile = open('./aplog', 'r')
        apdatalist = APFile.read()
        APFile.close()
        apdatalistSPLIT = apdatalist.split()
	
	apoutlist = []
	apout = open('./apout.txt', 'w')
	for count,i in enumerate(apdatalistSPLIT):
		if ('Cisco' in i and 'AP' in apdatalistSPLIT[count + 1] and 'Name' in apdatalistSPLIT[count + 2]):
			apoutlist.append(apdatalistSPLIT[count + 3])
		if ('assigned' in i and 'IP' in apdatalistSPLIT[count + 1] and 'Address' in apdatalistSPLIT[count + 2]):
			apoutlist.append('STATIC')
			apoutlist.append(apdatalistSPLIT[count + 3])
                if ('DHCP' in i and 'IP' in apdatalistSPLIT[count + 1] and 'Address' in apdatalistSPLIT[count + 2]):
			apoutlist.append('DHCP')
                        apoutlist.append(apdatalistSPLIT[count + 3])



                if ('MAC' in i and 'Address' in apdatalistSPLIT[count + 1]):
                        apoutlist.append('MAC')
                        apoutlist.append(apdatalistSPLIT[count + 2])

                if ('Cisco' in i and 'AP' in apdatalistSPLIT[count + 1] and 'Group' in apdatalistSPLIT[count + 2] and 'Name' in apdatalistSPLIT[count + 3]):
                        apoutlist.append('AP GROUP')
                        apoutlist.append(apdatalistSPLIT[count + 4])


		if ('Primary' in i and 'Cisco' in apdatalistSPLIT[count + 1] and 'Switch' in apdatalistSPLIT[count + 2] and 'Name' in apdatalistSPLIT[count + 3]):
			apoutlist.append('PRIMARY')
			apoutlist.append(apdatalistSPLIT[count + 4])
                if ('Secondary' in i and 'Cisco' in apdatalistSPLIT[count + 1] and 'Switch' in apdatalistSPLIT[count + 2] and 'Name' in apdatalistSPLIT[count + 3]):
			apoutlist.append('SECONDARY')
                        apoutlist.append(apdatalistSPLIT[count + 4])
                if ('Tertiary' in i and 'Cisco' in apdatalistSPLIT[count + 1] and 'Switch' in apdatalistSPLIT[count + 2] and 'Name' in apdatalistSPLIT[count + 3]):
                        apoutlist.append('TERTIARY')
                        apoutlist.append(apdatalistSPLIT[count + 4])


                if ('Neighbor' in i and 'Name' in apdatalistSPLIT[count + 1]):
                        apoutlist.append('CONNECTED TO')
			try:
                       		apoutlist.append(apdatalistSPLIT[count + 10])
				apoutlist.append(apdatalistSPLIT[count + 11])
			except IndexError:
				apoutlist.append('ERROR')
				apoutlist.append('ERROR')	
				


#	for item in apoutlist:
#		apout.write(item)
#		apout.write(",")
#		apout.write("\n")
#	apout.write(apoutlist)
#	pickle.dump(apoutlist, apout)
#	apout.write("\n".join(apoutlist))
	aplargelist.append(apoutlist)

#	print apoutlist
	print aplargelist

for item in aplargelist:
	print >> apout, item


			
			

	
#	for count,i in enumerate(apdatalistSPLIT):
#		print count,i
#	sleep(1)

