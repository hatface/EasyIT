# coding:utf-8
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from . import models
import json
from bson.json_util import dumps
from django.http import HttpResponseRedirect
from ..visit_report.models import add_visit
import sys,os
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import xlrd,xlwt
import re

def index(request):
    return HttpResponseRedirect('/capabilityFilingmanager/capabilityFilinglist.html')

@csrf_exempt
def create(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)
    ids = request.GET.get('id')
    new_capabilityFiling = json.loads(request.body)
    if ids:
        for id in ids.split(','):
            models.capabilityFilingManager.update_capabilityFiling_data(id,new_capabilityFiling)
    else:
        if (type(new_capabilityFiling) is list):
            for data_item in new_capabilityFiling[::-1]:
                models.capabilityFilingManager.add_capabilityFiling_data(data_item)
        else:
            models.capabilityFilingManager.add_capabilityFiling_data(new_capabilityFiling)
    return capabilityFilinglist(request)

def delete(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)

    id = request.GET.get('id')
    for idt in id.split(","):
        models.capabilityFilingManager.remove_capabilityFiling_data(idt)
    return JsonResponse({"result":"success"})

def capabilityFilinglist(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)

    context = {}
    template = loader.get_template('capabilityFilingmanager/capabilityFilinglist.html')
    return HttpResponse(template.render(context, request))

def capabilityFilingdata(request):
    limit = int(request.GET.get('limit')) if 'limit' in request.GET else 10
    offset = int(request.GET.get('offset'))  if 'offset' in request.GET else 0
    filter_data = request.GET.get('filter') if 'filter' in request.GET else "{}"
    sort_key = request.GET.get('sort') if 'sort' in request.GET else "_id"
    order = request.GET.get('order') if 'order' in request.GET and 'sort' in request.GET else "desc"
    mfilter = json.loads(filter_data)
    # mfilter = {}
    # if filter_json:
    #     for key in filter_json:
    #         regx = re.compile(".*"+filter_json[key]+".*", re.IGNORECASE)
    #         mfilter[key] = regx
    b_li = models.capabilityFilingManager.search_capabilityFiling_data(mfilter,offset=offset,limit=limit,sort_key=sort_key,order=order)
    resp = {
      "total":None ,
      "rows": None
    }
    resp["rows"] = json.loads(dumps(b_li))
    resp["total"] = models.capabilityFilingManager.get_capabilityFiling_data_count(mfilter)
    return JsonResponse(resp)

def reportdata(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)
    type = request.GET.get('type') if 'type' in request.GET else None
    param = request.GET.get('param')
    resp = {}
    rule = request.GET.get('rule')
    filter_json = None
    if rule:
        if rule.startswith("{"):
            filter_json = json.loads(rule)
        else:
            filter_json = json.loads('{"%s": ".*%s.*"}'%(param,rule))
    if type == "count":
        resp['data'] = models.capabilityFilingManager.get_capabilityFiling_data_count(filter_json)
    elif type=="bar":
        resp = models.capabilityFilingManager.custom_group_search(param,filter_json=filter_json)
    elif type == "pie":
        resp['value'] = models.capabilityFilingManager.custom_group_search(param,split=False,filter_json=filter_json)
    return JsonResponse(resp,safe=False)


def capabilityFilingform(request):
    context = {}
    id = request.GET.get('id')
    copyid = request.GET.get('copyid')
    if(copyid):
        id = copyid
    if id:
        old_capabilityFiling_data = models.capabilityFilingManager.get_capabilityFiling_data_by_id(id)
        context['oldcapabilityFiling'] = json.loads(dumps(old_capabilityFiling_data))
    template = loader.get_template('capabilityFilingmanager/capabilityFilingform.html')
    return HttpResponse(template.render(context, request))

def template_download(request):
    # add visit record
    add_visit(__file__, sys._getframe().f_code.co_name, request)

    filepath = os.path.join(os.path.split(os.path.realpath(__file__))[0],'file','template.xls')
    wb = xlrd.open_workbook(filepath)
    sh = wb.sheet_by_index(0)
    headers = sh.row_values(0)
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    index = 0
    for hd in headers:
        sheet.write(0, index, hd)
        index += 1
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=template.xls'
    wbk.save(response)
    return response


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('capabilityFilingmanager/' + load_template)
    return HttpResponse(template.render(context, request))

