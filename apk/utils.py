from PIL import Image


_MAX_SIZE = 800

# сжатие загружаемых изображений
def compress_image(source_image):
    filepath = source_image.path
    width = source_image.width
    height = source_image.height
    max_size = max(width, height)  # определяем максимальный размер
    if max_size > _MAX_SIZE:
        image = Image.open(filepath)
        image = image.resize(
            (round(width / max_size * _MAX_SIZE),  # сохраняем пропорции
            round(height / max_size * _MAX_SIZE)),
            Image.ANTIALIAS
        )
        image.save(filepath)
