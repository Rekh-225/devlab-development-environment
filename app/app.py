"""
DevLab Unit Converter — Flask Web Application
==============================================
A server-side web application that accepts a numeric value and conversion
type via HTTP POST, performs the mathematical conversion on the server,
and returns the result as JSON.

Accessible at: https://SERVER_IP/converter
Runs on port:  5000 (proxied by Nginx)
Service:       systemd (devlab-app.service)
"""

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ── HTML Template ──────────────────────────────────────────────────────────────
HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unit Converter — DevLab</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f4f4f4; color: #333; }

        nav {
            background: #2c3e50;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        nav .logo { color: white; font-size: 24px; font-weight: bold; }
        nav ul { list-style: none; display: flex; gap: 20px; }
        nav ul li a { color: white; text-decoration: none; font-size: 16px; }
        nav ul li a:hover { color: #3498db; }

        .container {
            max-width: 600px;
            margin: 60px auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h1 { color: #2c3e50; margin-bottom: 8px; }
        .subtitle { color: #666; margin-bottom: 30px; font-size: 14px; }

        label { display: block; margin-bottom: 6px; font-weight: bold; color: #2c3e50; }
        input, select {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: #2980b9; }

        .result {
            margin-top: 25px;
            padding: 20px;
            background: #eaf6ff;
            border-left: 4px solid #3498db;
            border-radius: 4px;
            display: none;
        }
        .result h3 { color: #2c3e50; margin-bottom: 8px; }
        .result .value { font-size: 28px; font-weight: bold; color: #3498db; }

        .error {
            margin-top: 25px;
            padding: 20px;
            background: #ffeaea;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
            display: none;
            color: #e74c3c;
        }

        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 60px;
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">DevLab</div>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/services.html">Services</a></li>
            <li><a href="/converter">Converter</a></li>
            <li><a href="/contact.html">Contact</a></li>
            <li><a href="/about.html">About Us</a></li>
        </ul>
    </nav>

    <div class="container">
        <h1>Unit Converter</h1>
        <p class="subtitle">
            Enter a value and select a conversion. The calculation is performed
            server-side and the result is returned as JSON.
        </p>

        <label for="value">Enter Value:</label>
        <input type="number" id="value" placeholder="e.g. 100" step="any"/>

        <label for="conversion">Conversion Type:</label>
        <select id="conversion">
            <option value="km_to_miles">Kilometres → Miles</option>
            <option value="miles_to_km">Miles → Kilometres</option>
            <option value="celsius_to_fahrenheit">Celsius → Fahrenheit</option>
            <option value="fahrenheit_to_celsius">Fahrenheit → Celsius</option>
            <option value="kg_to_pounds">Kilograms → Pounds</option>
            <option value="pounds_to_kg">Pounds → Kilograms</option>
            <option value="meters_to_feet">Metres → Feet</option>
            <option value="feet_to_meters">Feet → Metres</option>
        </select>

        <button onclick="convert()">Convert</button>

        <div class="result" id="result">
            <h3>Result:</h3>
            <div class="value" id="result-text"></div>
        </div>

        <div class="error" id="error" id="error-text"></div>
    </div>

    <footer>
        <p>&copy; 2026 DevLab. All rights reserved.</p>
    </footer>

    <script>
        async function convert() {
            const value = document.getElementById("value").value;
            const conversion = document.getElementById("conversion").value;

            document.getElementById("result").style.display = "none";
            document.getElementById("error").style.display = "none";

            if (!value) {
                document.getElementById("error").style.display = "block";
                document.getElementById("error").textContent = "Please enter a value.";
                return;
            }

            const response = await fetch("/convert", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    value: parseFloat(value),
                    conversion: conversion
                })
            });

            const data = await response.json();

            if (data.error) {
                document.getElementById("error").style.display = "block";
                document.getElementById("error").textContent = data.error;
            } else {
                document.getElementById("result").style.display = "block";
                document.getElementById("result-text").textContent = data.result;
            }
        }
    </script>
</body>
</html>'''


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/converter')
def converter():
    """Serve the unit converter HTML page."""
    return render_template_string(HTML)


@app.route('/convert', methods=['POST'])
def convert():
    """
    Accept JSON POST with 'value' and 'conversion' fields.
    Perform server-side calculation and return result as JSON.
    """
    data = request.get_json()

    if not data or 'value' not in data:
        return jsonify({'error': 'No value provided'}), 400

    value = data.get('value')
    conversion = data.get('conversion')

    # Conversion functions — all server-side computation
    conversions = {
        'km_to_miles':              lambda x: (round(x * 0.621371, 4), 'miles'),
        'miles_to_km':              lambda x: (round(x * 1.60934, 4),  'km'),
        'celsius_to_fahrenheit':    lambda x: (round(x * 9/5 + 32, 4), '°F'),
        'fahrenheit_to_celsius':    lambda x: (round((x - 32) * 5/9, 4), '°C'),
        'kg_to_pounds':             lambda x: (round(x * 2.20462, 4),  'pounds'),
        'pounds_to_kg':             lambda x: (round(x * 0.453592, 4), 'kg'),
        'meters_to_feet':           lambda x: (round(x * 3.28084, 4),  'feet'),
        'feet_to_meters':           lambda x: (round(x * 0.3048, 4),   'metres'),
    }

    if conversion not in conversions:
        return jsonify({'error': f'Unknown conversion type: {conversion}'}), 400

    result_value, unit = conversions[conversion](value)
    return jsonify({'result': f'{result_value} {unit}'})


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
