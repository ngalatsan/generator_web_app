from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flasgger import Swagger
from config import config
import uuid
import generator
import db

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Генератор случайных данных API',
    'uiversion': 3,
    'description': 'Документация для сервиса генерации паролей, UUID, координат и цветов'
}

swagger = Swagger(app)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', YANDEX_MAPS_API_KEY=config['YANDEX_MAPS_API_KEY'])

@app.route('/api/generate-password', methods=['GET'])
def api_generate_password():
    """
    Генерация пароля по заданным параметрам
    ---
    tags:
      - Пароль
    parameters:
      - name: length
        in: query
        type: integer
        required: true
        default: 12
        description: Длина пароля
      - name: use_digits
        in: query
        type: boolean
        required: false
        default: true
        description: Использовать ли цифры
      - name: use_special_chars
        in: query
        type: boolean
        required: false
        default: true
        description: Использовать ли спецсимволы
      - name: use_uppercase
        in: query
        type: boolean
        required: false
        default: true
        description: Использовать ли заглавные буквы
    responses:
      200:
        description: Сгенерированный пароль
        schema:
          type: object
          properties:
            password:
              type: string
              example: "aB3$dEfGh1!"
    """
    length = int(request.args.get('length', 12))
    digits = request.args.get('use_digits', 'true').lower() == 'true'
    spec_ch = request.args.get('use_special_chars', 'true').lower() == 'true'
    uppercase = request.args.get('use_uppercase', 'true').lower() == 'true'
    password = generator.generate_password(length, digits, spec_ch, uppercase)
    db.save_password(password, length, uppercase, digits, spec_ch)
    return jsonify({"password": password})

@app.route('/api/generate-uuid', methods=['GET'])
def api_generate_uuid():
    """
        Генерация уникального идентификатора пользователя UUID
        ---
        tags:
          - UUID
        responses:
          200:
            description: Сгенерированный UUID
            schema:
              type: object
              properties:
                uuid:
                  type: string
                  example: "b758a527-8d49-4002-91c9-afc9b5f90fa6"
        """
    new_uuid = str(uuid.uuid4())
    db.save_uuid(new_uuid)
    return jsonify({"uuid": new_uuid})

@app.route('/api/generate-coordinates')
def api_generate_coordinates():
    """
    Генерация случайных координат
    ---
    tags:
      - Координаты
    parameters:
      - name: lat-min
        in: query
        type: float
        required: false
        default: -90
        description: Минимальная широта
      - name: lat-max
        in: query
        type: float
        required: false
        default: 90
        description: Максимальная широта
      - name: lon-min
        in: query
        type: float
        required: false
        default: -180
        description: Минимальная долгота
      - name: lon-max
        in: query
        type: float
        required: false
        default: 180
        description: Максимальная долгота
    responses:
      200:
        description: Сгенерированные координаты
        schema:
          type: object
          properties:
            latitude:
              type: number
              example: 55.710702
            longitude:
              type: number
              example: 37.603747
            yandex_map_url:
              type: string
              example: "https://yandex.ru/maps/?pt=37.603747,55.710702&z=12&l=map"
    """
    try:
        lat_min = float(request.args.get('lat_min', -90))
        lat_max = float(request.args.get('lat_max', 90))
        lon_min = float(request.args.get('lon_min', -180))
        lon_max = float(request.args.get('lon_max', 180))

        lat, lon = generator.generate_coords(lat_min, lat_max, lon_min, lon_max)
        db.save_coordinates(lat, lon)
        return jsonify({
            "latitude": lat,
            "longitude": lon,
            "yandex_map_url": f"https://yandex.ru/maps/?pt={lon},{lat}&z=12&l=map"
        })

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка сервера: {str(e)}"
        }), 500

@app.route('/api/generate-color')
def generate_color():
    """
    Генерация случайного цвета
    ---
    tags:
      - Цвет
    responses:
      200:
        description: Сгенерированный цвет в HEX и RGB
        schema:
          type: object
          properties:
            hex:
              type: string
              example: "#439e60"
            rgb:
              type: string
              example: "(67, 158, 96)"
    """
    hex_col, R, G, B = generator.generate_color()
    db.save_color(hex_col, R, G, B)
    return jsonify({
        "hex": hex_col,
        "rgb": f"({R}, {G}, {B})"
    })

if __name__ == '__main__':
    app.run()