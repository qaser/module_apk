from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import datetime as dt

from apk.forms import ActForm, FaultForm, FixForm
from apk.models import Act, Fault


@login_required
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


@login_required
def single_act(request, act_year, act_number):
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year)
    faults = Fault.objects.all().filter(act=act)
    return render(
        request,
        'apk/single-act.html',
        {'act': act, 'faults': faults}
    )


@login_required
def single_fault_act(request, act_year, act_number, fault_number):
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year)
    fault = get_object_or_404(Fault, act=act, fault_number=fault_number)
    return render(
        request,
        'apk/single-fault-act.html',
        {'fault': fault}
    )


@login_required
def single_plan(request, act_year, act_number):
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


@login_required
def single_fault_plan(request, act_year, act_number, fault_number):
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year)
    fault = get_object_or_404(Fault, act=act, fault_number=fault_number)
    return render(
        request,
        'apk/single-fault-plan.html',
        {'fault': fault}
    )


# новый акт
@login_required
def act_new(request):
    form = ActForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        print(form.instance)
        form.instance.act_year = dt.datetime.today().year
        form.save()
        return redirect('single_act', form.instance.act_year, form.instance.act_number)
    return render(request, 'apk/form-act.html', {'form': form})


# новое несоответствие
@login_required
def fault_new(request, act_year, act_number):
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number)
    faults_count = act.faults.all().count()
    form = FaultForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        print(form.instance)
        form.instance.act = act
        form.instance.fault_number = faults_count + 1
        form.instance.inspector = request.user.profile
        form.save()
        return redirect('single_act', act_year, act_number)
    print(form.data)
    return render(request, 'apk/form-fault.html', {'form': form})


# редактировать несоответствие
@login_required
def fault_edit(request, act_year, act_number, fault_number):
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number)
    fault = get_object_or_404(Fault, fault_number=fault_number, act=act)
    if fault.inspector != request.user.profile:
        return redirect('single_fault_plan', act_year, act_number, fault_number)
    form = FaultForm(request.POST or None, files=request.FILES or None, instance=fault)
    if form.is_valid():
        form.save()
        return redirect('single_fault_act', act_year, act_number, fault_number)
    return render(request, 'apk/form-fault.html', {'form': form})


# новые мероприятия
@login_required
def fix_new(request, act_year, act_number, fault_number):
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number)
    fault = get_object_or_404(Fault, fault_number=fault_number, act=act)
    if fault.inspector != request.user.profile:
        return redirect('single_fault_plan', act_year, act_number, fault_number)
    form = FixForm(request.POST or None, files=request.FILES or None, instance=fault)
    if form.is_valid():
        form.save()
        return redirect('single_fault_plan', act_year, act_number, fault_number)
    return render(request, 'apk/form-fix.html', {'form': form})
