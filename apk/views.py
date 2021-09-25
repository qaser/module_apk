from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import datetime as dt
from django.core.exceptions import ObjectDoesNotExist

from apk.forms import FaultForm, FixForm
from apk.models import Act, Control, Fault


@login_required
def index(request):
    return render(request, 'apk/index.html')


@login_required
def index_control(request, slug):
    control = get_object_or_404(Control, slug=slug)
    acts = Act.objects.all().filter(control_level=control)
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
        {'years': context, 'control': control},
    )


@login_required
def single_act(request, slug, act_year, act_number,):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year, control_level=control)
    faults = Fault.objects.all().filter(act=act)
    return render(
        request,
        'apk/single-act.html',
        {'act': act, 'faults': faults, 'control': control}
    )


@login_required
def single_fault_act(request, slug, act_year, act_number, fault_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year, control_level=control)
    fault = get_object_or_404(Fault, act=act, fault_number=fault_number)
    return render(
        request,
        'apk/single-fault-act.html',
        {'fault': fault,
        'control': control}
    )


@login_required
def single_plan(request, slug, act_year, act_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year, control_level=control)
    faults = Fault.objects.all().filter(act=act)
    fixed_faults = faults.filter(fix__fixed=True).count()
    locations = faults.values('location__department__title').distinct()
    places = [place.get('location__department__title') for place in locations]
    return render(
        request,
        'apk/single-plan.html',
        {'act': act,
        'faults': faults,
        'fixed_faults': fixed_faults,
        'places': places,
        'control': control}
    )


@login_required
def single_fault_plan(request, slug, act_year, act_number, fault_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_number=act_number, act_year=act_year, control_level=control)
    fault = get_object_or_404(Fault, act=act, fault_number=fault_number)
    return render(
        request,
        'apk/single-fault-plan.html',
        {'fault': fault,
        'control': control}
    )


# новый акт
@login_required
def act_new(request, slug):
    control = get_object_or_404(Control, slug=slug)
    present_year = dt.datetime.today().year
    acts = Act.objects.filter(
        act_year=present_year,
        control_level=control,
    )
    # определяю последний доступный номер акта
    act_num = acts.latest('act_number').act_number + 1
    Act.objects.create(
        control_level=control,
        act_year=present_year,
        act_number=act_num
    )
    return redirect('single_act', slug, present_year, act_num)


# новое несоответствие
@login_required
def fault_new(request, slug, act_year, act_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number, control_level=control)
    faults_query = act.faults.all()
    try:
        fault_num = faults_query.latest('fault_number').fault_number + 1
    except ObjectDoesNotExist:
        fault_num = 1
    form = FaultForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.act = act
        form.instance.fault_number = fault_num
        form.instance.inspector = request.user.profile
        form.save()
        return redirect('single_act', slug, act_year, act_number)
    return render(request, 'apk/form-fault.html', {'form': form})


# редактировать несоответствие
@login_required
def fault_edit(request, slug, act_year, act_number, fault_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number, control_level=control)
    fault = get_object_or_404(Fault, fault_number=fault_number, act=act)
    if fault.inspector != request.user.profile:
        return redirect('single_fault_plan', slug, act_year, act_number, fault_number)
    form = FaultForm(request.POST or None, files=request.FILES or None, instance=fault)
    if form.is_valid():
        form.save()
        return redirect('single_fault_act', slug, act_year, act_number, fault_number)
    return render(request, 'apk/form-fault.html', {'form': form})


# новые мероприятия
@login_required
def fix_new(request, slug, act_year, act_number, fault_number):
    control = get_object_or_404(Control, slug=slug)
    act = get_object_or_404(Act, act_year=act_year, act_number=act_number, control_level=control)
    fault = get_object_or_404(Fault, fault_number=fault_number, act=act)
    # if fault.inspector != request.user.profile:
    #     return redirect('single_fault_plan', slug, act_year, act_number, fault_number)
    form = FixForm(request.POST or None, files=request.FILES or None, instance=fault.fix)
    if form.is_valid():
        form.save()
        return redirect('single_fault_plan', slug, act_year, act_number, fault_number)
    return render(request, 'apk/form-fix.html', {'form': form})
