import re
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

    best_plan = None
    highest_score = 0
    for filename in os.listdir(plans):
        with open(f'{plans}/{filename}') as file:
            plan = json.load(file)
            score = score_plan(plan) or 0
            if score > highest_score:
                best_plan = plan
                highest_score = score

    [summaryA, summaryB] = map(lambda plan: sum_usage(plan), [plan['serverA'], plan['serverB']])
    
    return JsonResponse({
        "best_plan": best_plan,
        "score": highest_score,
        "server_a_summary": summaryA,
        "server_b_summary": summaryB,
    })

def sum_usage(vms):
    total_memory = 0
    total_disk = 0
    for vm in vms:
        (vm_memory, _) = parse(vm['memory'])
        (vm_disk, _) = parse(vm['disk'])
        total_memory += vm_memory
        total_disk += vm_disk

    return {
        "cpu_cores": len(vms),
        "memory": f'{total_memory}Mi',
        "disk": f'{total_disk}Gb',
    }

def parse(text):
    (number, unit) = re.match('([0-9]+)([A-Za-z]+)', text).group(1, 2)
    number = int(number)
    if unit == 'Gi':
        return (number * 1024, 'Mi')
    if unit == 'Ti':
        return (number * 1024, 'Gb')

    return (number, unit)
    