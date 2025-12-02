import flet as ft
from app_controller import AppController


def main(page: ft.Page):
    # Configuracion de la ventana
    page.title = "PROYECTO AUDITORIO [BD]"
    page.bgcolor = ft.Colors.BLUE_GREY_700
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1280
    page.window.height = 720
    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variables y objetos
    controller = AppController()
    locked_admin = True
    prev_index = 0

    # Campo de contraseña y diálogo
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, on_submit=lambda e: check_password())
    dialog = ft.AlertDialog(
        title=ft.Text("ADMINISTRACION"),
        content=ft.Container(
            width=200,
            height=100,
            content=ft.Column(
                [password_field],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=10,
        ),
        actions=[
            ft.ElevatedButton("Cancelar", on_click=lambda e: close_dialog(False)),
            ft.ElevatedButton("Entrar", on_click=lambda e: check_password()),
        ]
    )

    def close_dialog(success: bool):
        dialog.open = False
        tabs.selected_index = 0
        prev_index = 0
        page.update()

    def check_password():
        nonlocal locked_admin, prev_index
        if password_field.value == "contraseña":
            locked_admin = False
            password_field.value = ""
            update_admin_tab_content()
            tabs.selected_index = 1
            prev_index = 1
            dialog.open = False
            page.update()
        else:
            snackbar = ft.SnackBar(content=ft.Text("Contraseña incorrecta"))
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

    # Contenidos de las pestañas
    venta_content = ft.Column([
        ft.Text("Pestaña VENTA", size=24),
        ft.Text("Aquí iría la interfaz de ventas..."),
    ], alignment=ft.MainAxisAlignment.START)

    admin_content = ft.Column([
        ft.Text("ADMINISTRACION", size=24),
        ft.Text("Sección administrativa. Acceso autorizado."),
        ft.ElevatedButton("Salir a VENTA", icon=ft.Icons.EXIT_TO_APP, on_click=lambda e: exit_admin()),
    ], alignment=ft.MainAxisAlignment.START)

    def exit_admin():
        nonlocal locked_admin, prev_index
        locked_admin = True
        tabs.selected_index = 0
        prev_index = 0
        update_admin_tab_content()
        page.update()
    
    def update_admin_tab_content():
        """Actualiza el contenido de la pestaña ADMINISTRACION según el estado de bloqueo"""
        if locked_admin:
            admin_tab_container.content = ft.Container(
                content=ft.Text("SECCIÓN BLOQUEADA", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREY_700,
                padding=20,
                alignment=ft.alignment.center
            )
            # Recrear el tab con icono de bloqueado
            tabs.tabs[1] = ft.Tab(
                text="ADMINISTRACION 🔒",
                icon=ft.Icons.LOCK,
                content=admin_tab_container,
            )
        else:
            admin_tab_container.content = admin_content
            # Recrear el tab con icono de desbloqueado
            tabs.tabs[1] = ft.Tab(
                text="ADMINISTRACION ✓",
                icon=ft.Icons.LOCK_OPEN,
                content=admin_tab_container,
            )

    # Control para manejar eventos de cambio de pestaña
    def on_tabs_change(e):
        nonlocal prev_index
        new_index = e.control.selected_index
        # Si intentan entrar a ADMINISTRACION y está bloqueada, abrir diálogo
        if new_index == 1 and locked_admin:
            dialog.open = True
            page.update()
        else:
            prev_index = new_index

    # Contenedor para el tab de ADMINISTRACION (para actualización dinámica)
    admin_tab_container = ft.Container(
        content=ft.Container(
            content=ft.Text("SECCIÓN BLOQUEADA", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREY_700,
            padding=20,
            alignment=ft.alignment.center
        ),
        padding=20
    )

    # Definición de las pestañas, con icono visual para indicar bloqueo
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        on_change=on_tabs_change,
        tabs=[
            ft.Tab(text="VENTA", content=ft.Container(content=venta_content, padding=20)),
            ft.Tab(
                text="ADMINISTRACION 🔒",
                icon=ft.Icons.LOCK,
                content=admin_tab_container,
            ),
        ],
        expand=1
    )

    page.overlay.append(dialog)
    page.add(tabs)

ft.app(main)
