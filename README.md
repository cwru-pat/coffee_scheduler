# coffee_scheduler

This repo contains a python(2.7) script and support files which creates a coffee talk schedule and checks against the CERCA talks schedule to ensure no one talks twice within a 1 weeks period. 

- "scheduler.py" is the python script which assigns talk dates randomly and checks against CERCA. The script outputs to stdout a list of grad-students not talking, and a list in date order format of "%m/%d/%Y Name\n" of the talks. The required libraries are:
  - urllib2- To open the CERCA page
  - bs4 (BeautifulSoup4)- a scrapper to read the CERCA page
  - datetime- to interpret dates
  - random- to randomize the talk schedule.
- "special.txt" contains dates and names for people who should give a talk on a particular date. The format of each line of the file should be "%Y-%m-%d Name\n"
- "dates.txt" contains a list of dates on which the coffee talks should occur (excluding those in "special.txt"). Each line should be of the format "%Y-%m-%d\n".
- "patgroup.txt" contains a list of the members of the PAT group. Each line should be of the format "%int, Name\n". The integer determines the status of the person:
    0- first year,
    1- professor,
    2- post doc,
    3- grad-student.
