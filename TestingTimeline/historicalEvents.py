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
outfile = open('historicalEvents.json','w')
reader = csv.DictReader(csvfile)

data = {}

history_events = []
events = []

data['history_events']=history_events
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
    history_event = {}
    publication = {}
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

    if (row['Historical Event'] == 'true'):
        data['historical_event']=event
    #
    # if (row['Type'] == 'title'):
    #     data['title']=event


    # else if (row['Type'] == 'publication'):
    #     data['publication']=event
    # else if (row['Type'] == 'history'):
    #     data['history']=event
    # else if (row['Type'] == 'life'):
    #     data['life']=event
    else:
        events.append(event)

json.dump(data,outfile, sort_keys=True,indent=4)
