import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools

# Define el alcance y las credenciales para autenticación
CLIENT_ID = '1083902324626-hdpct7kesvnugooh08metlujt6n7o3k8.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Crea el flujo de autenticación
flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri='http://localhost')

# Autentica con Google y obtén el token de acceso
storage = Storage('creds.data')
credentials = tools.run_flow(flow, storage)

# Conecta con Google Sheets
def conectar_google_sheets():
    try:
        gc = gspread.authorize(credentials)
        sheet_clientes = gc.open('clientesJD').worksheet('Clientes')
        sheet_autos = gc.open('clientesJD').worksheet('Autos')
        return sheet_clientes, sheet_autos
    except Exception as e:
        messagebox.showerror("Error de Google Sheets", str(e))

# Función para agregar un cliente
def agregar_cliente():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    auto_buscado = entry_auto_buscado.get()

    if nombre and telefono:
        try:
            sheet_clientes, _ = conectar_google_sheets()
            if sheet_clientes:
                # Obtener el número de filas en la hoja de cálculo de clientes
                num_filas = len(sheet_clientes.get_all_values())
                # Insertar los datos del cliente en la fila correspondiente a los clientes
                sheet_clientes.insert_row([nombre, telefono, auto_buscado], index=num_filas + 1)
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                actualizar_lista_clientes()
                entry_nombre.delete(0, tk.END)
                entry_telefono.delete(0, tk.END)
                entry_auto_buscado.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Función para borrar un cliente seleccionado
def borrar_cliente():
    seleccionado = lista_clientes.curselection()
    if seleccionado:
        cliente_seleccionado = lista_clientes.get(seleccionado)
        nombre_cliente = cliente_seleccionado.split(" - ")[0]
        try:
            sheet_clientes, _ = conectar_google_sheets()
            if sheet_clientes:
                # Obtén todos los registros de la hoja de cálculo de clientes
                data_clientes = sheet_clientes.get_all_values()
                # Busca el cliente en la lista de clientes
                index = next((i for i, row in enumerate(data_clientes) if row[0] == nombre_cliente), None)
                if index is not None:
                    # Borra el cliente
                    sheet_clientes.delete_row(index + 1)  # Suma 1 porque los índices de las filas en Sheets comienzan desde 1
                    messagebox.showinfo("Éxito", "Cliente borrado correctamente.")
                    actualizar_lista_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Por favor, selecciona un cliente para borrar.")

# Función para leer datos de Google Sheets y actualizar la lista de clientes
def actualizar_lista_clientes():
    lista_clientes.delete(0, tk.END)
    try:
        sheet_clientes, _ = conectar_google_sheets()
        if sheet_clientes:
            data_clientes = sheet_clientes.get_all_records()
            for cliente in data_clientes:
                lista_clientes.insert(tk.END, f"{cliente['Nombre']} - Teléfono: {cliente['Telefono']} - Auto Buscado: {cliente['Auto Buscado']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función para agregar un auto
def agregar_auto():
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    año = entry_año.get()
    precio = entry_precio.get()
    disponible = entry_disponible.get()

    if marca and modelo and año and precio and disponible:
        try:
            _, sheet_autos = conectar_google_sheets()
            if sheet_autos:
                # Insertar los datos del auto en la hoja de cálculo de autos
                sheet_autos.append_row([marca, modelo, año, precio, disponible])
                messagebox.showinfo("Éxito", "Auto agregado correctamente.")
                actualizar_lista_autos()
                entry_marca.delete(0, tk.END)
                entry_modelo.delete(0, tk.END)
                entry_año.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
                entry_disponible.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")


# Función para leer datos de Google Sheets y actualizar la lista de autos en stock
def actualizar_lista_autos():
    lista_autos.delete(0, tk.END)
    try:
        _, sheet_autos = conectar_google_sheets()
        if sheet_autos:
            data_autos = sheet_autos.get_all_records()
            for auto in data_autos:
                lista_autos.insert(tk.END, f"{auto['Marca']} {auto['Modelo']} ({auto['Año']}) - Precio: {auto['Precio']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Concesionaria de Autos")
root.geometry("600x400")

# Estilo de la interfaz
root.configure(bg="#f0f0f0")
root.option_add("*Font", "Arial 10")
root.option_add("*Label.Font", "Arial 10 bold")
root.option_add("*Button.Background", "#007bff")
root.option_add("*Button.Foreground", "white")

# Frames
frame_clientes = tk.Frame(root, bg="#f0f0f0")
frame_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_autos = tk.Frame(root, bg="#f0f0f0")
frame_autos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

frame_lista_clientes = tk.Frame(root, bg="#f0f0f0")
frame_lista_clientes.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

frame_lista_autos = tk.Frame(root, bg="#f0f0f0")
frame_lista_autos.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Widgets para clientes
label_nombre = tk.Label(frame_clientes, text="Nombre:", bg="#f0f0f0")
label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nombre = tk.Entry(frame_clientes)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

label_telefono = tk.Label(frame_clientes, text="Teléfono:", bg="#f0f0f0")
label_telefono.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_telefono = tk.Entry(frame_clientes)
entry_telefono.grid(row=1, column=1, padx=5, pady=5)

label_auto_buscado = tk.Label(frame_clientes, text="Auto Buscado:", bg="#f0f0f0")
label_auto_buscado.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_auto_buscado = tk.Entry(frame_clientes)
entry_auto_buscado.grid(row=2, column=1, padx=5, pady=5)

btn_agregar_cliente = tk.Button(frame_clientes, text="Agregar Cliente", command=agregar_cliente)
btn_agregar_cliente.grid(row=3, columnspan=2, pady=5)

# Lista de clientes
label_clientes = tk.Label(frame_lista_clientes, text="Clientes", bg="#f0f0f0")
label_clientes.pack()

lista_clientes = tk.Listbox(frame_lista_clientes, bg="white", fg="#007bff", font="Arial 10")
lista_clientes.pack(fill="both", expand=True)

# Widgets para autos
label_marca = tk.Label(frame_autos, text="Marca:", bg="#f0f0f0")
label_marca.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_marca = tk.Entry(frame_autos)
entry_marca.grid(row=0, column=1, padx=5, pady=5)

label_modelo = tk.Label(frame_autos, text="Modelo:", bg="#f0f0f0")
label_modelo.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_modelo = tk.Entry(frame_autos)
entry_modelo.grid(row=1, column=1, padx=5, pady=5)

label_año = tk.Label(frame_autos, text="Año:", bg="#f0f0f0")
label_año.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_año = tk.Entry(frame_autos)
entry_año.grid(row=2, column=1, padx=5, pady=5)

label_precio = tk.Label(frame_autos, text="Precio:", bg="#f0f0f0")
label_precio.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_precio = tk.Entry(frame_autos)
entry_precio.grid(row=3, column=1, padx=5, pady=5)

label_disponible = tk.Label(frame_autos, text="Disponible (SI/NO):", bg="#f0f0f0")
label_disponible.grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_disponible = tk.Entry(frame_autos)
entry_disponible.grid(row=4, column=1, padx=5, pady=5)

btn_agregar_auto = tk.Button(frame_autos, text="Agregar Auto", command=agregar_auto)
btn_agregar_auto.grid(row=5, columnspan=2, pady=5)

# Lista de autos
label_autos = tk.Label(frame_lista_autos, text="Autos en Stock", bg="#f0f0f0")
label_autos.pack()

lista_autos = tk.Listbox(frame_lista_autos, bg="white", fg="#007bff", font="Arial 10")
lista_autos.pack(fill="both", expand=True)

# Actualizar listas
actualizar_lista_clientes()
actualizar_lista_autos()

# Botones de borrar cliente
btn_borrar_cliente = tk.Button(root, text="Borrar Cliente", command=borrar_cliente)
btn_borrar_cliente.grid(row=3, column=0, padx=5, pady=5)

root.mainloop()
