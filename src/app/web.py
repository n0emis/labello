import logging
from . import app, label
from flask import render_template, send_file, request, jsonify, send_from_directory
from brother_ql.labels import ALL_LABELS


logger = logging.getLogger(__name__)

@app.route('/')
def root():
    return render_template("main.jinja2",
                           website=app.config['WEBSITE'],
                           fonts=app.config['fonts'],
                           margins=app.config['margins'],
                           spacing=app.config['font_spacing'],
                           labels=ALL_LABELS)


@app.errorhandler(404)
def error_404(e):
    return 'api endpoint "{}" not found'.format(request.path), 404


@app.route('/node_modules/<path:filename>', methods=['GET'])
def node_module(filename):
    logger.debug(filename)
    return send_from_directory(app.config['node_path'], filename)


@app.route('/preview', methods=['POST'])
def preview():
    prev = label.Label(request.get_json(True))
    return prev.draw()


@app.route('/preview/qrcode', methods=['POST'])
def qrcode_preview():
    qr = label.Label(request.get_json(True))
    return qr.draw()


@app.route('/preview/image', methods=['POST'])
def image_preview():
    logger.debug(request.files['file'])
    data = request.form.to_dict()
    logger.debug(data)
    img = label.Label(data, request.files['file'])
    return img.draw()


@app.route('/print/text', methods=['POST'])
def prt_text():
    prt = label.Label(request.get_json(True))
    return jsonify(prt.prt())


@app.route('/print/qrcode', methods=['POST'])
def prt_qrcode():
    prt = label.Label(request.get_json(True))
    prt.prt()
    return "printed"


@app.route('/print/image', methods=['POST'])
def prt_image():
    data = request.form.to_dict()
    img = label.Label(data, request.files['file'])
    img.prt()
    return "printed"
