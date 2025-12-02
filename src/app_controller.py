from db_manager import DBManager


class AppController:
    def __init__(self):
        self.db = DBManager()
        self._initialize_seats()
        self.__initialize_demo_event()

    def _initialize_seats(self):
        """Crea los asientos del auditorio si no existen."""
        # Verificar si ya existen asientos
        existing_seats = self.db.get_all_seats()
        if len(existing_seats) > 0:
            return  # Ya hay asientos creados
        
        # Crear asientos para sección A1 (10x10)
        for fila_num in range(1, 11):
            fila = chr(64 + fila_num)  # A, B, C, ..., J
            for numero in range(1, 11):
                self.db.create_seat(fila, numero, "A1")
        
        # Crear asientos para sección A2 (10x10)
        for fila_num in range(1, 11):
            fila = chr(64 + fila_num)  # A, B, C, ..., J
            for numero in range(1, 11):
                self.db.create_seat(fila, numero, "A2")
        
        # Crear asientos para sección A3 (10x10)
        for fila_num in range(1, 11):
            fila = chr(64 + fila_num)  # A, B, C, ..., J
            for numero in range(1, 11):
                self.db.create_seat(fila, numero, "A3")

    def __initialize_demo_event(self):
        """Crea un evento de prueba si no existen eventos."""
        eventos = self.db.get_all_events()
        if len(eventos) > 0:
            return  # Ya hay eventos creados
        
        # Crear evento de prueba
        self.db.create_event(
            tipo="Concierto Rock",
            costo_total=5000.0,
            descripcion="Gran concierto de rock en vivo",
            fecha_inicio="2025-12-15 20:00:00",
            fecha_fin="2025-12-15 23:00:00"
        )

    # Metodos llamados desde la UI (main.py)
    
    def get_all_events(self):
        """Obtiene todos los eventos."""
        return self.db.get_all_events()
    
    def get_all_seats(self):
        """Obtiene todos los asientos."""
        return self.db.get_all_seats()

    def get_available_seats(self, id_evento):
        """Obtiene los asientos disponibles para un evento."""
        return self.db.get_available_seats(id_evento)

    def get_seat_status(self, id_evento):
        """Obtiene el estado de todos los asientos para un evento."""
        return self.db.get_seat_status(id_evento)

    def create_sale(self, id_evento, asientos_ids, cliente_data, precio_unitario):
        """
        Crea una venta completa con múltiples boletos.
        
        Args:
            id_evento: ID del evento
            asientos_ids: Lista de IDs de asientos a vender
            cliente_data: Diccionario con datos del cliente {nombres, telefono, apellidos, correo}
            precio_unitario: Precio por boleto
            
        Returns:
            Tupla (success, message, client_id, ticket_ids)
            - success: True si la venta fue exitosa, False en caso contrario
            - message: Mensaje descriptivo del resultado
            - client_id: ID del cliente creado (o None si falló)
            - ticket_ids: Lista de IDs de boletos creados (o lista vacía si falló)
        """
        from datetime import datetime
        
        try:
            # Verificar disponibilidad de todos los asientos ANTES de crear nada
            seat_status = self.get_seat_status(id_evento)
            for seat_id in asientos_ids:
                if seat_status.get(seat_id, False):
                    return (False, f"El asiento {seat_id} ya está ocupado", None, [])
            
            # Crear cliente
            id_cliente = self.db.create_client(
                nombres=cliente_data.get('nombres'),
                telefono=cliente_data.get('telefono'),
                apellidos=cliente_data.get('apellidos'),
                correo=cliente_data.get('correo')
            )
            
            if id_cliente is None:
                return (False, "Error al crear el cliente", None, [])
            
            # Crear boletos para cada asiento
            fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticket_ids = []
            
            for id_asiento in asientos_ids:
                id_boleto = self.db.create_ticket(
                    id_evento=id_evento,
                    id_asiento=id_asiento,
                    precio=precio_unitario,
                    id_cliente=id_cliente,
                    fecha_compra=fecha_compra
                )
                
                if id_boleto is None:
                    # Si un asiento ya está vendido (condición de carrera)
                    return (False, f"Error: el asiento {id_asiento} fue vendido durante la transacción", id_cliente, ticket_ids)
                
                ticket_ids.append(id_boleto)
            
            return (True, f"Venta exitosa: {len(ticket_ids)} boleto(s) vendido(s)", id_cliente, ticket_ids)
            
        except Exception as e:
            return (False, f"Error en la venta: {str(e)}", None, [])

    def get_all_seats_by_section(self):
        """
        Obtiene todos los asientos organizados por sección.
        
        Returns:
            Diccionario con secciones como claves y listas de asientos como valores
            Ejemplo: {"A1": [(1, "A", 1), (2, "A", 2), ...], "A2": [...], "A3": [...]}
        """
        all_seats = self.db.get_all_seats()
        sections = {}
        
        for id_asiento, fila, numero, seccion in all_seats:
            if seccion not in sections:
                sections[seccion] = []
            sections[seccion].append((id_asiento, fila, numero))
        
        return sections
