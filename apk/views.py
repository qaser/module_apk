from apk.models import Act, Fault
from django.shortcuts import get_object_or_404, render


def index_level_3(request):
    # выбираю акты 3 уровня АПК
    acts = Act.objects.all().filter(control_level='3 уровень')
    # извлекаю уникальные значения годов из выбранных актов и сортирую их
    years_uniq = acts.order_by().values('act_year').distinct()
    years = [year.get('act_year') for year in years_uniq]
    context = {}
    # формирую словарь в виде {год: акты этого года}
    for year in years:
        context[year] = acts.filter(act_year=year).order_by('act_number')
    return render(
        request,
        'apk/index-acts.html',
        {'years': context},
    )

def single_act(request, act_year, act_number):
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year)
    faults = Fault.objects.all().filter(act=act)
    return render(
        request,
        'apk/single-act.html',
        {'act': act, 'faults': faults}
    )


def single_fault_act(request, act_year, act_number, fault_id):
    fault = get_object_or_404(Fault, id=fault_id)
    return render(
        request,
        'apk/single-fault-act.html',
        {'fault': fault}
    )

def single_plan(request, act_year, act_number):
    print(dir(request))
    print(request.path)
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year)
    faults = Fault.objects.all().filter(act=act)
    fixed_faults = faults.filter(fixed=True).count()
    locations = faults.values('location__department__title').distinct()
    places = [place.get('location__department__title') for place in locations]
    return render(
        request,
        'apk/single-plan.html',
        {'act': act,
        'faults': faults,
        'fixed_faults': fixed_faults,
        'places': places,}
    )


def single_fault_plan(request, act_year, act_number, fault_id):
    fault = get_object_or_404(Fault, id=fault_id)
    return render(
        request,
        'apk/single-fault-plan.html',
        {'fault': fault}
    )