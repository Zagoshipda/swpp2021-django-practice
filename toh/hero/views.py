from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.http.response import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import json
from json.decoder import JSONDecodeError

from .models import Hero

def index(request):
    if 'visit_count' not in request.session:
        request.session['visit_count'] = 1
    else:
        request.session['visit_count'] += 1

    return HttpResponse('Hello, world! You visited {} times.\n'.format(request.session['visit_count']))

def id(request, id):
    return HttpResponse(f'Your id is {id}!')

def name(request, name):
    return HttpResponse(f'Your name is {name}!')

@csrf_exempt
def hero_info(request, id):
    if request.method == 'GET':
        hero = Hero.objects.get(id=id)
        return JsonResponse({"id": hero.id, "name": hero.name, "age": hero.age})

    elif request.method == 'PUT':
        try:
            body = request.body.decode()
            hero_name = json.loads(body)['name']
            hero_age = json.loads(body)['age']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        hero = Hero.objects.get(id=id)
        hero.name = hero_name
        hero.age = hero_age
        hero.save()
        response_dict = {"id": hero.id, "name": hero.name, "age": hero.age}
        return JsonResponse(response_dict, status=200)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT'])

@csrf_exempt
def hero_list(request):
    if request.method == "GET":
        hero_all_list = [hero for hero in Hero.objects.all().values()]
        return JsonResponse(hero_all_list, safe=False)
    elif request.method == "POST":
        try:
            body = request.body.decode()
            hero_name = json.loads(body)['name']
            hero_age = json.loads(body)['age']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        hero = Hero(name=hero_name, age=hero_age)
        hero.save()
        response_dict = {'id': hero.id, 'name': hero.name, 'age': hero.age}
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
