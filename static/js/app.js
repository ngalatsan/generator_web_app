const API_BASE_URL = window.location.origin;
let map, placemark;

function initMap() {
    ymaps.ready(() => {
        const defaultCoords = [55.710702, 37.603747];

        map = new ymaps.Map("map", {
            center: defaultCoords,
            zoom: 17,
            controls: ['zoomControl', 'typeSelector']
        });

        placemark = new ymaps.Placemark(
            defaultCoords,
            { hintContent: 'Начальная точка' },
            { preset: 'islands#redIcon' }
        );

        map.geoObjects.add(placemark);
    });
}

async function generatePassword() {
    try {
        const length = document.getElementById('length').value;
        if (length < 4) {
            document.getElementById('password-result').textContent = 'Слишком короткий пароль';
            return
        }
        if (length > 100) {
            document.getElementById('password-result').textContent = 'Слишком длинный пароль';
            return
        }
        const useUppercase = document.getElementById('use-uppercase').checked;
        const useDigits = document.getElementById('use-digits').checked;
        const useSpecial = document.getElementById('use-special').checked;

        const response = await fetch(`${API_BASE_URL}/api/generate-password?length=${length}&use_uppercase=${useUppercase}&use_digits=${useDigits}&use_special_chars=${useSpecial}`);
        const data = await response.json();

        document.getElementById('password-result').textContent = data.password;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('password-result').textContent = 'Ошибка: ' + error.message;
        document.getElementById('password-result').classList.add('error');
    }
}

async function generateUUID() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-uuid`);
        const data = await response.json();
        document.getElementById('uuid-result').textContent = data.uuid;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('uuid-result').textContent = 'Ошибка: ' + error.message;
        document.getElementById('uuid-result').classList.add('error');
    }
}

async function generateCoordinates() {
    try {
        const lat_min = parseFloat(document.getElementById('lat_min').value);
        const lat_max = parseFloat(document.getElementById('lat_max').value);
        const lon_min = parseFloat(document.getElementById('lon_min').value);
        const lon_max = parseFloat(document.getElementById('lon_max').value);

        const validationError = validateCoordinates(lat_min, lat_max, lon_min, lon_max);
        if (validationError) throw new Error(validationError);

        const response = await fetch(`${API_BASE_URL}/api/generate-coordinates?lat_min=${lat_min}&lat_max=${lat_max}&lon_min=${lon_min}&lon_max=${lon_max}`);
        const data = await response.json();

        document.getElementById('coordinates-result').textContent =
            `Широта: ${data.latitude}\nДолгота: ${data.longitude}\nСсылка: ${data.yandex_map_url}`;

        ymaps.ready(() => {
            if (placemark) map.geoObjects.remove(placemark);
            placemark = new ymaps.Placemark(
                [data.latitude, data.longitude],
                { balloonContent: 'Случайная точка' },
                { preset: 'islands#redIcon' }
            );
            map.geoObjects.add(placemark);
            map.setCenter([data.latitude, data.longitude], 8);
        });
    } catch (error) {
        document.getElementById('coordinates-result').textContent = error.message;

        ymaps.ready(() => {
            if (placemark) map.geoObjects.remove(placemark);
        });
    }
}

function validateCoordinates(lat_min, lat_max, lon_min, lon_max) {
    if (isNaN(lat_min) || isNaN(lat_max) || isNaN(lon_min) || isNaN(lon_max)) {
        return "Все значения должны быть числами";
    }
    if (lat_min < -90 || lat_min > 90 || lat_max < -90 || lat_max > 90) {
        return "Широта должна быть в диапазоне от -90 до 90";
    }
    if (lon_min < -180 || lon_min > 180 || lon_max < -180 || lon_max > 180) {
        return "Долгота должна быть в диапазоне от -180 до 180";
    }
    if (lat_min >= lat_max) {
        return "Минимальная широта должна быть меньше максимальной";
    }
    if (lon_min >= lon_max) {
        return "Минимальная долгота должна быть меньше максимальной";
    }
    return null;
}

async function generateColor() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-color`);
        const colorData = await response.json();

        document.getElementById('color-display').style.backgroundColor = colorData.hex;
        document.getElementById('hex-code').textContent = colorData.hex;
        document.getElementById('rgb-code').textContent = colorData.rgb;

    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('hex-code').textContent = 'Ошибка: ' + error.message;
        document.getElementById('hex-code').classList.add('error');
        document.getElementById('rgb-code').textContent = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initMap();

    document.getElementById('generate-password').addEventListener('click', generatePassword);
    document.getElementById('generate-uuid').addEventListener('click', generateUUID);
    document.getElementById('generate-coordinates').addEventListener('click', generateCoordinates);
    document.getElementById('generate-color').addEventListener('click', generateColor);
});