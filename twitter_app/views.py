from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse
from twitter_app.tweet_fonksiyonlari import main
# Create your views here.

def main_page(request):
    context_dict = {}
    return render(request, 'main.html', context_dict)

def dashboard(request):
    if request.GET.get('username'):
        kullanici_adi = request.GET.get('username')
        data = main(kullanici_adi)
        polarite = data[0] # polarite bilgileri
        tweetler = data[1] # tweet polariteleri ve tweet bilgileri
        time_dict = {}
        for i in range(0, 23, 2):
            time_dict['{}'.format(i)] = 0
        for i in tweetler:
            tarih = i['tarih']
            tarih = str(tarih)
            tarih = tarih.split(' ')[1].split(':')[0]
            b = int(tarih)
            if b == 0:
                time_dict['{}'.format(b)] += 1
            elif b % 2 == 1:
                b -= 1
                time_dict['{}'.format(b)] += 1
            elif b % 2 == 0:
                time_dict['{}'.format(b)] += 1

        context_dict = {'tweetler':tweetler, 'polarite':polarite, 'zaman':time_dict}

        return render(request, 'dashboard.html', context_dict)
