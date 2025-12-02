import flet as ft
from app_controller import AppController


class VentaView:
    def __init__(self, controller: AppController, page: ft.Page):
        self.controller = controller
        self.page = page
        self.selected_event = None
        self.selected_seats = []  # Lista de IDs de asientos seleccionados
        self.seat_buttons = {}  # Diccionario para referencias a los botones de asientos
        self.event_containers = {}  # Diccionario para referencias a contenedores de eventos
        
        # Colores para estados de asientos
        self.COLOR_DISPONIBLE = ft.Colors.GREEN
        self.COLOR_OCUPADO = ft.Colors.RED
        self.COLOR_SELECCIONADO = ft.Colors.BLUE
        
        # Precio fijo por boleto
        self.PRECIO_BOLETO = 100.0
        
        self.build()

    def build(self):
        """Construye la interfaz completa de la vista de ventas."""
        # Sección 1: Selección de eventos
        self.eventos_row = self._build_eventos_section()
        
        # Sección 2: Selección de asientos
        self.asientos_section = self._build_asientos_section()
        
        # Sección 3: Confirmación de venta
        self.venta_section = self._build_venta_section()
        
        # Contenedor principal
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Eventos Disponibles", size=20, weight=ft.FontWeight.BOLD),
                        self.eventos_row,
                    ]),
                    padding=10,
                ),
                ft.Divider(height=2, color=ft.Colors.WHITE24),
                self.asientos_section,
                ft.Divider(height=2, color=ft.Colors.WHITE24),
                self.venta_section,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _build_eventos_section(self):
        """Construye la sección de selección de eventos."""
        # TODO: Cargar eventos desde el controlador
        # Por ahora, crear un evento de prueba
        evento_prueba = self._create_event_card(
            id_evento=1,
            tipo="Concierto Rock",
            descripcion="Gran concierto de rock en vivo",
            fecha_inicio="2025-12-15 20:00:00",
            fecha_fin="2025-12-15 23:00:00",
            costo_total=5000.0
        )
        
        return ft.Row(
            [evento_prueba],
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )

    def _create_event_card(self, id_evento, tipo, descripcion, fecha_inicio, fecha_fin, costo_total):
        """Crea una tarjeta para un evento."""
        container = ft.Container(
            content=ft.Column(
                [
                    ft.Text(tipo, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Inicio: {fecha_inicio}", size=12),
                    ft.Text(f"Fin: {fecha_fin}", size=12),
                    ft.Text(f"{descripcion}", size=10, italic=True),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=15,
            border_radius=10,
            width=250,
            on_click=lambda e, evt_id=id_evento: self._on_event_selected(evt_id),
            ink=True,
            border=ft.border.all(2, ft.Colors.TRANSPARENT),
        )
        self.event_containers[id_evento] = container
        return container

    def _on_event_selected(self, id_evento):
        """Maneja la selección de un evento."""
        # Si el evento ya está seleccionado, no hacer nada
        if self.selected_event == id_evento:
            return
        
        # Resetear borde del evento anterior
        if self.selected_event and self.selected_event in self.event_containers:
            self.event_containers[self.selected_event].border = ft.border.all(2, ft.Colors.TRANSPARENT)
            self.event_containers[self.selected_event].update()
        
        # Marcar nuevo evento
        self.selected_event = id_evento
        if id_evento in self.event_containers:
            self.event_containers[id_evento].border = ft.border.all(2, ft.Colors.BLUE)
            self.event_containers[id_evento].update()
        
        self.selected_seats.clear()  # Limpiar asientos seleccionados
        self._update_seats_display()
        self._update_info_panel()
        print(f"Evento seleccionado: {id_evento}")

    def _build_asientos_section(self):
        """Construye la sección de selección de asientos."""
        # Panel izquierdo: Información y lista de asientos seleccionados
        self.info_panel = self._build_info_panel()
        
        # Panel derecho: Diagrama de asientos
        self.seats_diagram = self._build_seats_diagram()
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=self.info_panel,
                        width=400,  # 1/3 aproximado de 1280px
                        padding=10,
                    ),
                    ft.VerticalDivider(width=2, color=ft.Colors.WHITE24),
                    ft.Container(
                        content=self.seats_diagram,
                        expand=True,
                        padding=10,
                    ),
                ],
                expand=True,
            ),
        )

    def _build_info_panel(self):
        """Construye el panel de información lateral."""
        self.selected_seats_list = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
        self.total_text = ft.Text("Total: $0.00", size=18, weight=ft.FontWeight.BOLD)
        self.selection_message = ft.Text(
            "⚠️ Selecciona un evento primero",
            size=14,
            color=ft.Colors.ORANGE,
            visible=True,
            weight=ft.FontWeight.BOLD,
        )
        
        return ft.Column(
            [
                ft.Container(
                    content=ft.Text("ASIENTOS SELECCIONADOS", size=20, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.BLUE_GREY_600,
                    padding=20,
                    alignment=ft.alignment.center,
                    border_radius=5,
                ),
                ft.Container(height=39),
                self.selection_message,
                ft.Container(
                    content=self.selected_seats_list,
                    border=ft.border.all(1, ft.Colors.WHITE24),
                    border_radius=5,
                    padding=10,
                    height=380,
                    width=float('inf'),
                ),
                ft.Divider(),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Limpiar selección",
                            icon=ft.Icons.CLEAR_ALL,
                            on_click=lambda e: self._clear_selection(),
                        ),
                        self.total_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
        )

    def _build_seats_diagram(self):
        """Construye el diagrama visual de asientos."""
        # ESCENARIO
        escenario = ft.Container(
            content=ft.Text("ESCENARIO", size=20, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.BLUE_GREY_600,
            padding=20,
            alignment=ft.alignment.center,
            border_radius=5,
        )
        
        # Sección A1 (10x10)
        seccion_a1 = self._build_section_grid("A1")
        
        # Sección A2 (10x10)
        seccion_a2 = self._build_section_grid("A2")
        
        # Sección A3 (10x10)
        seccion_a3 = self._build_section_grid("A3")
        
        return ft.Column(
            [
                escenario,
                ft.Container(height=20),
                ft.Row(
                    [
                        ft.Column([
                            ft.Text("Sección A1", size=14, weight=ft.FontWeight.BOLD),
                            seccion_a1,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=50),
                        ft.Column([
                            ft.Text("Sección A2", size=14, weight=ft.FontWeight.BOLD),
                            seccion_a2,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=50),
                        ft.Column([
                            ft.Text("Sección A3", size=14, weight=ft.FontWeight.BOLD),
                            seccion_a3,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                self._build_legend(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_section_grid(self, seccion):
        """Construye una cuadrícula de asientos para una sección."""
        rows = []
        
        for fila_num in range(1, 11):
            fila_letra = chr(64 + fila_num)  # A, B, C, ..., J
            seat_row = []
            
            for numero in range(1, 11):
                # Calcular ID del asiento (temporal, debe venir de la BD)
                # Sección A1: IDs 1-100, Sección A2: IDs 101-200, Sección A3: IDs 201-300
                if seccion == "A1":
                    base_id = 0
                elif seccion == "A2":
                    base_id = 100
                else:  # A3
                    base_id = 200
                seat_id = base_id + (fila_num - 1) * 10 + numero
                
                seat_btn = ft.IconButton(
                    icon=ft.Icons.CHAIR,
                    icon_color=self.COLOR_DISPONIBLE,
                    icon_size=20,
                    tooltip=f"{seccion}-{fila_letra}{numero}",
                    data={"id": seat_id, "seccion": seccion, "fila": fila_letra, "numero": numero},
                    on_click=lambda e, sid=seat_id: self._on_seat_clicked(sid),
                )
                
                self.seat_buttons[seat_id] = seat_btn
                seat_row.append(seat_btn)
            
            rows.append(ft.Row(seat_row, spacing=2))
        
        return ft.Column(rows, spacing=2)

    def _build_legend(self):
        """Construye la leyenda de colores."""
        return ft.Row(
            [
                ft.Icon(ft.Icons.CHAIR, color=self.COLOR_DISPONIBLE, size=20),
                ft.Text("Disponible", size=12),
                ft.Container(width=20),
                ft.Icon(ft.Icons.CHAIR, color=self.COLOR_OCUPADO, size=20),
                ft.Text("Ocupado", size=12),
                ft.Container(width=20),
                ft.Icon(ft.Icons.CHAIR, color=self.COLOR_SELECCIONADO, size=20),
                ft.Text("Seleccionado", size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _on_seat_clicked(self, seat_id):
        """Maneja el click en un asiento."""
        if self.selected_event is None:
            # Mostrar mensaje de error: debe seleccionar un evento primero
            print("Debe seleccionar un evento primero")
            return
        
        seat_btn = self.seat_buttons[seat_id]
        
        # Verificar si el asiento está ocupado
        if seat_btn.icon_color == self.COLOR_OCUPADO:
            return  # No se puede seleccionar
        
        # Toggle selección
        if seat_id in self.selected_seats:
            # Deseleccionar
            self.selected_seats.remove(seat_id)
            seat_btn.icon_color = self.COLOR_DISPONIBLE
        else:
            # Seleccionar
            self.selected_seats.append(seat_id)
            seat_btn.icon_color = self.COLOR_SELECCIONADO
        
        seat_btn.update()
        self._update_info_panel()

    def _update_seats_display(self):
        """Actualiza el estado visual de todos los asientos según el evento seleccionado."""
        if self.selected_event is None:
            # Resetear todos a disponible
            for seat_btn in self.seat_buttons.values():
                seat_btn.icon_color = self.COLOR_DISPONIBLE
                seat_btn.update()
            return
        
        # TODO: Obtener estado real de asientos desde el controlador
        # Por ahora, todos disponibles
        for seat_btn in self.seat_buttons.values():
            seat_btn.icon_color = self.COLOR_DISPONIBLE
            seat_btn.update()

    def _update_info_panel(self):
        """Actualiza el panel de información con los asientos seleccionados."""
        # Mostrar/ocultar mensaje de selección
        if self.selected_event:
            self.selection_message.visible = False
        else:
            self.selection_message.visible = True
        self.selection_message.update()
        
        self.selected_seats_list.controls.clear()
        
        for seat_id in self.selected_seats:
            seat_btn = self.seat_buttons[seat_id]
            seat_data = seat_btn.data
            
            self.selected_seats_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{seat_data['seccion']}-{seat_data['fila']}{seat_data['numero']}", size=14),
                        ft.Text(f"${self.PRECIO_BOLETO}", size=14),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    padding=8,
                    border_radius=5,
                )
            )
        
        total = len(self.selected_seats) * self.PRECIO_BOLETO
        self.total_text.value = f"Total: ${total:.2f}"
        
        self.selected_seats_list.update()
        self.total_text.update()

    def _clear_selection(self):
        """Limpia la selección de asientos."""
        for seat_id in self.selected_seats[:]:
            seat_btn = self.seat_buttons[seat_id]
            if seat_btn.icon_color == self.COLOR_SELECCIONADO:
                seat_btn.icon_color = self.COLOR_DISPONIBLE
                seat_btn.update()
        
        self.selected_seats.clear()
        self._update_info_panel()

    def _build_venta_section(self):
        """Construye la sección de confirmación de venta."""
        # Campos del formulario
        self.nombres_field = ft.TextField(label="Nombres *", hint_text="Obligatorio")
        self.apellidos_field = ft.TextField(label="Apellidos", hint_text="Opcional")
        self.telefono_field = ft.TextField(label="Teléfono *", hint_text="Obligatorio")
        self.correo_field = ft.TextField(label="Correo", hint_text="Opcional")
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Datos del Cliente", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.Column([self.nombres_field, self.telefono_field], expand=True),
                            ft.Column([self.apellidos_field, self.correo_field], expand=True),
                        ],
                        spacing=20,
                    ),
                    ft.Container(height=10),
                    ft.Divider(height=2, color=ft.Colors.WHITE24),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Cancelar",
                                color=ft.Colors.WHITE,
                                icon=ft.Icons.CANCEL,
                                bgcolor=ft.Colors.RED_700,
                                on_click=lambda e: self._cancelar_venta(),
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Confirmar Venta",
                                color=ft.Colors.WHITE,
                                icon=ft.Icons.CHECK_CIRCLE,
                                bgcolor=ft.Colors.GREEN_700,
                                on_click=lambda e: self._confirmar_venta(),
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        spacing=20,
                    ),
                ],
                spacing=15,
            ),
            padding=15,
        )

    def _confirmar_venta(self):
        """Confirma y procesa la venta."""
        # Validar que haya evento seleccionado
        if self.selected_event is None:
            self._show_snackbar("⚠️ Debes seleccionar un evento primero", ft.Colors.ORANGE)
            return
        
        # Validar que haya asientos seleccionados
        if len(self.selected_seats) == 0:
            self._show_snackbar("⚠️ Debes seleccionar al menos un asiento", ft.Colors.ORANGE)
            return
        
        # Validar campos obligatorios
        if not self.nombres_field.value or not self.telefono_field.value:
            self._show_snackbar("⚠️ Nombres y teléfono son obligatorios", ft.Colors.ORANGE)
            return
        
        # TODO: Procesar venta a través del controlador
        print(f"Procesando venta:")
        print(f"  Evento: {self.selected_event}")
        print(f"  Asientos: {self.selected_seats}")
        print(f"  Cliente: {self.nombres_field.value}")
        print(f"  Total: ${len(self.selected_seats) * self.PRECIO_BOLETO}")
        
        # Mostrar confirmación
        self._show_snackbar("✅ Venta confirmada y guardada en la base de datos", ft.Colors.GREEN)
        
        # Limpiar todo
        self._reset_all()

    def _cancelar_venta(self):
        """Cancela la venta y limpia todo."""
        self._show_snackbar("❌ Operación cancelada", ft.Colors.RED)
        self._reset_all()

    def _reset_form(self):
        """Resetea el formulario de cliente."""
        self.nombres_field.value = ""
        self.apellidos_field.value = ""
        self.telefono_field.value = ""
        self.correo_field.value = ""
        self.nombres_field.update()
        self.apellidos_field.update()
        self.telefono_field.update()
        self.correo_field.update()

    def _reset_all(self):
        """Resetea todo: formulario, asientos y evento."""
        # Limpiar formulario
        self._reset_form()
        
        # Limpiar asientos seleccionados
        self._clear_selection()
        
        # Deseleccionar evento
        if self.selected_event and self.selected_event in self.event_containers:
            self.event_containers[self.selected_event].border = ft.border.all(2, ft.Colors.TRANSPARENT)
            self.event_containers[self.selected_event].update()
        
        self.selected_event = None
        self._update_info_panel()

    def _show_snackbar(self, message: str, color: str):
        """Muestra un SnackBar con el mensaje y color especificado."""
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()

    def get_content(self):
        """Retorna el contenido principal de la vista."""
        return self.content
