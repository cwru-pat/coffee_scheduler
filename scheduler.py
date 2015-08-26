from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
from random import shuffle

def createSchedule(grads, postdocs, profs, firstyrs, talkweeks, cerca, dates, special):
	skeys=set(special.keys())
	g=list(set(grads)-skeys)
	pd=list(set(postdocs)-skeys)
	pr=list(set(profs)-skeys)
	shuffle(g)
	shuffle(pd)
	shuffle(pr)
	names=g+pd+pr
	names[len(talkweeks):]=[]
	shuffle(names)
	pat=dict.fromkeys(names,60)
	for person in names:
		if person in cerca:
 			pat[person]=cerca[person]

	talks={x:y for x,y in zip(names,talkweeks)}

	for person in names:
		if abs(pat[person]-talks[person])<=1:
			return 0
	else:
		print "Gradstudents not talking: "
		talks.update(special)
		print list(set(grads)-set(talks.keys()))
		schedule=sorted(talks.items(), key=lambda x:x[1])
		for idx,line in enumerate(schedule):
			print dates[idx]+' '+line[0]
		return 1


soup=BeautifulSoup(urlopen('http://cerca.case.edu/pizza.php'),"html.parser")
htmltable=soup.find('table')
#headers= [header.text for header in htmltable.find_all('th')][:-1]

people=[[cell.text.encode('ascii','ignore') for cell in row.find_all('span')] for row in htmltable.find_all('tr')[1:]]

dates=[row.td.contents[0].encode('ascii','ignore').split() for row in htmltable.find_all('tr')[1:]]
dates=zip(*dates)
dates[1]=[filter(str.isdigit,s) for s in dates[1]]
dates=zip(*dates)

dates=[datetime.strptime(" ".join(date),'%b %d %Y').isocalendar()[1] for date in dates] 
cerca={}

cerca={name:entry[0] for entry in zip(dates,people) for name in entry[1] }

grads=[]
postdocs=[]
profs=[]
firstyrs=[]
special={}

for line in open('patgroup.txt'):
	if line.split(',')[0]=='3':
		grads.append(line.split(',')[1].strip())
	elif line.split(',')[0]=='2':
		postdocs.append(line.split(',')[1].strip())
	elif line.split(',')[0]=='1':
		profs.append(line.split(',')[1].strip())
	elif line.split(',')[0]=='0':
		firstyrs.append(line.split(',')[1].strip())
	elif line.strip()=="":
		continue
	else:
		print "Unknown input: "+line

dates=[datetime.strptime(line.strip(),"%Y-%m-%d").strftime("%m/%d/%Y") for line in open('dates.txt')]
talkweeks=[datetime.strptime(line.strip(),"%m/%d/%Y").isocalendar()[1] for line in dates]

for line in open('special.txt'):
	special[line.split(',')[1].strip()] = datetime.strptime(line.split(',')[0],'%Y-%m-%d').isocalendar()[1]
	dates.append(datetime.strptime(line.split(',')[0],'%Y-%m-%d').strftime("%m/%d/%Y"))

dates.sort()



for i in range(100):
	if createSchedule(grads,postdocs,profs,firstyrs,talkweeks,cerca,dates,special)==1:
		break
else:
	print "Tried to schedule 100 times no solution found."
