from flask import Flask, request, render_template_string

app = Flask(__name__)

# Plantilla HTML para la interfaz web
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Tiempo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 40px auto; padding: 20px; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .time-group { display: flex; gap: 10px; margin-bottom: 15px; }
        input { width: 60px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #007acc; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background-color: #005f9e; }
        .result { margin-top: 20px; padding: 15px; background-color: #e8f5e9; border-left: 5px solid #4caf50; font-size: 24px; text-align: center; font-weight: bold;}
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align: center; color: #333;">Calculadora de Tiempo</h2>
        <form method="POST">
            <h3>Hora Inicial</h3>
            <div class="time-group">
                <label>H: <input type="number" name="h1" value="{{ request.form.h1 | default(12) }}" min="0" max="23" required></label>
                <label>M: <input type="number" name="m1" value="{{ request.form.m1 | default(45) }}" min="0" max="59" required></label>
                <label>S: <input type="number" name="s1" value="{{ request.form.s1 | default(0) }}" min="0" max="59" required></label>
            </div>

            <h3>Tiempo a Restar</h3>
            <div class="time-group">
                <label>H: <input type="number" name="h2" value="{{ request.form.h2 | default(0) }}" min="0" required></label>
                <label>M: <input type="number" name="m2" value="{{ request.form.m2 | default(0) }}" min="0" required></label>
                <label>S: <input type="number" name="s2" value="{{ request.form.s2 | default(0) }}" min="0" required></label>
            </div>

            <button type="submit">Calcular Resta</button>
        </form>

        {% if result %}
            <div class="result">
                Resultado: {{ result }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            h1, m1, s1 = int(request.form['h1']), int(request.form['m1']), int(request.form['s1'])
            h2, m2, s2 = int(request.form['h2']), int(request.form['m2']), int(request.form['s2'])

            # Convertir todo a segundos para facilitar la resta exacta
            total_segundos_inicial = (h1 * 3600) + (m1 * 60) + s1
            total_segundos_restar = (h2 * 3600) + (m2 * 60) + s2

            diferencia_segundos = total_segundos_inicial - total_segundos_restar

            # Si el resultado es negativo, damos la vuelta al día (24 horas = 86400 segundos)
            if diferencia_segundos < 0:
                diferencia_segundos = 86400 + (diferencia_segundos % 86400)

            # Volver a convertir a horas, minutos y segundos
            res_h = (diferencia_segundos // 3600) % 24
            res_m = (diferencia_segundos % 3600) // 60
            res_s = diferencia_segundos % 60

            # Formatear para que siempre muestre dos dígitos (ej. 09:05:02)
            result = f"{res_h:02d}:{res_m:02d}:{res_s:02d}"
        except Exception as e:
            result = "Error en el cálculo."

    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    # host='0.0.0.0' permite que sea accesible desde tu IP en la red local
    app.run(host='0.0.0.0', port=5000, debug=True)