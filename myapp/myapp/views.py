import json
import csv
from io import StringIO
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .algorithm import generate_plans


@csrf_exempt
def index(request):
    os.makedirs('./vmspecs', exist_ok=True)
    filepath = './vmspecs/input.json'

    plansText = request.body.decode('utf-8')
    textIO = StringIO(plansText)
    specs = csv.DictReader(textIO)
    with open(filepath, 'w') as f:
        json.dump(list(specs), f, indent=2)
    
    plans = generate_plans(filepath)
    print(plans)
    return HttpResponse('hello')

