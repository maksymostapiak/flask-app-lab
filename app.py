from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume():
    return render_template(
        'resume.html',
        page_title='Резюме',
        header_title='Моє резюме'
    )

@app.route('/contacts')
def contacts():
    return render_template(
        'contacts.html',
        page_title='Контакти',
        header_title='Зв’язок зі мною'
    )

if __name__ == '__main__':
    app.run(debug=True)