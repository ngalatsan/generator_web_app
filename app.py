from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from config import config
import uuid
import generator
import db

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', YANDEX_MAPS_API_KEY=config['YANDEX_MAPS_API_KEY'])

@app.route('/api/generate-password', methods=['GET'])
def api_generate_password():
    length = int(request.args.get('length', 12))
    digits = request.args.get('use_digits', 'true').lower() == 'true'
    spec_ch = request.args.get('use_special_chars', 'true').lower() == 'true'
    uppercase = request.args.get('use_uppercase', 'true').lower() == 'true'
    password = generator.generate_password(length, digits, spec_ch, uppercase)
    db.save_password(password, length, uppercase, digits, spec_ch)
    return jsonify({"password": password})

@app.route('/api/generate-uuid', methods=['GET'])
def api_generate_uuid():
    new_uuid = str(uuid.uuid4())
    db.save_uuid(new_uuid)
    return jsonify({"uuid": new_uuid})

@app.route('/api/generate-coordinates')
def api_generate_coordinates():
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
    hex_col, R, G, B = generator.generate_color()
    db.save_color(hex_col, R, G, B)
    return jsonify({
        "hex": hex_col,
        "rgb": f"({R}, {G}, {B})"
    })

if __name__ == '__main__':
    app.run()