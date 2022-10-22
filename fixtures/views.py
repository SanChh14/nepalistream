from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify
from datetime import datetime

def fixtures(request):
    leaguedict = {
        'All':'all',
        'Spanish Primera Division':'esp.1',
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
    try:
        league = request.GET['league']
        fdate = request.GET['date']
    except :
        league = ''
        fdate = ''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    if fdate == '' and league == '':
        todaysdate = datetime.now()
        todaysdate = [todaysdate.year, todaysdate.month, todaysdate.day]
        link = 'https://www.espn.in/football/fixtures/_/league/all'
    else:
        todaysdate = fdate.split('-')
        fdate = ''.join(fdate.split('-'))
        tdate = datetime.now()
        if todaysdate == [str(tdate.year), str(tdate.month), str(tdate.day)] and league != 'All':
            link = 'https://www.espn.in/football/fixtures/_/league/'+leaguedict.get(league, '')
        else:
            link = 'https://www.espn.in/football/fixtures/_/date/'+fdate+'/league/'+leaguedict.get(league, '')
    site = requests.get(link, headers=headers, verify = False).text
    football = BeautifulSoup(site, 'lxml')
    todaysdate = football.find('div', class_='calendar-container')['data-thisdate']
    todaysdate = [todaysdate[:4], todaysdate[4:6], todaysdate[6:]]
    matches = football.find(id='sched-container')
    fixtures = matches.contents[1:]
    allowedTitles = [
        'English Premier League',
        'Spanish Primera Division',
        'UEFA Champions League',
        'French Ligue 1',
        'Italian Serie A',
        'German Bundesliga',
        'UEFA Europa League',
        'UEFA European Championship Qualifying',
        'UEFA Nations League',
        'International Friendly',
        'FIFA World Cup Qualifying - CONMEBOL',
        'English League Championship',
        'Spanish Copa del Rey',
        'English FA Cup',
        'Italian Coppa Italia',
        'French Coupe de France',
        'German DFB Pokal',
        'FIFA World Cup',
        'FIFA World Cup Qualifying - UEFA',
        'FIFA World Cup Qualifying - CAF',
        'FIFA World Cup Qualifying - CONCACAF',
        'FIFA World Cup Qualifying - AFC',
        'FIFA World Cup Qualifying - OFC',
        'FIFA Confederations Cup',
        'FIFA Club World Cup',
        'FIFA Under-20 World Cup',
        'UEFA European Championship',
        'Copa America',
    ]
    prev = 'div'
    matchesdata = list()
    for fixture in fixtures:
        if fixture.name == 'span':
            matchesdata.append([fixture.find('h2').text, [ [  ], [  ] ] ])
            prev = 'h2'
        elif fixture.name == 'div':
            if prev == 'h2':
                place = 0
            else:
                place = 1
            try:
                matches = fixture.find('tbody').find_all('tr')
                n=0
            except:
                matches = fixture.find_all('tr')
                n=1
            tabhead = fixture.thead.tr.find_all('th')[2].span.text
            if tabhead == 'result':
                tabhead = 'RESULT'
            else:
                tabhead = 'TIME'
            matchesdata[-1][1][place].append(tabhead)
            matchdata = list()
            for match in matches:
                if n == 1:
                    n=0
                    continue
                td = match.find_all('td')
                if len(td) == 1:
                    pen = td[0].small.text
                    matchdata.append([pen])
                    continue
                home = td[0].a.span.text
                homeshort = td[0].a.abbr.text
                if homeshort == home or len(homeshort) > 4:
                    shortl = homeshort.split(' ')
                    sl=list()
                    for a in shortl:
                        sl.append(a[0])
                    homeshort = ''.join(sl)
                homelogo = td[0].find(class_='team-logo').img['src']
                record = td[0].find(class_='record').a.text
                awaylogo = td[1].find(class_='team-logo').img['src']
                away = td[1].a.span.text
                awayshort = td[1].a.abbr.text
                if awayshort == away or len(awayshort) > 4:
                    shortl = awayshort.split(' ')
                    sl=list()
                    for a in shortl:
                        sl.append(a[0])
                    awayshort = ''.join(sl)
                try:
                    time = td[2]['data-date'].split('T')[1][:-1]
                except:
                    try:
                        time = td[2].a.text
                    except :
                        time = 'LIVE'
                matchdata.append([home,homeshort,homelogo,record,awaylogo,away,awayshort,time])
            matchesdata[-1][1][place].append(matchdata)
            prev = 'div'
    if league == '' or league == 'All':
        tempdata = list()
        for matchesdatas in matchesdata:
            if matchesdatas[0] in allowedTitles:
                tempdata.append(matchesdatas)
        matchesdata = tempdata
    return render(request, 'fixtures.html', {'fixtures': 'active', 'matchesdata':matchesdata, 'todaysdate':todaysdate, 'leagues':allowedTitles, 'select':league})
