from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    if not data:
        return "Error: No data provided", 400

    # Create QR image
    img = qrcode.make(data)

    # Save to a bytes buffer (in-memory)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    # Return as downloadable file
    # download_name is used by modern Flask; older versions used attachment_filename.
    try:
        return send_file(
            buf,
            mimetype='image/png',
            as_attachment=True,
            download_name='qrcode.png'
        )
    except TypeError:
        # fallback for older Flask versions
        return send_file(
            buf,
            mimetype='image/png',
            as_attachment=True,
            attachment_filename='qrcode.png'
        )

if __name__ == '__main__':
    app.run(debug=True)
