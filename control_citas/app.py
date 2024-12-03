from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)

# Ruta de la base de datos
DATABASE = os.path.join(os.path.dirname(__file__), '..', 'bddcitas.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    nombre = request.args.get('nombre')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT ID, Nombre, Apellido FROM Pacientes WHERE Nombre LIKE ?',
        (f'%{nombre}%',)
    )
    pacientes = cursor.fetchall()
    conn.close()
    return jsonify([
        {'id': paciente['ID'], 'nombre': paciente['Nombre'], 'apellido': paciente['Apellido']}
        for paciente in pacientes
    ])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        
        # Insertar datos en la tabla Pacientes
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Pacientes (Nombre, Apellido, Fecha_de_Nacimiento, Teléfono, Correo_Electronico) '
            'VALUES (?, ?, ?, ?, ?)',
            (nombre, apellido, fecha_nacimiento, telefono, correo)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        
        cursor.execute(
            'UPDATE Pacientes SET Nombre=?, Apellido=?, Fecha_de_Nacimiento=?, Teléfono=?, Correo_Electronico=? '
            'WHERE ID=?',
            (nombre, apellido, fecha_nacimiento, telefono, correo, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM Pacientes WHERE ID = ?', (id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template('modificar.html', paciente=paciente)

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener todos los pacientes de la base de datos
    cursor.execute('SELECT ID, Nombre, Apellido FROM Pacientes')
    pacientes = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        # Si se hizo un POST, eliminar el paciente correspondiente
        paciente_id = request.form['id']
        conn = get_db_connection()
        conn.execute('DELETE FROM Pacientes WHERE ID=?', (paciente_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('eliminar'))  # Recargar la página después de la eliminación

    # Si es un GET, mostrar la lista de pacientes
    return render_template('eliminar.html', pacientes=pacientes)


if __name__ == '__main__':
    app.run(debug=True)
