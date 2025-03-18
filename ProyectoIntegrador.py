# --------- Sección 1: Importación de módulos ---------
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime

def conectar_bd():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        apellido TEXT,
                        cedula TEXT UNIQUE,
                        rol TEXT,
                        usuario TEXT UNIQUE,
                        contrasena TEXT)''')
    conn.commit()
    conn.close()


# Función para registrar un usuario
def registrar_usuario():
    def guardar_usuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        cedula = entry_cedula.get()
        rol = rol_var.get()
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if len(cedula) != 10 or not cedula.isdigit():
            messagebox.showerror("Error", "La cédula debe tener 10 dígitos numéricos.")
            return

        try:
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, cedula, rol, usuario, contrasena) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, apellido, cedula, rol, usuario, contrasena))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            reg_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La cédula o el usuario ya están registrados.")

    reg_window = tk.Toplevel()
    reg_window.title("Registro de Usuario")

    tk.Label(reg_window, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(reg_window)
    entry_nombre.grid(row=0, column=1)

    tk.Label(reg_window, text="Apellido:").grid(row=1, column=0)
    entry_apellido = tk.Entry(reg_window)
    entry_apellido.grid(row=1, column=1)

    tk.Label(reg_window, text="Cédula:").grid(row=2, column=0)
    entry_cedula = tk.Entry(reg_window)
    entry_cedula.grid(row=2, column=1)

    tk.Label(reg_window, text="Rol:").grid(row=3, column=0)
    rol_var = tk.StringVar(value="Trabajador")
    tk.OptionMenu(reg_window, rol_var, "Administrador", "Trabajador").grid(row=3, column=1)

    tk.Label(reg_window, text="Usuario:").grid(row=4, column=0)
    entry_usuario = tk.Entry(reg_window)
    entry_usuario.grid(row=4, column=1)

    tk.Label(reg_window, text="Contraseña:").grid(row=5, column=0)
    entry_contrasena = tk.Entry(reg_window, show="*")
    entry_contrasena.grid(row=5, column=1)

    tk.Button(reg_window, text="Registrar", command=guardar_usuario).grid(row=6, column=1)


# Función para recuperar contraseña
def recuperar_contrasena():
    def actualizar_contrasena():
        cedula = entry_cedula.get()
        nueva_contrasena = entry_nueva_contrasena.get()

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE cedula = ?", (cedula,))
        usuario = cursor.fetchone()

        if usuario:
            cursor.execute("UPDATE usuarios SET contrasena = ? WHERE cedula = ?", (nueva_contrasena, cedula))
            conn.commit()
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            rec_window.destroy()
        else:
            messagebox.showerror("Error", "No se encontró un usuario con esa cédula.")

        conn.close()

    rec_window = tk.Toplevel()
    rec_window.title("Recuperar Contraseña")

    tk.Label(rec_window, text="Cédula:").grid(row=0, column=0)
    entry_cedula = tk.Entry(rec_window)
    entry_cedula.grid(row=0, column=1)

    tk.Label(rec_window, text="Nueva Contraseña:").grid(row=1, column=0)
    entry_nueva_contrasena = tk.Entry(rec_window, show="*")
    entry_nueva_contrasena.grid(row=1, column=1)

    tk.Button(rec_window, text="Actualizar", command=actualizar_contrasena).grid(row=2, column=1)


# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    usuario_encontrado = cursor.fetchone()
    conn.close()

    if usuario_encontrado:
        messagebox.showinfo("Éxito", f"Bienvenido, {usuario_encontrado[1]} {usuario_encontrado[2]}")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


# Interfaz gráfica
root = tk.Tk()
root.title("Sistema de Inicio de Sesión")
conectar_bd()

tk.Label(root, text="Usuario:").grid(row=0, column=0)
entry_usuario = tk.Entry(root)
entry_usuario.grid(row=0, column=1)

tk.Label(root, text="Contraseña:").grid(row=1, column=0)
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.grid(row=1, column=1)

tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion).grid(row=2, column=1)
tk.Button(root, text="Registrar", command=registrar_usuario).grid(row=3, column=1)
tk.Button(root, text="¿Olvidó su contraseña?", command=recuperar_contrasena).grid(row=4, column=1)

root.mainloop()
# --------- Sección 2: Clase de gestión de base de datos ---------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('ventas.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                codigo TEXT PRIMARY KEY,
                descripcion TEXT,
                precio REAL,
                stock INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                nombre TEXT,
                cedula TEXT PRIMARY KEY,
                direccion TEXT,
                telefono TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                codigo TEXT,
                descripcion TEXT,
                cantidad INTEGER,
                precio REAL,
                total REAL,
                cliente TEXT,
                FOREIGN KEY (codigo) REFERENCES productos(codigo),
                FOREIGN KEY (cliente) REFERENCES clientes(cedula)
            )
        ''')
        self.conn.commit()

    def agregar_producto(self, codigo, descripcion, precio):
        self.cursor.execute('''
            INSERT OR REPLACE INTO productos (codigo, descripcion, precio, stock) VALUES (?, ?, ?, ?)
        ''', (codigo, descripcion, precio, 0))
        self.conn.commit()

    def actualizar_stock(self, codigo, cantidad):
        self.cursor.execute('''
            UPDATE productos SET stock = stock + ? WHERE codigo = ?
        ''', (cantidad, codigo))
        self.conn.commit()

    def registrar_cliente(self, nombre, cedula, direccion, telefono):
        self.cursor.execute('''
            INSERT OR REPLACE INTO clientes (nombre, cedula, direccion, telefono) VALUES (?, ?, ?, ?)
        ''', (nombre, cedula, direccion, telefono))
        self.conn.commit()

    def registrar_venta(self, fecha, codigo, descripcion, cantidad, precio, total, cliente):
        self.cursor.execute('''
            INSERT INTO ventas (fecha, codigo, descripcion, cantidad, precio, total, cliente) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fecha, codigo, descripcion, cantidad, precio, total, cliente))
        self.conn.commit()

    def obtener_productos(self):
        self.cursor.execute('SELECT codigo, descripcion, precio, stock FROM productos')
        return self.cursor.fetchall()

    def obtener_clientes(self):
        self.cursor.execute('SELECT nombre, cedula, direccion, telefono FROM clientes')
        return self.cursor.fetchall()

    def obtener_ventas(self):
        self.cursor.execute('SELECT * FROM ventas')
        return self.cursor.fetchall()


# --------- Sección 3: Clase de aplicación ---------
class Aplicacion:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Registrador de Ventas")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Agregar Producto", command=self.ventana_agregar_producto).grid(row=0, column=0,
                                                                                                  padx=10, pady=10)
        tk.Button(self.root, text="Actualizar Stock", command=self.ventana_actualizar_stock).grid(row=0, column=1,
                                                                                                  padx=10, pady=10)
        tk.Button(self.root, text="Registrar Cliente", command=self.ventana_registrar_cliente).grid(row=0, column=2,
                                                                                                    padx=10, pady=10)
        tk.Button(self.root, text="Registrar Venta", command=self.ventana_registrar_venta).grid(row=1, column=0,
                                                                                                padx=10, pady=10)
        tk.Button(self.root, text="Mostrar Inventario", command=self.ventana_mostrar_inventario).grid(row=1, column=1,
                                                                                                      padx=10, pady=10)
        tk.Button(self.root, text="Mostrar Libro Diario", command=self.ventana_mostrar_libro_diario).grid(row=1,
                                                                                                          column=2,
                                                                                                          padx=10,
                                                                                                          pady=10)
        tk.Button(self.root, text="Mostrar Clientes", command=self.ventana_mostrar_clientes).grid(row=2, column=0,
                                                                                                  padx=10, pady=10)
        tk.Button(self.root, text="Finalizar Día", command=self.ventana_finalizar_dia).grid(row=2, column=1, padx=10,
                                                                                            pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit).grid(row=2, column=2, padx=10, pady=10)

    # --------- Sección 3.1: Ventana de agregar producto ---------
    def ventana_agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Producto")

        tk.Label(ventana, text="Código").grid(row=0, column=0)
        tk.Label(ventana, text="Descripción").grid(row=1, column=0)
        tk.Label(ventana, text="Precio").grid(row=2, column=0)

        codigo = tk.Entry(ventana)
        descripcion = tk.Entry(ventana)
        precio = tk.Entry(ventana)

        codigo.grid(row=0, column=1)
        descripcion.grid(row=1, column=1)
        precio.grid(row=2, column=1)

        tk.Button(ventana, text="Agregar",
                  command=lambda: self.agregar_producto(codigo.get(), descripcion.get(), precio.get(), ventana)).grid(
            row=3, column=1, padx=5, pady=10)

    def agregar_producto(self, codigo, descripcion, precio, ventana):
        if not codigo or not descripcion or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "El precio debe ser un número positivo.")
            return

        if not codigo.replace(' ', '').isalnum():
            messagebox.showerror("Error", "El código solo puede contener letras y números.")
            return

        precio = float(precio)
        if precio < 0:
            messagebox.showerror("Error", "El precio no puede ser negativo.")
            return

        self.db.agregar_producto(codigo, descripcion, precio)
        messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
        ventana.destroy()

    # --------- Sección 3.2: Ventana de actualizar stock ---------
    def ventana_actualizar_stock(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar Stock")

        productos = self.db.obtener_productos()

        tk.Label(ventana, text="Código").grid(row=0, column=0)
        tk.Label(ventana, text="Cantidad a Aumentar").grid(row=1, column=0)

        self.codigo_stock = tk.Entry(ventana)
        self.cantidad_stock = tk.Entry(ventana)

        self.codigo_stock.grid(row=0, column=1)
        self.cantidad_stock.grid(row=1, column=1)

        tk.Button(ventana, text="Actualizar", command=self.actualizar_stock).grid(row=1, column=2, padx=5, pady=10)

        self.tabla_productos = ttk.Treeview(ventana, columns=("Código", "Descripción", "Precio", "Stock"),
                                            show='headings')
        self.tabla_productos.heading("Código", text="Código")
        self.tabla_productos.heading("Descripción", text="Descripción")
        self.tabla_productos.heading("Precio", text="Precio")
        self.tabla_productos.heading("Stock", text="Stock")
        self.tabla_productos.grid(row=2, column=0, columnspan=3, pady=10)

        for producto in productos:
            self.tabla_productos.insert("", tk.END, values=producto)

    def actualizar_stock(self):
        codigo = self.codigo_stock.get()
        cantidad = self.cantidad_stock.get()

        if not codigo or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not cantidad.isdigit() or int(cantidad) < 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        cantidad = int(cantidad)
        self.db.actualizar_stock(codigo, cantidad)
        messagebox.showinfo("Éxito", f"Stock actualizado para {codigo}.")

    # --------- Sección 3.3: Ventana de registrar cliente ---------
    def ventana_registrar_cliente(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Cliente")

        tk.Label(ventana, text="Nombre").grid(row=0, column=0)
        tk.Label(ventana, text="Cédula").grid(row=1, column=0)
        tk.Label(ventana, text="Dirección").grid(row=2, column=0)
        tk.Label(ventana, text="Teléfono").grid(row=3, column=0)

        nombre = tk.Entry(ventana)
        cedula = tk.Entry(ventana)
        direccion = tk.Entry(ventana)
        telefono = tk.Entry(ventana)

        nombre.grid(row=0, column=1)
        cedula.grid(row=1, column=1)
        direccion.grid(row=2, column=1)
        telefono.grid(row=3, column=1)

        tk.Button(ventana, text="Registrar",
                  command=lambda: self.registrar_cliente(nombre.get(), cedula.get(), direccion.get(), telefono.get(),
                                                         ventana)).grid(row=4, column=1, padx=5, pady=10)

    def registrar_cliente(self, nombre, cedula, direccion, telefono, ventana):
        if not nombre or not cedula or not direccion or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return


        if not cedula.isdigit() or len(cedula) != 10:
            messagebox.showerror("Error", "La cédula debe tener exactamente 10 dígitos y no puede contener letras.")
            return

        self.db.registrar_cliente(nombre, cedula, direccion, telefono)
        messagebox.showinfo("Éxito", "Cliente registrado exitosamente.")
        ventana.destroy()

    # --------- Sección 3.4: Ventana de registrar venta ---------
    def ventana_registrar_venta(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Venta")

        tk.Label(ventana, text="Código Producto").grid(row=0, column=0)
        tk.Label(ventana, text="Cantidad").grid(row=1, column=0)
        tk.Label(ventana, text="Cédula Cliente").grid(row=2, column=0)

        codigo_producto = tk.Entry(ventana)
        cantidad = tk.Entry(ventana)
        cedula_cliente = tk.Entry(ventana)

        codigo_producto.grid(row=0, column=1)
        cantidad.grid(row=1, column=1)
        cedula_cliente.grid(row=2, column=1)

        tk.Button(ventana, text="Registrar",
                  command=lambda: self.registrar_venta(codigo_producto.get(), cantidad.get(), cedula_cliente.get(),
                                                       ventana)).grid(row=3, column=1, padx=5, pady=10)

        # Mostrar productos
        productos = self.db.obtener_productos()
        tk.Label(ventana, text="Productos Disponibles").grid(row=4, column=0, columnspan=2)
        tabla_productos = ttk.Treeview(ventana, columns=("Código", "Descripción", "Precio", "Stock"), show='headings')
        tabla_productos.heading("Código", text="Código")
        tabla_productos.heading("Descripción", text="Descripción")
        tabla_productos.heading("Precio", text="Precio")
        tabla_productos.heading("Stock", text="Stock")
        tabla_productos.grid(row=5, column=0, columnspan=2)

        for producto in productos:
            tabla_productos.insert("", tk.END, values=producto)

        # Mostrar clientes
        clientes = self.db.obtener_clientes()
        tk.Label(ventana, text="Clientes Disponibles").grid(row=6, column=0, columnspan=2)
        tabla_clientes = ttk.Treeview(ventana, columns=("Nombre", "Cédula", "Dirección", "Teléfono"), show='headings')
        tabla_clientes.heading("Nombre", text="Nombre")
        tabla_clientes.heading("Cédula", text="Cédula")
        tabla_clientes.heading("Dirección", text="Dirección")
        tabla_clientes.heading("Teléfono", text="Teléfono")
        tabla_clientes.grid(row=7, column=0, columnspan=2)

        for cliente in clientes:
            tabla_clientes.insert("", tk.END, values=cliente)

    def registrar_venta(self, codigo, cantidad, cedula_cliente, ventana):
        if not codigo or not cantidad or not cedula_cliente:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        cantidad = int(cantidad)

        # Verificar si el producto y cliente existen
        productos = self.db.obtener_productos()
        clientes = self.db.obtener_clientes()

        producto_encontrado = False
        cliente_encontrado = False
        precio_producto = 0
        descripcion_producto = ""
        stock_producto = 0

        for prod in productos:
            if prod[0] == codigo:
                producto_encontrado = True
                precio_producto = prod[2]
                descripcion_producto = prod[1]
                stock_producto = prod[3]  # Stock actual del producto
                break

        for cli in clientes:
            if cli[1] == cedula_cliente:
                cliente_encontrado = True
                break

        if not producto_encontrado:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if not cliente_encontrado:
            messagebox.showerror("Error", "Cliente no encontrado.")
            return

        if cantidad > stock_producto:
            messagebox.showerror("Error", "No hay suficiente stock disponible.")
            return

        # Calcular el total de la venta
        total = precio_producto * cantidad
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Registrar la venta en la base de datos
        self.db.registrar_venta(fecha, codigo, descripcion_producto, cantidad, precio_producto, total, cedula_cliente)

        # Actualizar el stock del producto
        self.db.actualizar_stock(codigo, -cantidad)  # Restar la cantidad vendida del stock

        messagebox.showinfo("Éxito", "Venta registrada exitosamente.")
        ventana.destroy()

    # --------- Sección 3.5: Ventana de mostrar inventario ---------
    def ventana_mostrar_inventario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Mostrar Inventario")

        productos = self.db.obtener_productos()

        tabla = ttk.Treeview(ventana, columns=("Código", "Descripción", "Precio", "Stock"), show='headings')
        tabla.heading("Código", text="Código")
        tabla.heading("Descripción", text="Descripción")
        tabla.heading("Precio", text="Precio")
        tabla.heading("Stock", text="Stock")
        tabla.pack()

        for producto in productos:
            tabla.insert("", tk.END, values=producto)

    # --------- Sección 3.6: Ventana de mostrar libro diario ---------
    def ventana_mostrar_libro_diario(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Mostrar Libro Diario")

        ventas = self.db.obtener_ventas()

        tabla = ttk.Treeview(ventana,
                             columns=("","Fecha", "Código", "Descripción", "Cantidad", "Precio", "Total", "Nombre"),
                             show='headings')
        tabla.heading("Código", text="Código")
        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Descripción", text="Descripción")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.heading("Precio", text="Precio")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Total", text="Total")
        tabla.pack()

        total_dia = 0

        for venta in ventas:
            tabla.insert("", tk.END, values=venta)
            total_dia += venta[6]  # Columna del total

        tk.Label(ventana, text=f"Total del Día: {total_dia:.2f}").pack()

    # --------- Sección 3.7: Ventana de mostrar clientes ---------
    def ventana_mostrar_clientes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Mostrar Clientes")

        clientes = self.db.obtener_clientes()

        tabla = ttk.Treeview(ventana, columns=("Nombre", "Cédula", "Dirección", "Teléfono"), show='headings')
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Cédula", text="Cédula")
        tabla.heading("Dirección", text="Dirección")
        tabla.heading("Teléfono", text="Teléfono")
        tabla.pack()

        for cliente in clientes:
            tabla.insert("", tk.END, values=cliente)

    # --------- Sección 3.8: Finalizar Día ---------
    def ventana_finalizar_dia(self):
        respuesta = messagebox.askyesno("Confirmar",
                                        "¿Desea finalizar el día? Esto borrará el registro de ventas del día.")
        if respuesta:
            self.db.cursor.execute('DELETE FROM ventas')
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Día finalizado y ventas borradas.")


# --------- Sección 4: Función principal ---------
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()