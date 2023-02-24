import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageFont




class Producto:
    db = 'database/producto.db'


    def __init__(self, root):
        # ventana
        self.ventana = root
        self.ventana.title("Regsitro de Productos")
        self.ventana.resizable(1, 1)
        imagen = Image.open("recursos/LogoGarco.icns")
        self.imagen_tk = ImageTk.PhotoImage(imagen)
        self.ventana.iconphoto(False, self.imagen_tk)

        frame = LabelFrame(self.ventana, text='Registrar un nuevo producto', font=('Ariel', 18, 'bold'))
        frame.grid(row=0, column=0, columnspan=4, pady=20, sticky="nsew")
        self.etiqueta_nombre = Label(frame, text='Nombre: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        self.etiqueta_precio = Label(frame, text='Precio: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        self.etiqueta_categoria = Label(frame, text='Categoría: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_categoria.grid(row=3, column=0)
        self.categoria = ttk.Combobox(frame, values=['Ordenadores', 'Televisores', 'Consolas y Videojuegos'])
        self.categoria.set('Elija su categaoria')
        self.categoria.grid(row=3, column=1)

        self.etiqueta_stock = Label(frame, text='Stock: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_stock.grid(row=4, column=0)
        self.stock = Entry(frame)
        self.stock.grid(row=4, column=1)

        estilo_guardar = ttk.Style()
        estilo_guardar.configure('guardar.TButton',font=('Ariel', 12, 'bold'))
        estilo_guardar.map("guardar.TButton", foreground=[("active", "#00b140")])
        self.boton_agregar = ttk.Button(frame, text='Guardar Producto', command=self.add_producto, style='guardar.TButton')
        self.boton_agregar.grid(row=5, columnspan=2, sticky=W + E)

        frame_mensajes = LabelFrame(self.ventana, text='Mensajes', font=('Ariel', 18, 'bold'))
        frame_mensajes.grid(row=0, column=2, columnspan=3, pady=20, sticky="nsew")
        self.mensaje = Label(frame_mensajes, text='', fg='red')
        self.mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)
        self.mensaje_ok = Label(frame_mensajes, text='', fg='green')
        self.mensaje_ok.grid(row=2, column=0, columnspan=2, sticky=W + E)

        # estilo de la tabla

        # creacion de la tabla
        frame_tabla = LabelFrame(self.ventana, text='Lista de productos producto', font=('Ariel', 18, 'bold'))
        frame_tabla.grid(row=6, column=0, columnspan=3, pady=20, sticky="nsew")
        self.tabla = ttk.Treeview(frame_tabla, height=20, columns=('#0', '#1', '#2', '#3'))
        self.tabla.grid(row=0, column=0, columnspan=3)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)
        self.tabla.heading('#2', text='Categoría', anchor=CENTER)
        self.tabla.heading('#3', text='Stock', anchor=CENTER)

        estilo_eliminar = ttk.Style()
        estilo_eliminar.configure('Peligro.TButton',font=('Ariel', 12, 'bold'))
        estilo_eliminar.map("Peligro.TButton", foreground=[("active", "#ff0000")])
        boton_elimiar = ttk.Button(text='Eliminar', command=self.eliminar_producto, style='Peligro.TButton')
        boton_elimiar.grid(row=10, column=0, sticky=W + E)
        estilo_editar = ttk.Style()
        estilo_editar.configure('editar.TButton', font=('Ariel', 12, 'bold'))
        estilo_editar.map('editar.TButton', foreground=[("active", "#0000ff")])
        boton_editar = ttk.Button(text='Editar', command=self.editar_producto, style='editar.TButton')
        boton_editar.grid(row=10, column=2, sticky=W + E)

        self.get_productos()

    def db_consulta(self, query, parametros=()):

        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(query, parametros)
            con.commit()
            return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM producto ORDER BY Nombre DESC'
        registros = self.db_consulta(query)

        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text=fila[1], values=(fila[2], fila[3], fila[4]))

    def validacion_nombre(self):

        nombre_introducido = self.nombre.get()
        return len(nombre_introducido) != 0

    def validacion_precio(self):

        precio_introducido = self.precio.get()
        try:
            float(precio_introducido)
            return True
        except ValueError:
            return False

    def validacion_categoria(self):
        categoria_introducida = self.categoria.get()
        return len(categoria_introducida) != 0

    def validacion_stock(self):
        stcok_introducido = self.stock.get()
        try:
            float(stcok_introducido)
            return True
        except ValueError:
            return False

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_stock():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)

            self.mensaje_ok['text'] = 'Producto {} añadido con éxito'.format((self.nombre.get()))
            print('Datos guardados')

            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)

        elif self.validacion_nombre() and self.validacion_precio() == False:
            print('El precio es obligario y debe ser un numero')
            self.mensaje['text'] = 'El precio es obligario y debe ser un numero'

        elif self.validacion_nombre() == False and self.validacion_precio():
            print('El nombre es obligario')
            self.mensaje['text'] = 'El nombre es obligario'

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() == False:
            print('El stock debe ser un numero')
            self.mensaje['text'] = 'El stock debe ser un numero'

        else:
            print('Los campos Nombre y Precio no pueden estar vacios.')

            self.mensaje['text'] = 'Nombre y precio no pueden estar vacios.'


        self.get_productos()

    def eliminar_producto(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto para eliminar'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        #no sale por pantalla
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()
        print('producto eleminado')

    def editar_producto(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Selecione el producto que quieres editar'
            return

        name = self.tabla.item(self.tabla.selection())['text']
        old_price = self.tabla.item(self.tabla.selection())['values'][0]
        old_category = self.tabla.item(self.tabla.selection())['values'][1]
        old_stock = self.tabla.item(self.tabla.selection())['values'][2]

        self.ventana_editar = Toplevel()
        self.ventana_editar.title = 'Editar Produtcto'
        self.ventana_editar.resizable(1, 1)

        titulo = Label(self.ventana_editar, text='Edicion de Productos', font=('Ariel', 20, 'bold'))
        titulo.grid(column=0, row=0)
        frame_ep = LabelFrame(self.ventana_editar, text='Edicion de producto', font=('Ariel', 18, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=50, pady=20)

        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=name),
                                          state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()

        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_precio_anituguo.grid(row=4, column=0)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_price),
                                          state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        self.etiqueta_categoria_old = Label(frame_ep, text="Categoría antigua: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_categoria_old.grid(row=6, column=0)
        self.input_categoria_old = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_category),
                                         state='readonly')
        self.input_categoria_old.grid(row=6, column=1)

        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=('Ariel', 15, 'normal'))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, values=['Ordenadores','Televisores','Consolas y Videojuegos'])
        self.input_categoria_nueva.set('Elija su nueva categoria')
        self.input_categoria_nueva.grid(row=7, column=1)
        self.input_categoria_nueva.focus()

        self.etiqueta_stock_old = Label(frame_ep, text='Stock viejo: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_stock_old.grid(row=8, column=0)
        self.input_stock_old = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                     state='readonly')
        self.input_stock_old.grid(row=8, column=1)

        self.etiqueta_stock_nuevo = Label(frame_ep, text='Stock nuevo: ', font=('Ariel', 15, 'normal'))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        self.input_stock_nuevo = Entry(frame_ep)
        self.input_stock_nuevo.grid(row=9, column=1)
        self.input_stock_nuevo.focus()


        s = ttk.Style()
        s.configure('estilo.TButton', font=('Ariel', 12, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='estilo.TButton' , command=lambda:
            self.actualizar_productos(self.input_nombre_nuevo.get(),
                                    self.input_nombre_antiguo.get(),
                                    self.input_precio_nuevo.get(),
                                    self.input_precio_antiguo.get(),
                                    self.input_categoria_old.get(),
                                    self.input_categoria_nueva.get(),
                                    self.input_stock_old.get(),
                                    self.input_stock_nuevo.get()))

        self.boton_actualizar.grid(row=10, columnspan=1, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, categoria_nueva,
                             categoria_old, stock_nuevo, stock_old):

        producto_modificado = False

        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? ' \
                'WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'

        if nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva != '' and stock_nuevo != '':
            parametros = (nuevo_nombre, nuevo_precio, categoria_old, stock_old,
                          antiguo_nombre, antiguo_precio, categoria_nueva, stock_nuevo)
            producto_modificado = True
            print(parametros, 'estoy en 1')

        elif nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva != '' and stock_nuevo == '':
            producto_modificado = True
            parametros =(nuevo_nombre, nuevo_precio, categoria_old, stock_nuevo, nuevo_nombre, nuevo_precio,
                         categoria_nueva, stock_nuevo)
            print(parametros ,'estoy en 2 ')

        elif nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva == '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, categoria_nueva, stock_old, nuevo_nombre, nuevo_precio,
                          categoria_nueva, stock_old)
            print('estoy en 3 ')

        elif nuevo_nombre != '' and nuevo_precio != '' and categoria_nueva == '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (nuevo_nombre, nuevo_precio, categoria_nueva, stock_nuevo, nuevo_nombre, nuevo_precio,
                          categoria_old, stock_old)
            print(parametros ,'estoy en 4 ')

        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva != '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, categoria_nueva, stock_nuevo, antiguo_nombre, antiguo_precio,
                          categoria_nueva, stock_nuevo)
            print(parametros ,'estoy en 5 ')

        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva != '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, categoria_old, stock_nuevo, nuevo_nombre, antiguo_precio,
                          categoria_nueva, stock_old)
            print(parametros ,'estoy en 6 ')

        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva == '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, categoria_nueva, stock_old, nuevo_nombre, antiguo_precio,
                          categoria_old, stock_nuevo)
            print(parametros ,'estoy en 7 ')

        elif nuevo_nombre != '' and nuevo_precio == '' and categoria_nueva == '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (nuevo_nombre, antiguo_precio, categoria_nueva, stock_nuevo, nuevo_nombre, antiguo_precio,
                          categoria_old, stock_old)
            print(parametros ,'estoy en 8 ')

        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva != '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, categoria_old, stock_nuevo, antiguo_nombre, antiguo_precio,
                          categoria_nueva, stock_nuevo)
            print(parametros,'estoy en 9 ')

        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva != '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, categoria_old, stock_nuevo, antiguo_nombre, nuevo_precio,
                          categoria_nueva, stock_old)
            print(parametros ,'estoy en 10 ')

        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva == '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, categoria_nueva, stock_old, antiguo_nombre, nuevo_precio,
                          categoria_old, stock_nuevo)
            print(parametros ,'estoy en 11 ')

        elif nuevo_nombre == '' and nuevo_precio != '' and categoria_nueva == '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (antiguo_nombre, nuevo_precio, categoria_nueva, stock_nuevo, antiguo_nombre, nuevo_precio,
                          categoria_old, stock_old)
            print(parametros ,'estoy en 12 ')

        elif nuevo_nombre == '' and nuevo_precio == '' and categoria_nueva != '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, categoria_old, stock_nuevo, antiguo_nombre, antiguo_precio,
                          categoria_nueva, stock_nuevo)
            print(parametros ,'estoy en 13 ')

        elif nuevo_nombre == '' and nuevo_precio == '' and categoria_nueva != '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, categoria_old, stock_old, antiguo_nombre, antiguo_precio,
                          categoria_nueva, stock_nuevo)
            print('estoy en 14 ')

        elif nuevo_nombre == '' and nuevo_precio == '' and categoria_nueva == '' and stock_nuevo != '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, categoria_nueva, stock_nuevo, antiguo_nombre, antiguo_precio,
                          categoria_old, stock_old)
            print('estoy en 15 ')

        elif nuevo_nombre == '' and nuevo_precio == '' and categoria_nueva == '' and stock_nuevo == '':
            producto_modificado = True
            parametros = (antiguo_nombre, antiguo_precio, categoria_nueva, stock_nuevo, antiguo_nombre, antiguo_precio,
                          categoria_old, stock_old)
            print('estoy en 16 ')

        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje_ok['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            self.get_productos()
            print('productoeditado')
            
        else:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)

