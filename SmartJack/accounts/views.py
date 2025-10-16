from django.http import HttpResponse
from django.template import loader
from .models import Account

def accounts(request):
  myaccounts = Account.objects.all().values()
  template = loader.get_template('all_accounts.html')
  context = {
    'myaccounts': myaccounts,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  myaccount = Account.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'myaccount': myaccount,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))