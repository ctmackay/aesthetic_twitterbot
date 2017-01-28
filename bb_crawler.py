# Body Building web scraper
# Charles MacKay
# input: body building website
# output: .txt file of every exercise instruction on their website,
# broken up into muscle group, and exercise step. 

from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
import re
import pprint

muscleNameList = []
filteredMusGroup = []
workout_dict = dict()
exercise_dict = dict()

def write_a_dict(filename,my_d):
    i=1
    titles_filename = filename + "_titles.txt"
    ft = open(titles_filename,'a')
    for k in my_d:
        ft.write(k.strip()+'\n')
        for v in my_d[k]:
            fn = filename + str(i) +".txt"
            with open(fn,'a') as f:
                vv = v.encode('ascii','ignore')
                f.write(vv+'\n')
            i=i+1
            if i > 4:
                i=4
    ft.close()
            
def print_a_dict(my_d):
    for k in my_d:
        print (k)
        for v in my_d[k]:
            print (v)
            
def extract_exercise_contents(url):
    k = dict()
    l=[]
    html = urlopen(url)
    bsObj = BeautifulSoup(html,"html.parser")
    workoutName = bsObj.find("div",{"id":"exerciseDetails"}).h1.get_text()
    routine = bsObj.find("div",{"class":"guideContent"})
    results =  routine.findAll("li")
    for r in results:
        l.append(r.get_text())
    k[workoutName] = l
    return k


#extract all the exercise urls on the page
def find_exercises(url):
    filteredExList = []
    html = urlopen(url)
    bsObj = BeautifulSoup(html,"html.parser")
    for link in bsObj.find("div",{"id":"listResults"}).findAll("a",href=re.compile("\/exercises\/detail\/view")):
        if 'href' in link.attrs:
            x= link.attrs['href']
            if x not in filteredExList:
                filteredExList.append(x)
    return filteredExList


#start here
bburl='http://www.bodybuilding.com/exercises/list/muscle/selected/abdominals'
html = urlopen(bburl)
bsObj = BeautifulSoup(html,"html.parser")

print "finding a list of muscle groups..."
#find all the muscle group URLs
#build a list of muscles url sub pages
for link in bsObj.find("ul",{"class":"muscle-pagination"}).findAll("a",href=re.compile("\/exercises\/list\/muscle")):
    muscleGroupName = link.get_text()
    muscleNameList.append(muscleGroupName)
    if 'href' in link.attrs:
        link_url = link.attrs['href']
        if link_url not in filteredMusGroup:
            workout_dict[muscleGroupName] = 'http://www.bodybuilding.com'+link_url

print "finding a list of exercises for each muscle..."
#build a dictionary of all exercises based on muscle
for muscle in workout_dict.keys():
    print muscle,
    my_list = find_exercises(workout_dict[muscle])
    exercise_dict[muscle] = my_list
    print "...done"

#pprint.pprint(exercise_dict)    
print "learning each exercise"
#go through each muscle group, and each exercise, and print the description to a file

for muscle in workout_dict.keys():
    print "learning: %d exercises for %s"%(len(exercise_dict[muscle]),muscle)
    for url_value in exercise_dict[muscle]:
        #print muscle
        print url_value
        exercise_detail = extract_exercise_contents(url_value)
        #print_a_dict(exercise_detail)
        write_a_dict(muscle,exercise_detail)
print "program complete!"
