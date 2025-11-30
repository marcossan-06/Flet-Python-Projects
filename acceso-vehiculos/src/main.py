import flet as ft
import time  # para hacer un sleep y simular que la app carga
import collections # para contar valores repetidos de diccionarios (más eficiente que con un bucle y contadores)

from ControlAcceso import ControlAcceso
from Vehiculo import Vehiculo

# Para gestionar todo el backend
control = ControlAcceso()

# FORMULARIO DE REGISTRO DE VEHÍCULOS
def crear_form_registro(page):

    # CAMPOS
    # Compruebo que el usuario no introduce símbolos raros,
    # no hago la regex más estricta para que sirva con matrículas de fuera de España
    field_matricula= ft.TextField(label="Matricula", width=250,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[A-Za-z0-9]*$"))

    field_propietario = ft.TextField(label="Propietario",width=250)

    field_dropdown_tipo = ft.Dropdown(label="Tipo de vehiculo", width=250, value="Coche",  # Coche como predeterminado
        options=[
            ft.dropdown.Option("Coche"),
            ft.dropdown.Option("Moto"),
            ft.dropdown.Option("Camión")
        ]
    )

    # ACCIÓN DEL BOTÓN
    def add_vehiculo_clicado(e):
        matricula = field_matricula.value.strip().upper()
        propietario = field_propietario.value.strip()
        tipo = field_dropdown_tipo.value

        if not matricula or not propietario:
            page.open(
                ft.SnackBar(ft.Text("Los campos Matrícula y Propietario son obligatorios."), bgcolor=ft.Colors.RED_800))
            page.update()
            return
        vehiculo = Vehiculo(matricula, propietario, tipo)

        if control.add_vehiculo(vehiculo):
            page.open(ft.SnackBar(ft.Text(f"Acceso autorizado para el vehículo con matrícula {matricula}.")))

            # Limpiar formulario
            field_matricula.value = ""
            field_propietario.value = ""
            field_dropdown_tipo.value = "Coche"
        else:
            page.open(ft.SnackBar(ft.Text(f"El vehículo con matrícula {matricula} ya estaba autorizado."),
                                  bgcolor=ft.Colors.RED_800))

        page.update()

    # CARD
    registro_card = ft.Card(
        elevation=8,
        expand=True,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Registro de vehículos autorizados", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    field_matricula,
                    field_propietario,
                    field_dropdown_tipo,
                    ft.ElevatedButton(
                        "Añadir vehículo",
                        icon=ft.Icons.ADD_TASK_ROUNDED,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        on_click=add_vehiculo_clicado,
                    )
                ]
            )
        )
    )
    return registro_card

# FORMULARIO DE ACCESO
def crear_form_acceso(page, tabla_accesos, grafico_actual):

    # CAMPOS
    field_matricula = ft.TextField(label="Matricula", width=250,
        input_filter=ft.InputFilter(allow=True, regex_string=r"^[A-Za-z0-9]*$"))

    texto_resultado = ft.Text()

    container_resultado = ft.Container(
        texto_resultado,
        visible=False,
        padding=10,
        border_radius=5,
        width=250,
        alignment=ft.alignment.center_left,
        bgcolor=ft.Colors.BLACK12
    )

    # ACCIÓN DEL BOTÓN
    def control_acceso_clicado(e):
        matricula = field_matricula.value.strip().upper()

        if not matricula:
            page.open(
                ft.SnackBar(ft.Text("Introduce una matrícula para comprobar el acceso"), bgcolor=ft.Colors.RED_800))
            page.update()
            return

        container_resultado.visible = True
        texto_resultado.value = "COMPROBANDO..."
        texto_resultado.color = ft.Colors.BLUE_GREY_400
        texto_resultado.weight = ft.FontWeight.BOLD
        container_resultado.bgcolor = ft.Colors.BLUE_GREY_100
        field_matricula.value = ""
        page.update()

        time.sleep(0.5)  # cargando

        if control.comprobar(matricula):
            texto_resultado.value = f"Acceso permitido a {matricula}"
            resultado = "Permitido"
            texto_resultado.color = ft.Colors.GREEN_700
            container_resultado.bgcolor = ft.Colors.GREEN_100

        else:
            texto_resultado.value = f"Acceso denegado a {matricula}"
            resultado = "Denegado"
            texto_resultado.color = ft.Colors.RED_700
            container_resultado.bgcolor = ft.Colors.RED_100

        control.add_registro(matricula, resultado)
        actualizar_elementos(page,tabla_accesos, grafico_actual)

        page.update()

    # CARD DEL FORM DE ACCESO
    control_acceso_card = ft.Card(
        elevation=8,
        expand=True,

        height=315,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Control de acceso", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    field_matricula,
                    ft.ElevatedButton(
                        "Comprobar acceso",
                        icon=ft.Icons.FACT_CHECK_OUTLINED,
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                        on_click=control_acceso_clicado,
                    ),
                    container_resultado  # Contenedor que muestra el resultado
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
        )
    )
    return control_acceso_card


# GRÁFICO
def crear_grafico() -> ft.PieChart:
    # por cada registro en la lista de registros cuento el valor de la clave resultado, si se repite suma 1 (Permitido o Denegado)
    # ejemplo: conteo = {'Permitido': 2, 'Denegado': 1}
    conteo = collections.Counter(registro["resultado"] for registro in control.registro_accesos)

    accesos_totales = sum(conteo.values()) # suma de todos los valores del diccionario conteo

    if accesos_totales == 0:
        return ft.PieChart()

    # si permitido o denegado no existe devolverá 0
    permitidos = conteo.get("Permitido", 0)
    denegados = conteo.get("Denegado", 0)

    # me guardo una lista para las secciones (Permitido/Denegado)
    secciones = []
    estilo_textos = ft.TextStyle(color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16)
    # SECCIÓN DE PERMITIDOS
    if permitidos > 0:
        porcentaje = (permitidos / accesos_totales) * 100
        secciones.append(
            ft.PieChartSection(
                permitidos, # la cantidad (int)
                title=f"{porcentaje:.1f}%\n({permitidos})",
                title_style=estilo_textos,
                color=ft.Colors.GREEN,
                radius=60,
            )
        )

    # SECCIÓN DE DENEGADOS
    if denegados > 0:
        porcentaje = (denegados / accesos_totales) * 100
        secciones.append(
            ft.PieChartSection(
                value=denegados,
                title=f"{porcentaje:.1f}%\n({denegados})",
                title_style=estilo_textos,
                color=ft.Colors.RED,
                radius=60,
            )
        )

    return ft.PieChart(
        sections=secciones,

        center_space_radius=45,
    )

grafico = crear_grafico()
grafico_card = ft.Card(
        elevation=8,
        expand=True,
        content=ft.Container(
            padding=25,
            expand=True,
            content=ft.Column(
                [
                    ft.Text("Estadísticas de Acceso", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    grafico
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
    )

# PARA IR ACTUALIZANDO LA TABLA Y EL GRÁFICO
def actualizar_elementos(page, tabla_accesos, grafico_actual):

    # ACTUALIZAR TABLA
    registro = control.registro_accesos[0]

    resultado = registro["resultado"]

    # Pongo el color adecuado dependiendo del resultado del intento de acceso
    if resultado == "Permitido":
        color_texto = ft.Colors.GREEN_700
        color_fondo = ft.Colors.GREEN_100
    else:
        color_texto = ft.Colors.RED_700
        color_fondo = ft.Colors.RED_100

    nueva_row = ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(registro["fecha_hora"], weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text(registro["matricula"], weight=ft.FontWeight.BOLD)),
            ft.DataCell(
                ft.Container(
                    ft.Text(
                        resultado,
                        weight=ft.FontWeight.BOLD,
                        color=color_texto
                    ),
                    padding=5,
                    border_radius=5,
                    bgcolor=color_fondo
                )
            )
        ]
    )

    # añado la fila pero al principio
    tabla_accesos.controls[0].rows.insert(0, nueva_row)

    # ACTUALIZAR GRÁFICO
    nuevo_grafico = crear_grafico()
    grafico_actual.sections = nuevo_grafico.sections

    page.update()

def main(page: ft.Page):
    page.title = "Control de acceso de vehículos"
    page.padding = 20

    # TABLA ACCESOS
    tabla_accesos = ft.Column(
        controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Fecha y hora", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Resultado", weight=ft.FontWeight.BOLD)),
                ],
                rows=[],  # se llena al inicializar y al ir actualizando la tabla
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK12),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK12),
                heading_row_color=ft.Colors.BLUE_GREY_100,
                width=1600,
            ),
        ],
        # para que funcione el scroll hay que definir la altura
        height=350,
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    # Para inicializar la tabla con los datos existentes de REGISTRO_ACCESOS
    def inicializar_tabla():
        for registro in control.registro_accesos:

            resultado_str = registro["resultado"]

            if resultado_str == "Permitido":
                resultado = ft.Container(
                    ft.Text(
                        resultado_str,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700
                    ),
                    padding=5,
                    border_radius=5,
                    bgcolor=ft.Colors.GREEN_100
                )
            else:
                resultado = ft.Container(
                    ft.Text(
                        resultado_str,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_700
                    ),
                    padding=5,
                    border_radius=5,
                    bgcolor=ft.Colors.RED_100
                )

            tabla_accesos.controls[0].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(registro["fecha_hora"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(registro["matricula"], weight=ft.FontWeight.BOLD)),
                        ft.DataCell(resultado),
                    ]
                )
            )

    top_row = ft.Row([crear_form_registro(page),crear_form_acceso(page, tabla_accesos, grafico)],spacing=30)


    bottom_row = ft.Row(
        [
            tabla_accesos,
            grafico_card,
        ],
        spacing=30,
    )

    inicializar_tabla()
    main_column = ft.Column(
        [
            top_row,
            ft.Divider(thickness=3),
            bottom_row,
        ]
    )
    page.add(main_column)
ft.app(main)
