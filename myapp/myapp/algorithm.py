import json
import os
import random
from datetime import datetime


def generate_plans(vm_spec_path):
    '''
    Generate a number of virtual machine allocation plans.
    In each plan, some virtual machines will be allocated to physical
    server A, and another machines will be allocated to server B.

    ============================ATTENTION======================================
    Please note that a random split strategy is used here to mock the output,
    not real alloction algorithm. Candidates only need to use the mock return,
    please do not worry about the details here.
    ===========================================================================

    Args:
        vm_spec_path (str): Path to the VM requirement file detailing the list
        of VMs to allocate resources for.
        Expects file to be JSON serialized in the form of
            (:obj:`list` of :obj:`dict`).

        Example:
        [{"id": "0", "cpu": "Intel 8v Core", "memory": "8Gi", "disk": "500Gb"}]

    Returns:
        allocation_folder (str): Path to the output folder containing generated
        plans. The basic JSON format of of the allocation plans will be
        {
            'serverA':(:obj:`list` of :obj:`dict`),
            'serverB':(:obj:`list` of :obj:`dict`)
        }
        Example:
        {
            'serverA':[{"id": "0", "cpu": "Intel 8v Core", "memory": "8Gi", "disk": "500Gb"}],
            'serverB':[{"id": "15", "cpu": "Intel 2v Core", "memory": "500Mi", "disk": "100Gb"}]
        }
    '''

    plan_folder = './plans'

    os.makedirs(plan_folder, exist_ok=True)

    specs = list()
    with open(vm_spec_path) as file_handle:
        vm_spec_list = json.load(file_handle)
        # Generate 20 ramdom shuffled copy of the input spec list
        for _ in range(0, 20):
            random.seed(datetime.now())
            specs.append(random.sample(vm_spec_list, len(vm_spec_list)))

    for idx, plan in enumerate(specs, start=1):
        random.seed(idx)
        split_idx = random.randint(0, len(plan) - 1)
        specs_to_serverA = plan[0:split_idx]
        specs_to_serverB = plan[split_idx:]
        plan = {'serverA': specs_to_serverA, 'serverB': specs_to_serverB}
        plan_path = os.path.join(plan_folder, 'plan_{}.json'.format(idx))

        with open(plan_path, 'w') as plan_file:
            json.dump(plan, plan_file)

    return plan_folder


def score_plan(plan_json):
    '''
    Evaluates and returns a score suggesting the quality of the allocation plan

    ============================ATTENTION======================================
    Please note that a random number is returned to mock the scoring result,
    not real scoring logic.Candidates only need to use the mock return, please
    do not worry about the details here.
    ===========================================================================

    Args:
        plan_json: One allocation plan of virtual machines.
        The basic JSON format of of the allocation plans will be
        {
            'serverA':(:obj:`list` of :obj:`dict`),
            'serverB':(:obj:`list` of :obj:`dict`)
        }
        Example:
        {
            'serverA':[{"id": "0", "cpu": "Intel 8v Core", "memory": "8Gi", "disk": "500Gb"}],
            'serverB':[{"id": "15", "cpu": "Intel 2v Core", "memory": "500Mi", "disk": "100Gb"}]
        }

    Returns:
        score (int | None): Plan score (out of 100) if valid.
        Returns None if the plan is invalid
    '''

    seed = int("".join(map(lambda vm: str(vm['id']), plan_json['serverA'])))

    random.seed(seed)

    if random.randint(0, 100) < 45:
        return None

    return random.randrange(45, 90)
