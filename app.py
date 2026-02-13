import subprocess
from urllib import request

from flask import Flask, render_template_string
import os

app = Flask(__name__)

homepage_html = '\n<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Utility Hub</title>\n    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n</head>\n<body>\n    <div class="container mt-5">\n        <h1 class="text-center">Welcome to Utility Hub</h1>\n        <p class="text-center">Choose a utility below:</p>\n        <div class="list-group">\n            <a href="/utility-a" class="list-group-item list-group-item-action">Utility A</a>\n            <a href="/utility-b" class="list-group-item list-group-item-action">Utility B</a>\n            <a href="/utility-c" class="list-group-item list-group-item-action">Utility C</a>\n        </div>\n    </div>\n</body>\n</html>\n'

@app.route('/')
def homepage():
    return render_template_string(homepage_html)

utility_a_html = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Advanced Profile Migration Utility</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script>
        function showProgress() {
            document.getElementById('progress').style.display = 'block';
        }
    </script>
</head>
<body>
    <div class='container mt-5'>
        <h2>Advanced Profile Migration Utility</h2>
        <form method='POST' enctype='multipart/form-data' onsubmit='showProgress()'>
            {% for filename in files %}
            <div class='mb-3'>
                <label class='form-label'>{{ filename }}</label>
                <div class='d-flex'>
                    <a href='/download-example/{{ filename }}' class='btn btn-secondary me-2'>Download Example</a>
                    <input type='file' class='form-control' name='{{ filename }}' required>
                </div>
            </div>
            {% endfor %}
            <button type='submit' class='btn btn-primary'>Start</button>
        </form>
        <div id='progress' class='mt-3' style='display:none;'>
            <div class='progress'>
                <div class='progress-bar progress-bar-striped progress-bar-animated' style='width:100%'>Uploading and Processing...</div>
            </div>
        </div>
    </div>
</body>
</html>"""

@app.route('/utility-a', methods=['GET', 'POST'])
def utility_a():
    if request.method == 'POST':
        uploaded_paths = []
        for fname in required_files:
            file = request.files.get(fname)
            if file:
                path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
                file.save(path)
                uploaded_paths.append(path)

        subprocess.run(['python', 'run_migration.py'] + uploaded_paths)
        return "Files uploaded and migration process started."
    return render_template_string(utility_a_html, files=required_files)

@app.route('/download-example/<filename>')
def download_example(filename):
    example_path = os.path.join('examples', filename)
    if os.path.exists(example_path):
        return send_file(example_path, as_attachment=True)
    return f"Example file for {filename} not found.", 404

if __name__ == '__main__':
    os.makedirs('examples', exist_ok=True)
    for fname in required_files:
        example_path = os.path.join('examples', fname)
        if not os.path.exists(example_path):
            with open(example_path, 'w') as f:
                f.write(f"Example content for {fname}")
    app.run(debug=True)

@app.route('/utility-b')
def utility_b():
    return "This is Utility B page."

@app.route('/utility-c')
def utility_c():
    return "This is Utility C page."

if __name__ == '__main__':
    app.run(debug=True)
