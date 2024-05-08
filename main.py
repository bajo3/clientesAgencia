import tkinter as tk
from tkinter import messagebox
import sqlite3

# Función para conectar a la base de datos
def conectar_bd():
    conexion = sqlite3.connect('concesionaria.db')
    cursor = conexion.cursor()

    # Crear tabla de clientes si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT,
                        telefono TEXT,
                        auto_buscado TEXT)''')

    # Verificar si la columna auto_buscado existe, y si no, agregarla
    cursor.execute("PRAGMA table_info(clientes)")
    columnas = cursor.fetchall()
    columnas_existentes = [columna[1] for columna in columnas]
    if 'auto_buscado' not in columnas_existentes:
        cursor.execute("ALTER TABLE clientes ADD COLUMN auto_buscado TEXT")

    # Crear tabla de autos si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS autos (
                        id INTEGER PRIMARY KEY,
                        marca TEXT,
                        modelo TEXT,
                        año INTEGER,
                        precio REAL,
                        disponible BOOLEAN)''')

    conexion.commit()
    return conexion, cursor

# Función para cerrar la conexión a la base de datos
def cerrar_bd(conexion):
    conexion.close()

# Función para agregar un cliente
def agregar_cliente():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    auto_buscado = entry_auto_buscado.get()

    if nombre and telefono:
        try:
            cursor.execute("INSERT INTO clientes (nombre, telefono, auto_buscado) VALUES (?, ?, ?)", (nombre, telefono, auto_buscado))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            actualizar_lista_clientes()
            entry_nombre.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
            entry_auto_buscado.delete(0, tk.END)

            # Verificar si hay un auto que coincida con el auto buscado por el cliente
            if auto_buscado:
                auto_buscado = auto_buscado.lower().strip()
                cursor.execute("SELECT * FROM autos")
                autos_disponibles = cursor.fetchall()
                for auto in autos_disponibles:
                    descripcion_auto = f"{auto[1]} {auto[2]} ({auto[3]})".lower().strip()
                    if auto_buscado in descripcion_auto:
                        messagebox.showinfo("Match", f"Se ha encontrado un match para el auto buscado por {nombre}: {auto[1]} {auto[2]} ({auto[3]})")
                        break
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Función para actualizar la lista de clientes en la interfaz gráfica
def actualizar_lista_clientes():
    lista_clientes.delete(0, tk.END)
    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        lista_clientes.insert(tk.END, f"{cliente[1]} - Teléfono: {cliente[2]} - Auto buscado: {cliente[3]}")

# Crear la ventana principal
root = tk.Tk()
root.title("Concesionaria de Autos")
root.geometry("500x400")

# Conectar a la base de datos
conexion, cursor = conectar_bd()

# Estilo de la interfaz
root.configure(bg="#f0f0f0")
root.option_add("*Font", "Arial 10")
root.option_add("*Label.Font", "Arial 10 bold")
root.option_add("*Button.Background", "#007bff")
root.option_add("*Button.Foreground", "white")

# Widgets para agregar clientes
frame_cliente = tk.Frame(root, bg="#f0f0f0")
frame_cliente.pack(padx=10, pady=10, fill="x")

label_nombre = tk.Label(frame_cliente, text="Nombre:", bg="#f0f0f0")
label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nombre = tk.Entry(frame_cliente)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

label_telefono = tk.Label(frame_cliente, text="Teléfono:", bg="#f0f0f0")
label_telefono.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_telefono = tk.Entry(frame_cliente)
entry_telefono.grid(row=1, column=1, padx=5, pady=5)

label_auto_buscado = tk.Label(frame_cliente, text="Auto Buscado:", bg="#f0f0f0")
label_auto_buscado.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_auto_buscado = tk.Entry(frame_cliente)
entry_auto_buscado.grid(row=2, column=1, padx=5, pady=5)

btn_agregar_cliente = tk.Button(frame_cliente, text="Agregar Cliente", command=agregar_cliente)
btn_agregar_cliente.grid(row=3, columnspan=2, pady=5)

# Lista de clientes
frame_lista_clientes = tk.Frame(root, bg="#f0f0f0")
frame_lista_clientes.pack(padx=10, pady=10, fill="both", expand=True)

label_clientes = tk.Label(frame_lista_clientes, text="Clientes", bg="#f0f0f0")
label_clientes.pack()

lista_clientes = tk.Listbox(frame_lista_clientes, bg="white", fg="#007bff", font="Arial 10")
lista_clientes.pack(fill="both", expand=True)

# Actualizar lista de clientes
actualizar_lista_clientes()

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al salir
cerrar_bd(conexion)
