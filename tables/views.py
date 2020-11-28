from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify
from datetime import datetime
from fixtures.models import site_views

def tables(request):
    site = site_views.objects.get(pk='tables')
    site.page_views += 1
    site.save()
    leaguedict = {
        'Spanish Primera División':'esp.1',
        'French Ligue 1':'fra.1',
        'English Premier League':'eng.1',
        'UEFA Champions League':'uefa.champions',
        'Italian Serie A':'ita.1',
        'German Bundesliga':'ger.1',
        'UEFA Europa League':'uefa.europa',
        'UEFA European Championship Qualifying':'uefa.euroq',
        'UEFA Nations League':'uefa.nations',
        'International Friendly':'fifa.friendly',
        'FIFA World Cup Qualifying - CONMEBOL':'fifa.worldq.conmebol',
        'English League Championship':'eng.2',
        'Spanish Copa del Rey':'esp.copa_del_rey',
        'English FA Cup':'eng.fa',
        'Italian Coppa Italia':'ita.coppa_italia',
        'French Coupe de France':'fra.coupe_de_france',
        'German DFB Pokal':'ger.dfb_pokal',
        'FIFA World Cup':'fifa.world',
        'FIFA World Cup Qualifying - UEFA':'fifa.worldq.uefa',
        'FIFA World Cup Qualifying - CAF':'fifa.worldq.caf',
        'FIFA World Cup Qualifying - CONCACAF':'fifa.worldq.concacaf',
        'FIFA World Cup Qualifying - AFC':'fifa.worldq.afc',
        'FIFA World Cup Qualifying - OFC':'fifa.worldq.ofc',
        'FIFA Confederations Cup':'fifa.confederations',
        'FIFA Club World Cup':'fifa.cwc',
        'FIFA Under-20 World Cup':'fifa.world.u20',
        'UEFA European Championship':'uefa.euro',
        'Copa America':'conmebol.america',
    }
    allowedTitles = [
        'English Premier League',
        'Spanish Primera División',
        'UEFA Champions League',
        'French Ligue 1',
        'Italian Serie A',
        'German Bundesliga',
        'UEFA Europa League',
        'UEFA European Championship Qualifying',
        'UEFA Nations League',
        'FIFA World Cup Qualifying - CONMEBOL',
        'English League Championship',
        'FIFA World Cup',
        'FIFA World Cup Qualifying - UEFA',
        'FIFA World Cup Qualifying - CAF',
        'FIFA World Cup Qualifying - CONCACAF',
        'FIFA World Cup Qualifying - AFC',
        'FIFA World Cup Qualifying - OFC',
        'FIFA Confederations Cup',
        'FIFA Under-20 World Cup',
        'UEFA European Championship',
        'Copa America',
    ]
    try:
        league = request.GET['league']
    except:
        league = ''
    try:
        fdate = request.GET['date']
    except :
        fdate = ''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    if fdate is '' and league is '':
        link = 'https://www.espn.in/football/table/_/league/eng.1'
    elif league != '' and fdate == '':
        link = 'https://www.espn.in/football/table/_/league/'+leaguedict.get(league, '')
    else:
        todaysdate = fdate[:4]
        link = 'https://www.espn.in/football/table/_/league/'+leaguedict.get(league, '')+'/season/'+todaysdate
    site = requests.get(link, headers=headers, verify = False).text
    football = BeautifulSoup(site, 'lxml')
    try:
        years = football.find_all('select', class_='dropdown__select')[2]
        years = years.find_all('option')
        yearlist = list()
        for year in years:
            yearlist.append(year.text)
    except :
        tdate = datetime.now().year
        tdate = str(tdate)+'-'+str(tdate+1)[2:]
        yearlist = [tdate]
    try:
        if league != '':
            todaysdate = fdate
            if len(yearlist[0]) == 4 and len(fdate) == 7:
                todaysdate = fdate[:4]
            if len(fdate) == 4 and len(yearlist[0]) == 7:
                todaysdate = fdate+'-'+str(int(fdate)+1)[2:]
            if todaysdate not in yearlist:
                todaysdate = yearlist[0]
                link = 'https://www.espn.in/football/table/_/league/'+leaguedict.get(league, '')
                site = requests.get(link, headers=headers, verify = False).text
                football = BeautifulSoup(site, 'lxml')
        clubnames = football.find('table', class_='Table Table--align-right Table--fixed Table--fixed-left')
        thead1 = clubnames.thead
        clubnames = clubnames.tbody.find_all('tr')
        clublist = list()
        for club in clubnames:
            details = club.find_all('span')
            if len(details) == 1:
                th = details[0].text
                clublist.append([th])
            else:
                pos = details[0].text
                clubid = details[1].a['href'].split('/')[5]
                logo = 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/'+clubid+'.png&h=50'
                shortname = details[2].a.abbr.text
                fullname = details[3].a.text
                clublist.append([pos,logo,shortname,fullname])
        points = football.find('div', class_='Table__ScrollerWrapper relative overflow-hidden')
        try:
            thead1 = thead1.span.text
            thead2 = points.thead.find_all('a')
            thead = list()
            thead.append(thead1)
            for t in thead2:
                thead.append(t.text)
        except :
            thead = list()
        points = points.tbody.find_all('tr')
        pointsdata = list()
        for data in points:
            datalist = list()
            atag = data.find_all('a')
            if len(atag) == 0:
                for point in data.find_all('span'):
                    datalist.append(point.text)
                pointsdata.append(datalist)
            else:
                for th in data.find_all('span'):
                    datalist.append(th.a.text)
                pointsdata.append(datalist)
        tbodydata = list()
        for cname, pdata in zip(clublist, pointsdata):
            tbodydata.append([cname, pdata])
        tabledata = [thead, tbodydata]
        check = len(thead)
    except:
        todaysdate = fdate
        thead = list()
        tabledata = list()
        check = len(thead)
    if league == '':
        league = 'English Premier League'
        tdate = datetime.now().year
        todaysdate = str(tdate)+'-'+str(tdate+1)[2:]

    return render(request, 'tables.html', {'tables': 'active', 'tabledata':tabledata, 'todaysdate':todaysdate, 'leagues':allowedTitles, 'select':league, 'check':check, 'years':yearlist})
