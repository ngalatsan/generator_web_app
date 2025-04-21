import random
import string

def generate(length, chars):
    password = ''
    for i in range(length):
        char = random.choice(chars)
        password += char
    return password

def generate_password(length=12, use_digits=True, use_special_chars=True, use_uppercase=True):
    if length < 4:
        return 'Слишком короткий пароль'
    elif length > 100:
        return 'Слишком длинный пароль'

    chars = string.ascii_lowercase
    if use_uppercase:
        chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special_chars:
        chars += "!@#$%^&*()_=~"
    return generate(length, chars)

def generate_coords(lat_min=-90, lat_max=90, lon_min=-180, lon_max=180):
    if not (-90 <= lat_min <= 90) or not (-90 <= lat_max <= 90):
        raise ValueError("Широта должна быть в диапазоне от -90 до 90")

    if not (-180 <= lon_min <= 180) or not (-180 <= lon_max <= 180):
        raise ValueError("Долгота должна быть в диапазоне от -180 до 180")

    if lat_min >= lat_max:
        raise ValueError("Минимальная широта должна быть меньше максимальной")

    if lon_min >= lon_max:
        raise ValueError("Минимальная долгота должна быть меньше максимальной")

    return (
        round(random.uniform(lat_min, lat_max), 6),
        round(random.uniform(lon_min, lon_max), 6)
    )

def generate_color():
    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    return color, r, g, b