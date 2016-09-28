from django.shortcuts import render
from django.http import HttpResponse
import HowToClimb.afk as HTCafk
import HowToClimb.apicall as HTCapicall
import HowToClimb.cfg as HTCcfg
import HowToClimb.myRateLimiter as HtcRl
import time
import manage

# Create your views here.

def index(request):
    return render(request, 'Afk/index.html')

def countAfk(request, summonername):
    myAfk = HTCafk.GetAllAfk(summonername, 5, HTCcfg.apiRateLimiter,'euw')
    return render(request, 'afk/afk.html', {'myAfk':myAfk})