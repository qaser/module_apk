from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


# склонение слов
@register.filter
def word_tail(number, args):
    args = [arg.strip() for arg in args.split(',')]
    int_num = int(number)
    last_digit = int_num % 10
    last_two_digit = int_num % 100  # для проверки 11...14
    if last_digit == 1 and last_two_digit != 11:
        return f'{number} {args[0]}'  # несоответствие
    if 1 < last_digit < 5 and last_two_digit not in range(11, 15):
        return f'{number} {args[1]}'  # несоответствия
    return f'{number} {args[2]}'  # несоответствий


@register.filter
def color_tag(tag):
    if tag == 'ПБ':
        return 'pb'
    elif tag == 'ОТ':
        return 'ot'
    elif tag == 'Э':
        return 'eco'
    elif tag == 'ПОЖ':
        return 'fire'


@register.simple_tag
def url_replace(request, field, value):
    url_path = request.GET.copy()
    url_path[field] = value
    return url_path.urlencode()
