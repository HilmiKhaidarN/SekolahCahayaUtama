from flask import Flask, render_template_string, request
import os
import math

app = Flask(__name__)

# Mengambil konfigurasi nama aplikasi dari Environment Variable (Nilai Plus K8s ConfigMap)
APP_NAME = os.getenv("APP_NAME", "SDGs Carbon Calculator")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        h1 { color: #2e7d32; text-align: center; }
        .btn { background-color: #2e7d32; color: white; padding: 10px 15px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background-color: #e8f5e9; border-left: 5px solid #2e7d32; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 {{ app_name }}</h1>
        <p style="text-align: center; color: #666;">SDGs Poin 13: Penanganan Perubahan Iklim</p>
        <hr>
        <form method="POST">
            <label>Jarak Tempuh ke Kampus (km):</label><br>
            <input type="number" name="distance" required style="width: 93%; padding: 10px; margin: 10px 0;"><br>
            <label>Jenis Kendaraan:</label><br>
            <select name="vehicle_type" style="width: 100%; padding: 10px; margin: 10px 0;">
                <option value="motorcycle">Sepeda Motor (Bensin)</option>
                <option value="car">Mobil Pribadi (Bensin)</option>
                <option value="bus">Kendaraan Umum / Bus</option>
            </select><br><br>
            <button type="submit" class="btn">Hitung Emisi Karbon</button>
        </form>

        {% if result %}
        <div class="result">
            <h3>Hasil Perhitungan:</h3>
            <p>Estimasi Emisi: <strong>{{ result }} kg CO2</strong> per hari.</p>
            <p><small>Mari kurangi emisi dengan menggunakan transportasi umum atau bersepeda! 🚲</small></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            distance = float(request.form.get("distance", 0))
            vehicle_type = request.form.get("vehicle_type", "motorcycle")
            
            # Faktor emisi sederhana (kg CO2 per km)
            factors = {"motorcycle": 0.1, "car": 0.2, "bus": 0.05}
            emissions = distance * factors.get(vehicle_type, 0.1) * 2 # Pulang-Pergi
            result = round(emissions, 2)
        except ValueError:
            result = "Input tidak valid"
            
    return render_template_string(HTML_TEMPLATE, app_name=APP_NAME, result=result)

# Rute khusus untuk simulasi stress test (Memicu HPA)
@app.route("/stress")
def stress():
    # Melakukan komputasi berat untuk memanaskan CPU
    y = 0.0001
    for i in range(1000000):
        y += math.sin(i) * math.cos(i)
    return f"Simulasi komputasi selesai! CPU load dinaikkan sementara. Nilai: {y}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)