import sqlite3
from pathlib import Path


class DBManager:
    def __init__(self, path=None):
        if path is None:
            base_dir = Path.cwd() 
            path = base_dir / "storage" / "data" / "database.db"
        self.path = Path(path) #ruta a la bd
        self.path.parent.mkdir(parents=True, exist_ok=True) #asegura que exista el directorio
        self.conn = sqlite3.connect(self.path) #conexion a la bd
        self.conn.execute("PRAGMA foreign_keys = ON;") #habilita llaves-foraneas
        self.__create_tables()

    def __create_tables(self):
        cur = self.conn.cursor()
        # EVENTOS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            costo_total REAL,
            descripcion TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT
        );
        """)
        # ASIENTOS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS asientos (
            id_asiento INTEGER PRIMARY KEY AUTOINCREMENT,
            fila TEXT,
            numero INTEGER,
            seccion TEXT
        );
        """)
        # CLIENTES
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT,
            apellidos TEXT,
            correo TEXT,
            telefono TEXT
        );
        """)
        # BOLETOS
        cur.execute("""
        CREATE TABLE IF NOT EXISTS boletos (
            id_boleto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_evento INTEGER NOT NULL,
            id_asiento INTEGER NOT NULL,
            id_cliente INTEGER,
            fecha_compra TEXT,
            precio REAL,
            FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE,
            FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento) ON DELETE CASCADE,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE SET NULL
        );
        """)
        self.conn.commit()

    def get_available_seats(self, id_evento):
        """
        Obtiene los asientos disponibles para un evento específico.
        
        Argumentos:
            id_evento: ID del evento para consultar disponibilidad
            
        Returns:
            Lista de tuplas con (id_asiento, fila, numero, seccion) de asientos disponibles,
            o None si el evento no existe
        """
        cur = self.conn.cursor()
        # Verificar si el evento existe
        cur.execute("SELECT 1 FROM eventos WHERE id_evento = ?", (id_evento,))
        if cur.fetchone() is None:
            return None
        else:
            cur.execute("""
                SELECT a.id_asiento, a.fila, a.numero, a.seccion
                FROM asientos a
                WHERE a.id_asiento NOT IN (
                    SELECT b.id_asiento
                    FROM boletos b
                    WHERE b.id_evento = ?
                )
                ORDER BY a.seccion, a.fila, a.numero
            """, (id_evento,))
            return cur.fetchall()
    
    def create_event(self, tipo, costo_total, descripcion=None, fecha_inicio=None, fecha_fin=None):
        """
        Crea un nuevo evento en la base de datos.
        
        Args:
            tipo: Tipo de evento (ej: "Concierto", "Teatro", "Conferencia")
            costo_total: Costo total del evento
            descripcion: Descripción opcional del evento
            fecha_inicio: Fecha de inicio del evento (formato: "YYYY-MM-DD HH:MM:SS")
            fecha_fin: Fecha de fin del evento (formato: "YYYY-MM-DD HH:MM:SS")
            
        Returns:
            ID del evento creado
        """
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO eventos (tipo, costo_total, descripcion, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?)
        """, (tipo, costo_total, descripcion, fecha_inicio, fecha_fin))
        self.conn.commit()
        return cur.lastrowid

    def create_ticket(self, id_evento, id_asiento, precio, id_cliente=None, fecha_compra=None):
        """
        Crea un nuevo boleto (venta de asiento para un evento).
        
        Args:
            id_evento: ID del evento para el cual se vende el boleto
            id_asiento: ID del asiento a vender
            precio: Precio de venta del boleto
            id_cliente: ID del cliente (opcional)
            fecha_compra: Fecha de compra (formato: "YYYY-MM-DD HH:MM:SS"), se usa la actual si no se especifica
            
        Returns:
            ID del boleto creado, o None si el asiento ya está vendido para ese evento
        """
        cur = self.conn.cursor()
        # Verificar si el asiento ya está vendido para este evento
        cur.execute("""
            SELECT 1 FROM boletos 
            WHERE id_evento = ? AND id_asiento = ?
        """, (id_evento, id_asiento))
        if cur.fetchone() is not None:
            return None  # Asiento ya vendido
        # Usar fecha actual si no se proporciona
        if fecha_compra is None:
            from datetime import datetime
            fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO boletos (id_evento, id_asiento, id_cliente, fecha_compra, precio)
            VALUES (?, ?, ?, ?, ?)
        """, (id_evento, id_asiento, id_cliente, fecha_compra, precio))
        self.conn.commit()
        return cur.lastrowid

    def create_seat(self, fila, numero, seccion):
        """
        Crea un nuevo asiento en la base de datos.
        
        Args:
            fila: Fila del asiento (ej: "A", "B", "C")
            numero: Número del asiento en la fila
            seccion: Sección del auditorio (ej: "A1", "A2")
            
        Returns:
            ID del asiento creado
        """
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO asientos (fila, numero, seccion)
            VALUES (?, ?, ?)
        """, (fila, numero, seccion))
        self.conn.commit()
        return cur.lastrowid

    def get_all_events(self):
        """
        Obtiene todos los eventos de la base de datos.
        
        Returns:
            Lista de tuplas con todos los eventos
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_evento, tipo, costo_total, descripcion, fecha_inicio, fecha_fin
            FROM eventos
            ORDER BY fecha_inicio
        """)
        return cur.fetchall()

    def get_seat_status(self, id_evento):
        """
        Obtiene el estado de todos los asientos para un evento específico.
        
        Args:
            id_evento: ID del evento
            
        Returns:
            Diccionario con id_asiento como clave y estado como valor (True=ocupado, False=disponible)
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_asiento FROM boletos WHERE id_evento = ?
        """, (id_evento,))
        ocupados = {row[0] for row in cur.fetchall()}
        
        cur.execute("SELECT id_asiento FROM asientos")
        todos = cur.fetchall()
        
        return {id_asiento: id_asiento in ocupados for (id_asiento,) in todos}

    def get_all_seats(self):
        """
        Obtiene todos los asientos de la base de datos.
        
        Returns:
            Lista de tuplas con (id_asiento, fila, numero, seccion)
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_asiento, fila, numero, seccion
            FROM asientos
            ORDER BY seccion, fila, numero
        """)
        return cur.fetchall()

    def create_client(self, nombres, telefono, apellidos=None, correo=None):
        """
        Crea un nuevo cliente en la base de datos.
        
        Args:
            nombres: Nombres del cliente (obligatorio)
            telefono: Teléfono del cliente (obligatorio)
            apellidos: Apellidos del cliente (opcional)
            correo: Correo del cliente (opcional)
            
        Returns:
            ID del cliente creado
        """
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO clientes (nombres, apellidos, correo, telefono)
            VALUES (?, ?, ?, ?)
        """, (nombres, apellidos, correo, telefono))
        self.conn.commit()
        return cur.lastrowid
