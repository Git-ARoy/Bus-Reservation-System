import sqlite3
import os
from utils import hash_password

class DatabaseManager:
    def __init__(self, db_path="bus_reservation.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        """Returns a database connection with dict-like rows."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database schema if tables don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
                )
            ''')
            
            # Buses Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Buses (
                    bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    total_seats INTEGER NOT NULL
                )
            ''')
            
            # Bookings Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    bus_id INTEGER NOT NULL,
                    seat_number TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES Users(id),
                    FOREIGN KEY(bus_id) REFERENCES Buses(bus_id)
                )
            ''')
            
            # Create a default admin user if none exists
            cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role = 'admin'")
            if cursor.fetchone()['count'] == 0:
                admin_user = os.environ.get("ADMIN_USERNAME", "admin")
                admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
                admin_hash = hash_password(admin_pass)
                cursor.execute(
                    "INSERT INTO Users (username, password_hash, role) VALUES (?, ?, ?)",
                    (admin_user, admin_hash, "admin")
                )
            conn.commit()

    # --- Authentication ---
    def register_user(self, username, password, role="customer"):
        """Registers a new user. Returns True if successful, False if username exists."""
        hashed = hash_password(password)
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO Users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, hashed, role)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        """Logs in a user. Returns a dict with user details or None if invalid."""
        hashed = hash_password(password)
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, username, role FROM Users WHERE username = ? AND password_hash = ?",
                (username, hashed)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def get_all_admins(self):
        """Returns all admin users."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT id, username, role FROM Users WHERE role = 'admin' ORDER BY username")
            return [dict(row) for row in cursor.fetchall()]

    def delete_user(self, user_id):
        """Deletes a user by their ID."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM Users WHERE id = ?", (user_id,))
            conn.commit()

    # --- Bus Management ---
    def add_bus(self, source, destination, date, time, total_seats):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO Buses (source, destination, date, time, total_seats) VALUES (?, ?, ?, ?, ?)",
                (source, destination, date, time, total_seats)
            )
            conn.commit()

    def get_all_buses(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM Buses ORDER BY date, time")
            return [dict(row) for row in cursor.fetchall()]

    def search_buses(self, source, destination):
        with self.get_connection() as conn:
            query = "SELECT * FROM Buses WHERE source LIKE ? AND destination LIKE ? ORDER BY date, time"
            cursor = conn.execute(query, (f"%{source}%", f"%{destination}%"))
            return [dict(row) for row in cursor.fetchall()]
            
    def get_bus_by_id(self, bus_id):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM Buses WHERE bus_id = ?", (bus_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_bus(self, bus_id, source, destination, date, time, total_seats):
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE Buses 
                   SET source = ?, destination = ?, date = ?, time = ?, total_seats = ? 
                   WHERE bus_id = ?""",
                (source, destination, date, time, total_seats, bus_id)
            )
            conn.commit()

    def delete_bus(self, bus_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM Buses WHERE bus_id = ?", (bus_id,))
            # Cascade delete bookings if needed, but for now just delete the bus.
            conn.execute("DELETE FROM Bookings WHERE bus_id = ?", (bus_id,))
            conn.commit()

    # --- Booking Management ---
    def book_seat(self, user_id, bus_id, seat_number):
        """Books a seat and returns the booking_id, or None if already booked."""
        with self.get_connection() as conn:
            # Check if seat is already booked
            cursor = conn.execute(
                "SELECT booking_id FROM Bookings WHERE bus_id = ? AND seat_number = ?",
                (bus_id, seat_number)
            )
            if cursor.fetchone():
                return None  # Seat taken
                
            cursor = conn.execute(
                "INSERT INTO Bookings (user_id, bus_id, seat_number) VALUES (?, ?, ?)",
                (user_id, bus_id, seat_number)
            )
            conn.commit()
            return cursor.lastrowid

    def get_booked_seats(self, bus_id):
        """Returns a list of seat numbers already booked for a specific bus."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT seat_number FROM Bookings WHERE bus_id = ?", (bus_id,))
            return [row['seat_number'] for row in cursor.fetchall()]

    def get_all_bookings(self):
        """Returns all passenger bookings for the Master View."""
        with self.get_connection() as conn:
            query = """
                SELECT 
                    b.booking_id, u.username, 
                    bus.source, bus.destination, bus.date, bus.time, 
                    b.seat_number
                FROM Bookings b
                JOIN Users u ON b.user_id = u.id
                JOIN Buses bus ON b.bus_id = bus.bus_id
                ORDER BY b.booking_id DESC
            """
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]
