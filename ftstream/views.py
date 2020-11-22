from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify

def home(request):
    headers = {'User-Agent':'Mozilla/5 (X11; U; Linux i686; en-US) Gecko/2010 Ubuntu/9.10 (karmic) Firefox/3.5'}
    link = 'https://buffersports.com/football-games'
    site = requests.get(link, headers=headers, verify = False).text
    football = BeautifulSoup(site, 'lxml')
    leagues = football.find_all(class_='country-sales-content list-group-item')
    matchesdata = list()
    for league in leagues:
        leagueimg = league.find(class_='row justify-content-center').img['src']
        type = league.find(class_='row justify-content-center').find(class_='ml-3 mt-3 font-weight-bold').text
        timezone = league.find(class_='ml-5').text
        matches = league.find_all('div', class_='row mt-3')
        leaguedata = list()
        for match in matches:
            matchdata = match.find_all('span')
            time = matchdata[0].a.text.strip()
            vs = matchdata[1].a.text
            link = matchdata[2].a['href']
            slug = slugify(vs)
            leaguedata.append([time, vs, link, slug])
        leaguedatas = {'type': type, 'leagueimg':leagueimg, 'timezone':timezone, 'leaguedata':leaguedata}
        matchesdata.append(leaguedatas)
    return render(request, 'home.html', {'matchesdata':matchesdata, 'home':'active'})

def matches(request):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    link = 'https://buffersports.com/football-games'
    site = requests.get(link, headers=headers, verify=False).text
    football = BeautifulSoup(site, 'lxml')
    leagues = football.find_all(class_='country-sales-content list-group-item')
    matchesdata = list()
    for league in leagues:
        leagueimg = league.find(class_='row justify-content-center').img['src']
        type = league.find(class_='row justify-content-center').find(class_='ml-3 mt-3 font-weight-bold').text
        timezone = league.find(class_='ml-5').text
        matches = league.find_all('div', class_='row mt-3')
        leaguedata = list()
        for match in matches:
            matchdata = match.find_all('span')
            time = matchdata[0].a.text.strip()
            vs = matchdata[1].a.text
            link = matchdata[2].a['href']
            slug = slugify(vs)
            leaguedata.append([time, vs, link, slug])
        leaguedatas = {'type': type, 'leagueimg':leagueimg, 'timezone':timezone, 'leaguedata':leaguedata}
        matchesdata.append(leaguedatas)
    return render(request, 'matches.html', {'matchesdata':matchesdata, 'matches':'active'})

def match(request, slug):
    vs = slug
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    link = 'https://buffersports.com/football-games'
    site = requests.get(link, headers=headers, verify = False).text
    football = BeautifulSoup(site, 'lxml')
    matches = football.find_all('div', class_='row mt-3')
    matchlink = ''
    matchvs = ''
    for match in matches:
        matchdata = match.find_all('span')
        if vs == slugify(matchdata[1].a.text):
            matchvs = matchdata[1].a.text
            matchlink = matchdata[2].a['href']
    if matchlink == '':
        return redirect('fixtures')
    else:
        s = requests.get(matchlink, headers = headers, verify = False).text
        soup = BeautifulSoup(s, 'lxml')
        linksdata = list()
        try:
            iframe = soup.find('iframe')
            link = iframe['src'].split('/')
        except:
            return redirect('fixtures')
        if link[2]=='buffersports.com':
            try:
                iframe = soup.find('iframe')
                link = iframe['src']
                site = requests.get(link, headers=headers, verify = False).text
                football = BeautifulSoup(site, 'lxml')
                linkdata = football.find('table')
                tablerow = linkdata.find_all('tr')
                links = tablerow[1:]
                for link in links:
                    td = link.find_all('td')
                    streamer = td[0].text.strip()
                    if streamer == 'PREMIUM':
                        continue
                    slink = td[1].a['href']
                    channel = td[1].a.text
                    language = td[5].text.strip()
                    linksdata.append([streamer, slink, channel, language])
                return render(request, 'match.html', {'linksdata':linksdata, 'check':len(linksdata), 'vs':matchvs})
            except:
                return redirect('fixtures')
        else:
            return redirect('fixtures')
