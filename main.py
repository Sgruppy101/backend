from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageDraw
import random

app = FastAPI()

def generate_abstract_image(width: int, height: int) -> Image:
    # Создание пустого изображения с черным фоном
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)

    # Генерация случайных цветов и рисование на изображении
    for _ in range(random.randint(50, 100)):  # Случайное количество фигур
        # Генерация случайного цвета
        color = tuple(random.randint(0, 255) for _ in range(3))

        # Генерация случайных координат
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        # Используем min и max для правильной установки координат
        x0 = min(x1, x2)
        y0 = min(y1, y2)
        x1 = max(x1, x2)
        y1 = max(y1, y2)

        # Рисование случайного прямоугольника
        draw.rectangle([x0, y0, x1, y1], fill=color)

    return image

@app.get("/abstract-image")
async def get_abstract_image(width: int = 800, height: int = 600):
    image = generate_abstract_image(width, height)
    
    # Сохраняем изображение в BytesIO
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)