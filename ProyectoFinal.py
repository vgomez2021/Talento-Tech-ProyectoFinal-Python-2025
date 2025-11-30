import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class SistemaInventario:
    """Sistema de gestión de inventario para negocio de informática"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - Informática")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        # Inicializar base de datos
        self.inicializar_bd()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar productos al inicio
        self.listar_productos()
    
    def inicializar_bd(self):
        """Crea la base de datos y la tabla de productos si no existen"""
        self.conn = sqlite3.connect('inventario.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla productos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        ''')
        self.conn.commit()
    
    def cargar_datos_prueba(self):
        """Carga datos de prueba en la base de datos"""
        try:
            # Verificar si ya hay datos
            self.cursor.execute("SELECT COUNT(*) FROM productos")
            cantidad = self.cursor.fetchone()[0]
            
            if cantidad > 0:
                confirmar = messagebox.askyesno(
                    "Datos existentes",
                    f"Ya hay {cantidad} productos en la base de datos.\n¿Desea agregar datos de prueba de todas formas?"
                )
                if not confirmar:
                    return
            
            # Datos de prueba para negocio de informática
            productos_prueba = [
                # Hardware
                ("Procesador Intel Core i7-13700K", "Procesador 16 núcleos, 3.4GHz base", 15, 389.99, "Hardware"),
                ("Procesador AMD Ryzen 9 7900X", "12 núcleos, 4.7GHz, Socket AM5", 8, 449.99, "Hardware"),
                ("Tarjeta Gráfica NVIDIA RTX 4070", "12GB GDDR6X, Ray Tracing", 5, 599.99, "Hardware"),
                ("Tarjeta Gráfica AMD RX 7800 XT", "16GB GDDR6, 2565MHz", 3, 499.99, "Hardware"),
                ("Motherboard ASUS ROG Strix Z790", "Socket LGA1700, DDR5, WiFi 6E", 12, 329.99, "Hardware"),
                ("Motherboard MSI B650 Gaming", "Socket AM5, PCIe 5.0, DDR5", 10, 199.99, "Hardware"),
                
                # Componentes
                ("Memoria RAM Corsair 32GB DDR5", "2x16GB, 6000MHz, RGB", 25, 159.99, "Componentes"),
                ("Memoria RAM Kingston 16GB DDR4", "2x8GB, 3200MHz, CL16", 30, 59.99, "Componentes"),
                ("SSD Samsung 980 PRO 1TB", "NVMe M.2, 7000MB/s lectura", 20, 119.99, "Almacenamiento"),
                ("SSD Kingston NV2 500GB", "NVMe PCIe 4.0, M.2 2280", 18, 44.99, "Almacenamiento"),
                ("Disco Duro WD Blue 2TB", "7200 RPM, SATA 6Gb/s, 256MB Cache", 15, 64.99, "Almacenamiento"),
                ("Fuente EVGA 850W Gold", "Modular, 80 Plus Gold, PCIe 5.0", 10, 139.99, "Componentes"),
                ("Fuente Corsair 650W Bronze", "Semi-modular, 80 Plus Bronze", 14, 79.99, "Componentes"),
                
                # Periféricos
                ("Teclado Mecánico Logitech G915", "Switches GL Tactile, RGB, Inalámbrico", 22, 229.99, "Periféricos"),
                ("Teclado Razer BlackWidow V3", "Switches mecánicos, RGB Chroma", 18, 139.99, "Periféricos"),
                ("Mouse Logitech G502 Hero", "25600 DPI, 11 botones programables", 35, 79.99, "Periféricos"),
                ("Mouse Razer DeathAdder V3", "30000 DPI, sensor óptico", 28, 69.99, "Periféricos"),
                ("Monitor LG 27 4K UHD", "IPS, 144Hz, HDR400, 1ms", 7, 449.99, "Periféricos"),
                ("Monitor Samsung 24 FHD", "VA, 75Hz, FreeSync, Curvo", 12, 159.99, "Periféricos"),
                ("Webcam Logitech C920", "Full HD 1080p, 30fps, Micrófono", 20, 79.99, "Periféricos"),
                ("Auriculares HyperX Cloud II", "7.1 Surround, Micrófono removible", 25, 99.99, "Periféricos"),
                
                # Redes
                ("Router TP-Link AX5400", "WiFi 6, Dual Band, 8 antenas", 15, 199.99, "Redes"),
                ("Router ASUS RT-AX88U", "WiFi 6, AiMesh, Gaming", 8, 299.99, "Redes"),
                ("Switch TP-Link 8 Puertos", "Gigabit, No administrable", 20, 29.99, "Redes"),
                ("Cable Ethernet Cat 8 10m", "40Gbps, Blindado, RJ45", 50, 19.99, "Redes"),
                ("Adaptador WiFi USB 3.0", "Dual Band AC1200, Antena externa", 30, 24.99, "Redes"),
                
                # Accesorios
                ("Gabinete Corsair 4000D", "ATX Mid Tower, Templado lateral", 10, 109.99, "Accesorios"),
                ("Gabinete NZXT H510 Flow", "ATX, Flujo de aire optimizado, RGB", 8, 119.99, "Accesorios"),
                ("Refrigeración Líquida Corsair H100i", "240mm, RGB, Control iCUE", 12, 129.99, "Accesorios"),
                ("Pasta Térmica Arctic MX-5", "Alto rendimiento, 4g", 45, 9.99, "Accesorios"),
                ("Hub USB 3.0 7 Puertos", "Con alimentación externa, LEDs", 25, 34.99, "Accesorios"),
                ("Mousepad XXL RGB", "900x400mm, Superficie suave, USB", 40, 29.99, "Accesorios"),
                ("Cable HDMI 2.1 3m", "8K 60Hz, 4K 120Hz, eARC", 60, 14.99, "Accesorios"),
                
                # Software
                ("Windows 11 Pro OEM", "Licencia digital, 64 bits", 50, 139.99, "Software"),
                ("Office 2021 Home & Business", "Word, Excel, PowerPoint, Outlook", 30, 249.99, "Software"),
                ("Antivirus Norton 360 Deluxe", "5 dispositivos, 1 año, VPN incluido", 25, 49.99, "Software"),
                ("Adobe Creative Cloud", "Photoshop, Illustrator, 1 año", 15, 599.99, "Software"),
                
                # Productos con stock bajo (para pruebas de reporte)
                ("Tarjeta Gráfica RTX 4090", "24GB GDDR6X, Última generación", 2, 1599.99, "Hardware"),
                ("Procesador Intel i9-14900K", "24 núcleos, overclock extremo", 3, 589.99, "Hardware"),
                ("Monitor OLED 32 4K", "240Hz, HDR1000, G-Sync", 1, 1299.99, "Periféricos"),
                ("Teclado Custom Keychron Q1", "Aluminio CNC, Hot-swap, QMK", 4, 169.99, "Periféricos"),
            ]
            
            # Insertar productos
            self.cursor.executemany('''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', productos_prueba)
            
            self.conn.commit()
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Se han cargado {len(productos_prueba)} productos de prueba correctamente.\n\n"
                "Incluye productos de todas las categorías:\n"
                "• Hardware (procesadores, tarjetas gráficas)\n"
                "• Componentes (RAM, fuentes)\n"
                "• Almacenamiento (SSD, HDD)\n"
                "• Periféricos (teclados, mouse, monitores)\n"
                "• Redes (routers, switches)\n"
                "• Accesorios (gabinetes, cables)\n"
                "• Software (Windows, Office, antivirus)\n\n"
                "💡 Algunos productos tienen stock bajo para probar reportes."
            )
            
            # Actualizar lista
            self.listar_productos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos de prueba: {str(e)}")
    
    def limpiar_base_datos(self):
        """Elimina todos los productos de la base de datos"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM productos")
            cantidad = self.cursor.fetchone()[0]
            
            if cantidad == 0:
                messagebox.showinfo("Base de datos vacía", "No hay productos para eliminar.")
                return
            
            confirmar = messagebox.askyesno(
                "⚠️ Confirmación Crítica",
                f"¿Está SEGURO de eliminar TODOS los {cantidad} productos?\n\n"
                "Esta acción NO se puede deshacer."
            )
            
            if confirmar:
                self.cursor.execute("DELETE FROM productos")
                self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos'")
                self.conn.commit()
                
                messagebox.showinfo("Éxito", f"Se eliminaron {cantidad} productos correctamente.")
                self.limpiar_formulario()
                self.listar_productos()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar base de datos: {str(e)}")
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica"""
        
        # Título principal
        titulo = tk.Label(
            self.root,
            text="🖥️ SISTEMA DE INVENTARIO - INFORMÁTICA",
            font=("Arial", 20, "bold"),
            bg="#34495e",
            fg="white",
            pady=15
        )
        titulo.pack(fill=tk.X)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario
        self.crear_panel_formulario(main_frame)
        
        # Panel derecho - Lista de productos
        self.crear_panel_lista(main_frame)
    
    def crear_panel_formulario(self, parent):
        """Crea el panel de formulario para registro/edición"""
        
        form_frame = tk.Frame(parent, bg="#34495e", relief=tk.RAISED, borderwidth=2)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=5)
        
        # Título del formulario
        titulo_form = tk.Label(
            form_frame,
            text="📝 Registro de Productos",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        titulo_form.pack(pady=10)
        
        # Campos del formulario
        campos_frame = tk.Frame(form_frame, bg="#34495e")
        campos_frame.pack(padx=20, pady=10)
        
        # ID (para edición)
        self.id_var = tk.StringVar()
        tk.Label(campos_frame, text="ID:", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.id_entry = tk.Entry(campos_frame, textvariable=self.id_var, state='readonly', width=30)
        self.id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Nombre
        self.nombre_var = tk.StringVar()
        tk.Label(campos_frame, text="Nombre:*", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_entry = tk.Entry(campos_frame, textvariable=self.nombre_var, width=30)
        self.nombre_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Descripción
        self.descripcion_var = tk.StringVar()
        tk.Label(campos_frame, text="Descripción:", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.descripcion_entry = tk.Entry(campos_frame, textvariable=self.descripcion_var, width=30)
        self.descripcion_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Cantidad
        self.cantidad_var = tk.StringVar()
        tk.Label(campos_frame, text="Cantidad:*", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.cantidad_entry = tk.Entry(campos_frame, textvariable=self.cantidad_var, width=30)
        self.cantidad_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Precio
        self.precio_var = tk.StringVar()
        tk.Label(campos_frame, text="Precio:*", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        self.precio_entry = tk.Entry(campos_frame, textvariable=self.precio_var, width=30)
        self.precio_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # Categoría
        self.categoria_var = tk.StringVar()
        tk.Label(campos_frame, text="Categoría:", bg="#34495e", fg="white", font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=5)
        categorias = ["Hardware", "Periféricos", "Software", "Componentes", "Accesorios", "Redes", "Almacenamiento"]
        self.categoria_combo = ttk.Combobox(campos_frame, textvariable=self.categoria_var, values=categorias, width=27, state='readonly')
        self.categoria_combo.grid(row=5, column=1, pady=5, padx=5)
        
        # Botones de acción
        botones_frame = tk.Frame(form_frame, bg="#34495e")
        botones_frame.pack(pady=20)
        
        btn_agregar = tk.Button(
            botones_frame,
            text="➕ Agregar",
            command=self.agregar_producto,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        btn_agregar.grid(row=0, column=0, padx=5, pady=5)
        
        btn_actualizar = tk.Button(
            botones_frame,
            text="✏️ Actualizar",
            command=self.actualizar_producto,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        btn_actualizar.grid(row=0, column=1, padx=5, pady=5)
        
        btn_limpiar = tk.Button(
            botones_frame,
            text="🔄 Limpiar",
            command=self.limpiar_formulario,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        btn_limpiar.grid(row=1, column=0, padx=5, pady=5)
        
        btn_eliminar = tk.Button(
            botones_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_producto,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        btn_eliminar.grid(row=1, column=1, padx=5, pady=5)
        
        # Sección de búsqueda
        busqueda_frame = tk.Frame(form_frame, bg="#34495e")
        busqueda_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(
            busqueda_frame,
            text="🔍 Búsqueda",
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack()
        
        search_frame = tk.Frame(busqueda_frame, bg="#34495e")
        search_frame.pack(pady=10)
        
        self.busqueda_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.busqueda_var, width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_frame,
            text="Buscar por ID",
            command=lambda: self.buscar_producto("id"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            search_frame,
            text="Por Nombre",
            command=lambda: self.buscar_producto("nombre"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            search_frame,
            text="Por Categoría",
            command=lambda: self.buscar_producto("categoria"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=2)
        
        # Reporte de stock bajo
        reporte_frame = tk.Frame(form_frame, bg="#34495e")
        reporte_frame.pack(pady=10)
        
        tk.Label(
            reporte_frame,
            text="📊 Stock Bajo",
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack()
        
        stock_frame = tk.Frame(reporte_frame, bg="#34495e")
        stock_frame.pack(pady=10)
        
        self.limite_stock_var = tk.StringVar(value="10")
        tk.Label(stock_frame, text="Límite:", bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Entry(stock_frame, textvariable=self.limite_stock_var, width=10).pack(side=tk.LEFT)
        
        tk.Button(
            stock_frame,
            text="Ver Reporte",
            command=self.reporte_stock_bajo,
            bg="#e67e22",
            fg="white",
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón para cargar datos de prueba
        tk.Label(
            form_frame,
            text="⚙️ Herramientas",
            bg="#34495e",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=(20, 5))
        
        btn_datos_prueba = tk.Button(
            form_frame,
            text="📦 Cargar Datos de Prueba",
            command=self.cargar_datos_prueba,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=25
        )
        btn_datos_prueba.pack(pady=5)
        
        btn_limpiar_bd = tk.Button(
            form_frame,
            text="🗑️ Limpiar Base de Datos",
            command=self.limpiar_base_datos,
            bg="#c0392b",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=25
        )
        btn_limpiar_bd.pack(pady=5)
    
    def crear_panel_lista(self, parent):
        """Crea el panel de lista de productos"""
        
        lista_frame = tk.Frame(parent, bg="#34495e", relief=tk.RAISED, borderwidth=2)
        lista_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        
        # Título
        titulo_lista = tk.Label(
            lista_frame,
            text="📦 Inventario de Productos",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        titulo_lista.pack(pady=10)
        
        # Botón refrescar
        tk.Button(
            lista_frame,
            text="🔄 Refrescar Lista",
            command=self.listar_productos,
            bg="#16a085",
            fg="white",
            cursor="hand2"
        ).pack(pady=5)
        
        # Treeview para mostrar productos
        tree_frame = tk.Frame(lista_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio ($)")
        self.tree.heading("Categoría", text="Categoría")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150)
        self.tree.column("Descripción", width=200)
        self.tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.tree.column("Precio", width=80, anchor=tk.CENTER)
        self.tree.column("Categoría", width=120)
        
        # Empaquetar
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_producto)
    
    def agregar_producto(self):
        """Registra un nuevo producto en la base de datos"""
        try:
            # Validar campos obligatorios
            nombre = self.nombre_var.get().strip()
            cantidad = self.cantidad_var.get().strip()
            precio = self.precio_var.get().strip()
            
            if not nombre or not cantidad or not precio:
                messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos obligatorios (*).")
                return
            
            # Validar tipos de datos
            cantidad = int(cantidad)
            precio = float(precio)
            
            if cantidad < 0 or precio < 0:
                messagebox.showerror("Error de validación", "La cantidad y el precio deben ser positivos.")
                return
            
            # Insertar en la base de datos
            self.cursor.execute('''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                nombre,
                self.descripcion_var.get().strip(),
                cantidad,
                precio,
                self.categoria_var.get()
            ))
            
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")
            
            # Limpiar formulario y actualizar lista
            self.limpiar_formulario()
            self.listar_productos()
            
        except ValueError:
            messagebox.showerror("Error de formato", "Cantidad debe ser un número entero y Precio un número decimal.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def actualizar_producto(self):
        """Actualiza un producto existente"""
        try:
            producto_id = self.id_var.get().strip()
            
            if not producto_id:
                messagebox.showwarning("Sin selección", "Seleccione un producto de la lista para actualizar.")
                return
            
            # Validar campos
            nombre = self.nombre_var.get().strip()
            cantidad = self.cantidad_var.get().strip()
            precio = self.precio_var.get().strip()
            
            if not nombre or not cantidad or not precio:
                messagebox.showwarning("Campos incompletos", "Complete todos los campos obligatorios.")
                return
            
            cantidad = int(cantidad)
            precio = float(precio)
            
            # Actualizar en la base de datos
            self.cursor.execute('''
                UPDATE productos
                SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=?
                WHERE id=?
            ''', (
                nombre,
                self.descripcion_var.get().strip(),
                cantidad,
                precio,
                self.categoria_var.get(),
                producto_id
            ))
            
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Producto ID {producto_id} actualizado correctamente.")
            
            self.limpiar_formulario()
            self.listar_productos()
            
        except ValueError:
            messagebox.showerror("Error de formato", "Verifique que cantidad y precio sean números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def eliminar_producto(self):
        """Elimina un producto de la base de datos"""
        try:
            producto_id = self.id_var.get().strip()
            
            if not producto_id:
                messagebox.showwarning("Sin selección", "Seleccione un producto para eliminar.")
                return
            
            # Confirmación
            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro de eliminar el producto ID {producto_id}?"
            )
            
            if confirmar:
                self.cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
                self.conn.commit()
                
                messagebox.showinfo("Éxito", f"Producto ID {producto_id} eliminado.")
                self.limpiar_formulario()
                self.listar_productos()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def buscar_producto(self, tipo_busqueda):
        """Busca productos según el criterio especificado"""
        try:
            termino = self.busqueda_var.get().strip()
            
            if not termino:
                messagebox.showwarning("Campo vacío", "Ingrese un término de búsqueda.")
                return
            
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Buscar según tipo
            if tipo_busqueda == "id":
                self.cursor.execute("SELECT * FROM productos WHERE id=?", (termino,))
            elif tipo_busqueda == "nombre":
                self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{termino}%",))
            elif tipo_busqueda == "categoria":
                self.cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{termino}%",))
            
            resultados = self.cursor.fetchall()
            
            if resultados:
                for producto in resultados:
                    self.tree.insert("", tk.END, values=producto)
                messagebox.showinfo("Resultados", f"Se encontraron {len(resultados)} producto(s).")
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron productos con ese criterio.")
                self.listar_productos()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
    
    def reporte_stock_bajo(self):
        """Genera un reporte de productos con stock bajo"""
        try:
            limite = int(self.limite_stock_var.get())
            
            self.cursor.execute(
                "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC",
                (limite,)
            )
            
            productos = self.cursor.fetchall()
            
            if productos:
                # Crear ventana de reporte
                ventana_reporte = tk.Toplevel(self.root)
                ventana_reporte.title("Reporte de Stock Bajo")
                ventana_reporte.geometry("700x400")
                ventana_reporte.configure(bg="#34495e")
                
                tk.Label(
                    ventana_reporte,
                    text=f"📊 Productos con stock ≤ {limite}",
                    font=("Arial", 14, "bold"),
                    bg="#34495e",
                    fg="white"
                ).pack(pady=10)
                
                # Crear texto con scrollbar
                texto = scrolledtext.ScrolledText(
                    ventana_reporte,
                    width=80,
                    height=20,
                    font=("Courier", 10)
                )
                texto.pack(padx=10, pady=10)
                
                # Escribir reporte
                texto.insert(tk.END, f"{'ID':<5} {'Nombre':<25} {'Cantidad':<10} {'Precio':<10} {'Categoría':<15}\n")
                texto.insert(tk.END, "-" * 80 + "\n")
                
                for p in productos:
                    texto.insert(tk.END, f"{p[0]:<5} {p[1]:<25} {p[3]:<10} ${p[4]:<9.2f} {p[5] or 'N/A':<15}\n")
                
                texto.insert(tk.END, "\n" + "=" * 80 + "\n")
                texto.insert(tk.END, f"Total de productos con stock bajo: {len(productos)}\n")
                texto.config(state=tk.DISABLED)
            else:
                messagebox.showinfo(
                    "Sin alertas",
                    f"No hay productos con stock igual o menor a {limite}."
                )
        
        except ValueError:
            messagebox.showerror("Error", "El límite debe ser un número entero.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def listar_productos(self):
        """Muestra todos los productos en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener todos los productos
            self.cursor.execute("SELECT * FROM productos ORDER BY id")
            productos = self.cursor.fetchall()
            
            # Insertar en la tabla
            for producto in productos:
                self.tree.insert("", tk.END, values=producto)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar productos: {str(e)}")
    
    def seleccionar_producto(self, event):
        """Carga los datos del producto seleccionado en el formulario"""
        try:
            seleccion = self.tree.selection()
            if seleccion:
                item = self.tree.item(seleccion[0])
                valores = item['values']
                
                # Cargar datos en el formulario
                self.id_var.set(valores[0])
                self.nombre_var.set(valores[1])
                self.descripcion_var.set(valores[2])
                self.cantidad_var.set(valores[3])
                self.precio_var.set(valores[4])
                self.categoria_var.set(valores[5] if valores[5] else "")
        
        except Exception as e:
            pass
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.id_var.set("")
        self.nombre_var.set("")
        self.descripcion_var.set("")
        self.cantidad_var.set("")
        self.precio_var.set("")
        self.categoria_var.set("")
        self.busqueda_var.set("")
    
    def __del__(self):
        """Cierra la conexión a la base de datos al destruir el objeto"""
        if hasattr(self, 'conn'):
            self.conn.close()


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaInventario(root)
    root.mainloop()