import json
import csv
from io import StringIO
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .algorithm import generate_plans, score_plan


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

    with open(f'{plans}/plan_1.json') as file:
        plan1 = json.load(file)
    
    best_plan = plan1
    score = score_plan(plan1)

    return JsonResponse({
        "best_plan": best_plan,
        "score": score,
        "server_a_summary": {
            "total_cpu": '',
            "total_ram": "",
            "total_disk_usage": "",
        },
        "server_b_summary": {

        }
    })

