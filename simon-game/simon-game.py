import flet as ft
import random
import asyncio

def simon_button(letra, color, on_click_async, loop):
    return ft.Container(
        content=ft.Text(letra, weight=ft.FontWeight.BOLD, size=22),
        alignment=ft.alignment.center,
        margin=20,
        bgcolor=color,
        height=180,
        border_radius=12,
        ink=True,
        on_click=lambda e: asyncio.run_coroutine_threadsafe(on_click_async(letra), loop),
    col={"xs": 12, "sm": 6}
    )


async def main(page: ft.Page):
    loop = asyncio.get_event_loop()
    page.title = "Simon"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    colores = ["T", "Y", "G", "H"]
    secuencia = []
    indice_usuario = 0
    botones = {}
    reproduciendo = False  # bloquea input mientras se reproduce

    # para mostrar los snackbars de forma compatible con la asincronía
    async def show_snackbar(text: str):
        page.open(ft.SnackBar(ft.Text(text)))
        page.update()

    async def flash(letra):
        original = botones[letra].bgcolor
        botones[letra].bgcolor = ft.Colors.WHITE
        page.update()
        await asyncio.sleep(0.07)
        botones[letra].bgcolor = original
        botones[letra].update()

    async def reproducir_secuencia():
        nonlocal reproduciendo
        reproduciendo = True

        await asyncio.sleep(0.3)

        for letra in secuencia:
            await flash(letra)
            await asyncio.sleep(0.2)

        reproduciendo = False


    async def nueva_ronda():
        letra_nueva = random.choice(colores)
        secuencia.append(letra_nueva)
        await reproducir_secuencia()

    async def usuario_input(letra):
        nonlocal indice_usuario

        # No hace nada si la secuencia está vacía o está reproduciendo una
        if reproduciendo:
            return

        if not secuencia:
            return

        await flash(letra)

        # Comprobar el acierto
        if letra == secuencia[indice_usuario]:
            indice_usuario += 1

            # Si es el último hace una pausa un poco más larga y empieza nueva nueva ronda
            if indice_usuario == len(secuencia):
                # para motivar un poquito
                if len(secuencia) == 3:
                   await show_snackbar("Bien jugado")
                if len(secuencia) == 5:
                    await show_snackbar("Muy buena!")
                if len(secuencia) == 10:
                    await show_snackbar("Que bueno eres!!")
                if len(secuencia) == 15:
                    await show_snackbar("I AM FLIPING BRO 😵‍💫😵‍💫🥴🥴😵")
                if len(secuencia) == 20:
                    await show_snackbar("DEDÍCATE A ESTO TÍO 🤯🤯🤑🤑🥵🥵🥵🥶🥶😵‍💫😵‍‍💫🥴🥴😵😵")
                if len(secuencia) == 25:
                    await show_snackbar("Mis respetos, has superado mi récord 🫡")
                indice_usuario = 0
                await asyncio.sleep(0.4)
                await nueva_ronda()
        else:
            # Si falla reiniciamos todo
            color_original = botones[letra].bgcolor
            # para que se note que ha fallado
            botones[letra].bgcolor = ft.Colors.RED_900
            botones[letra].update()

            page.open(ft.SnackBar(ft.Text("¡Vaya! Has fallado. Toca volver a empezar.")))
            page.update()

            # Restaura el color original después de avisar del fallo
            await asyncio.sleep(1.0)
            botones[letra].bgcolor = color_original
            botones[letra].update()

            secuencia.clear()
            indice_usuario = 0

            # un segundo para que asuma su derrota
            await asyncio.sleep(1)
            await nueva_ronda()

    async def teclado(e: ft.KeyboardEvent):
        key = e.key.upper()
        if key in colores:
            await usuario_input(key)

    page.on_keyboard_event = teclado

    # UI
    botones["T"] = simon_button("T", ft.Colors.RED_400, usuario_input, loop)
    botones["Y"] = simon_button("Y", ft.Colors.YELLOW_400,usuario_input, loop)
    botones["G"] = simon_button("G", ft.Colors.BLUE_400, usuario_input, loop)
    botones["H"] = simon_button("H", ft.Colors.GREEN_400, usuario_input, loop)

    page.add(
        ft.Card(
            elevation=10,
            margin=20,
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Simón", size=28, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        padding=15,
                        bgcolor=ft.Colors.GREY_300,
                        border_radius=ft.border_radius.only(12, 12, 0, 0),
                    ),
                    ft.ResponsiveRow(
                        [botones["T"], botones["Y"], botones["G"], botones["H"]],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ]
            ),
        )
    )

    page.update()

    # para que empiece el juego
    await nueva_ronda()
    await show_snackbar("El juego de Simón ha comenzado. ¡Repite la secuencia!")
    page.update()


ft.app(target=main)
