import hashlib
import os
from datetime import datetime

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a hash."""
    return hash_password(password) == hashed_password

def generate_ticket(user_name: str, bus_route: str, date_time: str, seat_number: str, booking_id: int) -> str:
    """
    Generates a digital ticket as a .txt file.
    Saves it in the 'tickets' directory and returns the file path.
    """
    tickets_dir = "tickets"
    if not os.path.exists(tickets_dir):
        os.makedirs(tickets_dir)
    
    file_path = os.path.join(tickets_dir, f"Ticket_{booking_id}.txt")
    
    ticket_content = f"""
========================================
         BUS RESERVATION TICKET         
========================================
Booking ID  : {booking_id}
Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
Passenger   : {user_name}
Route       : {bus_route}
Date & Time : {date_time}
Seat Number : {seat_number}
========================================
    Thank you for choosing our service!
========================================
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ticket_content)
        
    return file_path
