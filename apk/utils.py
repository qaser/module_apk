from django.core.paginator import Paginator
from PIL import Image


_MAX_SIZE = 1000


# сжатие загружаемых изображений
def compress_image(source_image):
    filepath = source_image.path
    width = source_image.width
    height = source_image.height
    max_size = max(width, height)  # определяем максимальный размер
    if max_size > _MAX_SIZE:
        image = Image.open(filepath)
        image = image.resize(
            (
                round(width / max_size * _MAX_SIZE),
                round(height / max_size * _MAX_SIZE)
            ),
            Image.ANTIALIAS
        )
        image.save(filepath)


# проверка наличия введенного объекта в поля исполнителей
# использую при экспорте в формат .xlsx
def check_person(person):
    if person is not None:
        return person.lastname_and_initials
    return 'Данные не введены'


# пагинатор
def split_on_page(request, queryset):
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return {'page': page, 'paginator': paginator}
