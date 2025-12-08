import flet as ft
import random

FORMAS_TEXTO = ["Cuadrado", "Círculo"]

# relaciona el color con un string para compararlo
COLORES = {
    "Azul": ft.Colors.BLUE_700,
    "Rojo": ft.Colors.RED_700
}

# saco las keys (una lista con los string azul y rojo)
COLORES_STR = list(COLORES.keys())


correct_answer = None
current_mode = None

def main(page: ft.Page):
    page.title = "Reto Psicológico"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT

    output_text = ft.Text("", size=32, weight=ft.FontWeight.BOLD)
    output_container = ft.Container(
        content=output_text,
        alignment=ft.alignment.center,
        height=120,
        width=300,
        border=ft.border.all(3, ft.Colors.GREY_300),
        border_radius=15,
        padding=10
    )

    reset_button = ft.OutlinedButton(
        text="Cambiar Modo",
        icon=ft.Icons.RESTART_ALT,
        on_click=lambda e: reset_game(),
    )


    # MANEJAR EL TECLADO
    # referencias a los contenedores
    figura_q_ref = ft.Ref[ft.Container]()
    figura_p_ref = ft.Ref[ft.Container]()

    # en esta función simulo el click del ratón cuando se pulsa la tecla Q o P
    def tecla_pulsada(e: ft.KeyboardEvent):
        if current_mode:
            if e.key.upper() == "Q":
                figure_click(ft.ControlEvent(figura_q_ref.current,'click', "Q", figura_q_ref.current, page))
            elif e.key.upper() == "P":
                figure_click(ft.ControlEvent(figura_p_ref.current,'click', "P", figura_p_ref.current, page))

    page.on_keyboard_event = tecla_pulsada

    # genera un output aleatorio según el modo de juego que haya elegido el usuario
    def generate_task():
        # necesario redefinirla con global
        global correct_answer

        # color del texto en String (saco uno random de la lista)
        text_color_str = random.choice(COLORES_STR)

        # color del texto
        text_color = COLORES[text_color_str]

        if current_mode == "Figuras":
            figure_text = random.choice(FORMAS_TEXTO)

            output_text.value = figure_text
            output_text.color = text_color
            correct_answer = "Q" if figure_text == "Cuadrado" else "P"
        else:
            figure_text = random.choice(FORMAS_TEXTO)
            output_text.value = figure_text
            output_text.color = text_color
            correct_answer = "Q" if text_color_str == "Azul" else "P"

        page.update()

    # verifica la respuesta del usuario
    def figure_click(e):
        global correct_answer

        if not current_mode:
            page.open(ft.SnackBar(ft.Text("¡Debes elegir el modo de juego!")))
            return

        clicked_figure_id = e.control.content.value

        if clicked_figure_id != correct_answer:
            page.open(ft.SnackBar(ft.Text("❌ ¡Respuesta Incorrecta!"), duration=400)) # poca duración del snackbar  para que no moleste

        generate_task()

    def reset_game():
        global current_mode
        current_mode = None
        output_text.value = ""

        page.clean()
        page.add(
            main_card,
            options_section,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            start_button,
        )
        page.update()

    def start_game(e):
        global current_mode

        selected_option = option_group.value # Figuras/Colores

        if not selected_option:
            page.open(ft.SnackBar(ft.Text("¡Debes elegir el modo de juego!")))
            page.update()
            return

        current_mode = selected_option

        page.clean()

        # pantalla de cuando el usuario está jugando
        page.add(
            main_card,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            output_container,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            reset_button,
        )
        page.update()

        generate_task()

    # Cuadrado azul (Q)
    figura_q = ft.Container(
        content=ft.Text("Q", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.alignment.center,
        expand=True,
        aspect_ratio=1,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.all(10),
        ink=True,
        on_click=figure_click,
        ref=figura_q_ref
    )

    # Círculo rojo (P)
    figura_p = ft.Container(
        content=ft.Text("P", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        alignment=ft.alignment.center,
        expand=True,
        aspect_ratio=1,
        bgcolor=ft.Colors.RED_700,
        border_radius=ft.border_radius.all(100000),
        ink=True,
        on_click=figure_click,
        ref=figura_p_ref
    )

    # Contenedor de las figuras
    figuras_container = ft.Container(
        content=
        ft.Row(
            [figura_q, figura_p],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        padding=30,
        width=500
    )

    # Radio buttons
    option_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Figuras", label="Figuras"),
            ft.Radio(value="Colores", label="Colores"),
        ], spacing=50, alignment=ft.MainAxisAlignment.CENTER),
    )

    options_section = ft.Column([
        ft.Text("Elige una opción:", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(content=option_group, padding=ft.padding.only(top=10)),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # card principal con le título y el contenedor con  las figuras
    main_card = ft.Card(
        elevation=10,
        margin=20,
        content=
        ft.Column(
            [
                ft.Container(
                    content=ft.Text("Reto Psicológico", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    alignment=ft.alignment.center,
                    padding=15,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=ft.border_radius.only(12, 12, 0, 0),
                ),
                figuras_container,
                ft.Divider(height=0, color=ft.Colors.TRANSPARENT),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    # button para empezar a jugar
    start_button = ft.ElevatedButton(
        text="Confirmar selección y empezar a jugar",
        icon=ft.Icons.CHECK,
        on_click=start_game,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
            bgcolor=ft.Colors.BLUE_ACCENT_700,
            color=ft.Colors.WHITE
        )
    )

    # estructura inicial
    page.add(
        main_card,
        options_section,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        start_button,
    )


ft.app(target=main)