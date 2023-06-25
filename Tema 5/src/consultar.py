from datetime import datetime
from flask import Flask, request, render_template, session
from __main__ import app

from .models import db, Asistencia, Estudiante

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if request.method == 'POST':
        dni = request.form['dni']
        inasistencia = Asistencia.query.join(Estudiante, Asistencia.idestudiante == Estudiante.id).filter(Estudiante.dni == dni, Asistencia.asistio == 'n').all()
        return render_template('inasistencias.html', inasistencias=inasistencia)
    else:
        return render_template('consultar.html')
