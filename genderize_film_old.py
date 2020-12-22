from bs4 import BeautifulSoup
from genderize import Genderize
import re
import time
import requests

def get_gender_from_wikidata(crew):
    imdbs = list(crew.keys())

    url = "https://query.wikidata.org/sparql"

    start = 0
    stop = 199

    while(start<=len(imdbs)+1):

        #print("start: "+str(start)+", stop: "+str(stop))

        imdb_string = ''

        for imdb in imdbs[start:stop:1]:
            imdb_string = imdb_string + '"'+str(imdb)+'"'

        query = """
        SELECT
          ?imdb ?genderLabel
        WHERE {
          VALUES ?imdb {"""+imdb_string+"""}
          ?person wdt:P345 ?imdb; wdt:P21 ?gender
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """

        #print(query)

        r = requests.get(url, params={'query' : query}, headers={'Accept' : 'application/sparql-results+json'})
        #print(r)
        resultsList = r.json()['results']['bindings']
        #print(resultsList)

        for result in resultsList:
            #print(result['imdb']['value'] + ', ' + result['genderLabel']['value'])
            crew[result['imdb']['value']]['gender'] = result['genderLabel']['value']
            crew[result['imdb']['value']]['gender_probability'] = 'NA'
            crew[result['imdb']['value']]['source'] = 'wikidata'
        
        start = start + 200
        stop = min(stop + 200, len(imdbs)+1)
        time.sleep(5)
    with open('crew_gender_' + film_title + '.csv','a', encoding="utf-8") as file:
        for crew_member in [crew_member for crew_member in crew.values() if 'source' in crew_member.keys() and crew_member['source'] == 'wikidata']:
            print(crew_member['imdb']+","+crew_member['name']+','+crew_member['given_name']+","+str(crew_member['categories'])+","+crew_member['gender']+","+crew_member['gender_probability']+","+crew_member['source'])
            file.write(crew_member['imdb']+","+crew_member['name']+','+crew_member['given_name']+',"'+str(crew_member['categories'])+'",'+crew_member['gender']+","+crew_member['gender_probability']+","+crew_member['source']+"\n")    

def get_gender_from_imdb(ungendered_imdbs):
    file = open('name.basics.tsv','r', encoding="utf-8")

    for line in file:
        info = line.split('\t')
        if(info[0] in ungendered_imdbs):
            if("actor" in info[4]):
                #print(info[0]+": male")
                crew[info[0]]['gender']='male'
                crew[info[0]]['gender_probability'] = 'NA'
                crew[info[0]]['source'] = 'imdb names.basic.tsv'
            if("actress" in info[4]):
                #print(info[0]+": female")
                crew[info[0]]['gender']='female'
                crew[info[0]]['gender_probability'] = 'NA'
                crew[info[0]]['source'] = 'imdb names.basic.tsv'
            ungendered_imdbs.remove(info[0])
    file.close()

    with open('crew_gender_' + film_title + '.csv','a', encoding="utf-8") as file:
        for crew_member in [crew_member for crew_member in crew.values() if 'source' in crew_member.keys() and crew_member['source'] == 'imdb names.basic.tsv']:
            print(crew_member['imdb']+","+crew_member['name']+','+crew_member['given_name']+','+str(crew_member['categories'])+','+crew_member['gender']+","+crew_member['gender_probability']+","+crew_member['source'])
            file.write(crew_member['imdb']+","+crew_member['name']+','+crew_member['given_name']+',"'+str(crew_member['categories'])+'",'+crew_member['gender']+","+crew_member['gender_probability']+","+crew_member['source']+"\n")


def get_gender_from_given_name(ungendered_imdbs):
    names = {}
    for imdb in ungendered_imdbs:
        if imdb[0] not in names.keys():
            names[imdb[0]] = {}
            names[imdb[0]]['imdbs'] = []
        names[imdb[0]]['imdbs'].append(imdb[1])

    #print(names)
    
    #trying to get gender from name file
    try:
        with open('names_to_gender.csv','r',encoding="utf-8") as file:
            for line in file:
                info = line.split(',')
                if info[0] in names:
                    #print(info[0]+"("+info[1]+") is given name of "+str(names[info[0]]['imdbs']))
                    for imdb in names[info[0]]['imdbs']:
                        #print(imdb)
                        crew[imdb]['gender'] = info[1]
                        crew[imdb]['gender_probability'] = info[2]
                        crew[imdb]['source'] = 'Genderize.io'
                    del names[info[0]]
    except:
        print('names_to_gender file not found. No problem. Proceeding.')

    names_list = list(names.keys())

    start = 0
    stop = 9
    namesfile = open("names_to_gender.csv",'a',encoding="utf-8")
    while(start<len(names_list)):

        #print("Getting gender of names "+str(names_list[start:stop+1]))
        gendered_names = Genderize().get(names_list[start:stop+1])
        for name in gendered_names:
            #print(name['name'])
            namesfile.write(str(name['name'])+','+str(name['gender'])+','+str(name['probability'])+','+str(name['count'])+'\n')
            for imdb in names[name['name']]['imdbs']:
                #print(imdb)
                crew[imdb]['gender'] = name['gender']
                crew[imdb]['gender_probability'] = name['probability']
                crew[imdb]['source'] = 'Genderize.io'
        start = start + 10
        stop = min(stop + 10, len(names)+1)
        time.sleep(5)
    namesfile.close()

def get_crew_members_from_imdb(imdb):
    film_url = 'https://www.imdb.com/title/'+film_imdb+'/fullcredits'
    r = requests.get(url = film_url)
    soup = BeautifulSoup(r.text, 'html.parser')


    # if there is a file you like to use you need to remove the '#'
    # with open("Downloads/imdb_"+film_title+".html", encoding="utf-8") as fp:
    #    soup = BeautifulSoup(fp, 'html.parser')

    # Getting only the credit part of the page
    credits_head = soup.find(id = 'fullcredits_content')
    #print(credits_head.prettify)

    crew = {}
    category = ""
    for child in credits_head.children:
        if(child.name == 'h4'):
            category = BeautifulSoup(str(child),'html.parser').h4['id']
            #print(child)
        if(child.name == 'table' and category not in ['cast', 'thanks','miscellaneous','transportation_department','stunts']):
            rows = child.find_all('tr')
            for row in rows:
                link = BeautifulSoup(str(row), 'html.parser').a
                if(link != None):
                    id = str(link['href']).replace("/name/",'').replace("/?",'').strip("/")
                    id = re.sub(r'ref_=(.+)','',id)
                    if(id not in crew.keys()):
                        crew[id] = {}
                    if('categories' not in crew[id].keys()):
                        crew[id]['categories'] = {category}
                    crew[id]['categories'].add(category)
                    name = link.string.replace('\n','').strip()
                    crew[id]['name'] = name
                    crew[id]['imdb'] = id
                    crew[id]['given_name'] = re.sub(r' .+','',name)
                    print(crew[id])

    print('number of crew members: ' + str(len(crew)))
    return crew

#prompting for title and imdb
film_title = str(input("Please enter the title of the film: ")).lower().replace(' ','_')
film_imdb = str(input("Please enter the imdb Id of the film (e.g. tt0059229): "))

#creating csv to store the information
with open('crew_gender_' + film_title + '.csv','a', encoding="utf-8") as file:
    file.write('imdb,name,given_name,departments,gender,gender_probability,source\n')

#getting crew members from imdb
print()
print("========GETTING CREW MEMBERS FROM IMDB========")
crew = get_crew_members_from_imdb(film_imdb)
print()


#trying to get gender from sparql
print("========TRYING TO GET GENDER FROM WIKIDATA========")
get_gender_from_wikidata(crew)
print()

print("========TRYING TO GET GENDER FROM IMDB'S NAME.BASICS.TSV========")
#trying to get gender from actor/actress information in names.basics
ungendered_imdbs = [person['imdb'] for person in crew.values() if 'gender' not in person.keys()]
ungendered_imdbs.sort() 
try:
    get_gender_from_imdb(ungendered_imdbs)
except:
    print('imdbs names.basics.tsv not found. Proceeding')
print()

#trying to derive gender by name
ungendered_imdbs = [(person['given_name'],person['imdb']) for person in crew.values() if 'gender' not in person.keys()]
ungendered_imdbs.sort()
print("========TRYING TO DERIVE GENDER FROM GIVEN NAME VIA GENDERIZE.IO========")
get_gender_from_given_name(ungendered_imdbs)
print()

with open('crew_gender_' + film_title + '.csv','a', encoding="utf-8") as file:
    for crew_member in [crew_member for crew_member in crew.values() if 'source' in crew_member.keys() and crew_member['source'] == 'Genderize.io']:
        print(crew_member['imdb']+","+crew_member['name']+','+crew_member['given_name']+","+str(crew_member['categories'])+","+str(crew_member['gender'])+","+str(crew_member['gender_probability'])+","+crew_member['source'])
        file.write(str(crew_member['imdb'])+","+str(crew_member['name'])+','+str(crew_member['given_name'])+',"'+str(crew_member['categories'])+'",'+str(crew_member['gender'])+","+str(crew_member['gender_probability'])+","+str(crew_member['source'])+"\n")

gender_count = {'female':0,'male':0,'unsure':0}

for imdb in [imdb for imdb in crew.keys() if 'gender_probability' in crew[imdb].keys()]:
    if crew[imdb]['gender_probability'] == 'NA' or (crew[imdb]['gender_probability'] != 'NA' and float(crew[imdb]['gender_probability'])>=0.9):
        gender_count[crew[imdb]['gender']] += 1
    else:
        gender_count['unsure'] += 1

print()
print("BREAKDOWN OF THE RESULTS: ")

print('male count: '+str(gender_count['male'])+', male ratio: '+str(gender_count['male']/len(crew)))
print('female count: '+str(gender_count['female'])+', female ratio: '+str(gender_count['female']/len(crew)))
print('unsure count: '+str(gender_count['unsure'])+', unsure ratio: '+str(gender_count['unsure']/len(crew)))
print()
print("Genderize.io's gender attribution was only accepted when its probability was at least 90%. Otherwise it was counted towards 'unsure'.  You can find an overview about all crew members and their (probable) gender in the file crew_gender_"+film_title+".csv.")
