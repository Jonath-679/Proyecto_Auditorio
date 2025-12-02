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
        pass

    def get_available_seats(self, id_evento):
        """Obtiene los asientos disponibles para un evento."""
        pass

    def get_seat_status(self, id_evento):
        """Obtiene el estado de todos los asientos para un evento."""
        pass

    def create_sale(self, id_evento, asientos_ids, cliente_data, precio_unitario):
        """Crea una venta completa con múltiples boletos."""
        pass

    def get_all_seats_by_section(self):
        """Obtiene todos los asientos organizados por sección."""
        pass
