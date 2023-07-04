from __main__ import app
from flask import render_template, request, redirect, url_for
from .models import Curso, Estudiante, Asistencia, db
from .login import obtener_preceptor_actual
from datetime import datetime

@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():

    preceptor_actual = obtener_preceptor_actual()

    if not preceptor_actual:
        return redirect(url_for('login'))

    curso_id = request.args.get('curso_id', None)

    if not curso_id:
        return redirect(url_for('home'))

    curso = Curso.query.filter_by(id=curso_id, idpreceptor=preceptor_actual.id).first()

    if not curso:
        return redirect(url_for('home'))

    # Restricción: Solo se puede registrar una vez al día
    if request.method == 'POST':
        fecha = request.form['fecha']
        fecha_actual = datetime.now().date()
        fecha_seleccionada = datetime.strptime(fecha, "%Y-%m-%d").date()

        if fecha_seleccionada > fecha_actual:
            return render_template("message.html", message="No se puede registrar asistencia en días anteriores.", tipo="error")

        asistencia_registrada = Asistencia.query.filter_by(codigoclase=int(request.form['clase']), fecha=fecha_seleccionada).first()
        if asistencia_registrada:
            return render_template("message.html", message="La asistencia ya ha sido registrada para esta fecha.", tipo="error")

        clase = int(request.form['clase'])
        for estudiante in curso.estudiantes:
            estudiante_id = estudiante.id
            asistencia = request.form.get(f'asistencia_{estudiante.id}') 
            justificacion = request.form.get(f'justificacion_{estudiante.id}', '')
            registro_asistencia = Asistencia(
                idestudiante=estudiante_id,
                fecha=fecha_seleccionada,
                codigoclase=clase,
                asistio=asistencia,
                justificacion=justificacion if asistencia == 'n' else None 
            )

            db.session.add(registro_asistencia)
        db.session.commit()
        return render_template("message.html", message="Asistencia registrada con éxito", tipo="success")

    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()

    return render_template('registrar_asistencia.html', curso=curso, estudiantes=estudiantes)

