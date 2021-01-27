from flask import Flask, render_template, send_file, request

from calendar_convertor.calendar_converter import CalendarConverter

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/convert-file', methods=["POST"])
def convert_file():
    file = request.files['uploadedfile']
    calendar_type = request.form.get('calendar_type')
    xls_io, file_name = CalendarConverter(file, calendar_type).convert_to_xls()
    print(xls_io)
    return send_file(
        xls_io,
        as_attachment=True,
        attachment_filename=file_name,
        mimetype="application/vnd.ms-excel"
    )


if __name__ == "__main__":
    app.run(debug=True)
