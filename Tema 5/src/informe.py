from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session, abort
from __main__ import app
from .login import obtener_id_preceptor
from .models import db, Preceptor, Asistencia, Curso, Estudiante, Padre


@app.route('/informe', methods=['GET'])
def informe():
    preceptor = obtener_id_preceptor()

    if not preceptor:
        return redirect(url_for('login'))

    curso_p = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    curso_id = request.args.get('curso_id', None)

    if not curso_id:
        return render_template('informe_detallado.html', cursos=curso_p)
    
    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
    informe = []
    # Obtener el objeto Curso correspondiente al ID recibido
    for estudiante in estudiantes:
        asistencia = Asistencia.query.filter_by(idestudiante=estudiante.id).all()
        aula = aula_justificada = aula_injustificada = 0
        fisica = fisica_justificada = fisica_injustificada = 0

        for asistencias in asistencia:
            if asistencias.codigoclase == 1:
                if asistencias.asistio == 's':
                    aula += 1
                elif asistencias.asistio == 'n':
                    if asistencias.justificacion:
                        aula_justificada += 1
                    else:
                        aula_injustificada += 1
            elif asistencias.codigoclase == 2:
                if asistencias.asistio == 's':
                    fisica += 1
                elif asistencias.asistio == 'n':
                    if asistencias.justificacion:
                        fisica_justificada += 1
                    else:
                        fisica_injustificada += 1
        total = aula_injustificada + aula_justificada + (fisica_injustificada + fisica_justificada) / 2

        informe.append({
            'estudiante': estudiante,
            'asistencia_fecha': asistencias.fecha.date(),
            'aula': aula,
            'aula_justificada': aula_justificada,
            'aula_injustificada': aula_injustificada,
            'edu_fisica': fisica,
            'fisica_justificada': fisica_justificada,
            'fisica_injustificada': fisica_injustificada,
            'total': total
        })

    return render_template('informe.html', informe=informe, cursos=curso_p)
