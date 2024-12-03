import sqlite3
import os

# Ruta de la base de datos
ruta_db = os.path.join(os.path.dirname(__file__), 'bddcitas.db')

# Crear la base de datos y las tablas
conexion = sqlite3.connect(ruta_db)
cursor = conexion.cursor()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pacientes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Apellido TEXT NOT NULL,
    Fecha_de_Nacimiento DATE,
    Teléfono TEXT,
    Correo_Electronico TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Medicos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Apellido TEXT NOT NULL,
    Especialidad TEXT,
    Teléfono TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Citas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Paciente_ID INTEGER,
    Medico_ID INTEGER,
    Fecha_Hora DATETIME NOT NULL,
    Motivo TEXT,
    Estado TEXT,
    FOREIGN KEY (Paciente_ID) REFERENCES Pacientes(ID),
    FOREIGN KEY (Medico_ID) REFERENCES Medicos(ID)
);
''')

# Guardar cambios y cerrar conexión
conexion.commit()
cursor.close()
conexion.close()
