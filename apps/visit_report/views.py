#coding=utf-8
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from .models import add_visit,get_daily_visit
import sys
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponseRedirect('/index.html')

def get_trand_data(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)
    return JsonResponse(get_daily_visit(),safe=False)

@csrf_exempt
def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    try:
        template = loader.get_template('common/' + load_template)
    except:
        template = loader.get_template('common/index.html' )
    return HttpResponse(template.render(context, request))

