import os
import subprocess
import pandas as pd
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)
OUTPUT_DIR = "/app/outputs"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SEO Auditor Pro</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-5">
    <div class="card shadow-sm p-4">
        <h2 class="mb-4 text-center">🚀 Auditoría SEO Automatizada</h2>
        <form method="post">
            <div class="mb-3">
                <input type="url" name="url" class="form-control" placeholder="https://ejemplo.com" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Generar Auditoría Completa</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template_string(HTML_TEMPLATE)

    url = request.form.get('url')
    try:
        # Comando de rastreo
        command = [
            "screamingfrogseospider", "--crawl", url, "--headless",
            "--save-report", "Internal:All", "--output-folder", OUTPUT_DIR,
            "--export-format", "csv", "--overwrite"
        ]
        
        # Ejecutar y capturar error si ocurre
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return f"<h3>Error en el rastreo:</h3><pre>{result.stderr}</pre>", 500

        # Procesamiento con Pandas (Lógica de tu Notebook)
        csv_path = os.path.join(OUTPUT_DIR, "internal_all.csv")
        df = pd.read_csv(csv_path)

        # Filtros específicos de Auditoría_BLANK.ipynb
        df_4xx = df[df['Status Code'].astype(str).str.startswith('4')].copy()
        df_3xx = df[df['Status Code'].astype(str).str.startswith('3')].copy()
        df_img_heavy = df[df['Size (Bytes)'] > 180000].copy() if 'Size (Bytes)' in df.columns else pd.DataFrame()
        df_desc_long = df[df['Meta Description 1 Length'] > 155].copy() if 'Meta Description 1 Length' in df.columns else pd.DataFrame()
        
        # Imágenes sin Alt
        df_missing_alt = pd.DataFrame()
        if 'Alt Text' in df.columns:
            mask = df['Address'].str.contains(r'\.(jpg|jpeg|png|webp|gif)', case=False, na=False)
            df_missing_alt = df[df['Alt Text'].isna() & mask].copy()

        # Crear Excel con múltiples pestañas
        report_name = "Auditoria_SEO_Final.xlsx"
        excel_path = os.path.join(OUTPUT_DIR, report_name)
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data Cruda', index=False)
            df_4xx.to_excel(writer, sheet_name='Errores 4xx', index=False)
            df_3xx.to_excel(writer, sheet_name='Redirecciones 3xx', index=False)
            df_img_heavy.to_excel(writer, sheet_name='img + 180kb', index=False)
            df_missing_alt.to_excel(writer, sheet_name='missing alt attribute', index=False)
            df_desc_long.to_excel(writer, sheet_name='Descriptions more 155', index=False)

        return send_file(excel_path, as_attachment=True, download_name=report_name)

    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)