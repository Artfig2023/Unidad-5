from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

import src.models
import src.login
import src.registrar_asistencia
import src.informe
import src.listado
import src.consultar

if __name__ == "__main__":
    app.run()