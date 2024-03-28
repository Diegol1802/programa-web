from flask import Flask, render_template

app = Flask(__name__)

# Ruta para el menú con los enlaces a las cuatro páginas
@app.route('/')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='servidor', port=6005)
