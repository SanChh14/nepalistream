from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.shortcuts import redirect
from slugify import slugify


def highlights(request):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    try:
        num = request.GET['date']
        link = 'http://footeks.com/'+num
    except :
        num = '-1'
        link = 'http://footeks.com/-1'
    site = requests.get(link, headers=headers, verify=False).text
    football = BeautifulSoup(site, 'lxml')
    dates = football.find(class_='card-header shadow font-24 text-center mb-3').find_all('a')
    first = dates[0].text
    second = dates[1].text
    leagues = football.find_all(class_='country-sales-content list-group-item')
    matchesdata = list()
    for league in leagues:
        leagueimg = league.find(class_='row text-center justify-content-center').img['src']
        type = league.find(class_='font-weight-bold text-center').text
        timezone = league.find(class_='ml-5 mb-3').text
        matches = league.find_all('div', class_='row mt-3 pb-3')
        leaguedata = list()
        for match in matches:
            matchdata = match.find_all('span')
            time = matchdata[0].a.text.strip()
            vs = matchdata[1].h6.text
            link = matchdata[2].a['href']
            linktext = matchdata[2].a.text
            hcheck = 0
            try:
                link = link.split('php/')[1]
            except :
                hcheck = 1
            slug = slugify(vs)
            leaguedata.append([time, vs, link, slug, linktext, hcheck])
        leaguedatas = {'type': type, 'leagueimg':leagueimg, 'timezone':timezone, 'leaguedata':leaguedata}
        matchesdata.append(leaguedatas)
    return render(request, 'highlights.html', {'matchesdata':matchesdata, 'highlights':'active', 'date':[first, second, num]})
