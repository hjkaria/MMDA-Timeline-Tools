# Convert google doc spreadsheet format for timelinejs to json file
# useful if you want to experiment using google doc but eventually
# host everything yourself privately.

# Example: go to google docs spreadsheet and do File -> Download As -> CSV (Comma Separated Values)
# save as timeline.csv, run this, you get a timeline.json out
#
# Or look at your google doc ID long string like for example 1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo
# wget -qO timeline.csv 'https://docs.google.com/spreadsheets/d/1xTn9OSdmnxbBtQcKxZYV-xXkKoOpPSu6AUT0LXXszHo/pub?ou tput=csv'

import csv
import json

csvfile = open('demo.csv','r')
outfile = open('lifeEvents.json','w')
reader = csv.DictReader(csvfile)

data = {}

life_events = []
events = []

data['life_events']=life_events
data['events']=events

# Didn't support 'End Time': '', 'Time': ''

keymap = {'Media': 'media|url', 'Media Caption': 'media|caption', 'Media Thumbnail': 'media|thumbnail',
          'Media Credit': 'media|credit',
          'Month': 'start_date|month', 'Day': 'start_date|day', 'Year': 'start_date|year',
          'End Month': 'end_date|month', 'End Day': 'end_date|day', 'End Year': 'end_date|year',
          'Headline': 'text|headline', 'Text': 'text|text',
          'Group': 'group', 'Display Date': 'display_date'}

for row in reader:
    event = {}
    life_event = {}
    for a in keymap:
        if row[a]:
            if '|' in keymap[a]:
                (x,y)=keymap[a].split("|")
                if not x in event: event[x]={}
                event[x][y] = row[a]
            else:
                event[keymap[a]] = row[a]

    # if row['Background']:
    #     event['background'] = {}
    #     if row['Background'].startswith("#"):
    #         event['background']['color']=row['Background']
    #     else:
    #         event['background']['url']=row['Background']

    if (row['Life Event'] == 'true'):
        data['life_event']=event

    else:
        events.append(event)

json.dump(data,outfile, sort_keys=True,indent=4)
