# Bus Reservation System

A modern, secure, and functional Bus Reservation System built in Python using **CustomTkinter** for a sleek graphical user interface (GUI) and **SQLite3** for robust database management. 

## Features

*   **Modern GUI**: A single-window application with smooth frame switching, built with CustomTkinter.
*   **Secure User Authentication**:
    *   Separate roles for **Admins** and **Customers**.
    *   User passwords are securely hashed before being stored in the database.
    *   The primary admin account is securely mapped from environment variables.
*   **Admin Dashboard**:
    *   Manage buses (Add, Edit, Delete).
    *   Manage system administrators.
    *   View a master list of all current passenger bookings.
*   **Customer Dashboard**:
    *   Search and filter available buses based on source and destination routes.
    *   Interactive seat booking system.
    *   Automatically generate and save text-based digital tickets to the `tickets/` directory.

## Project Structure

*   `main.py`: The entry point of the application. Initializes the application container, database, and handles frame routing.
*   `ui_frames.py`: Contains the actual UI classes and logic for each screen (Login, Register, Admin Dashboard, Customer Dashboard).
*   `database.py`: Handles all SQLite database interactions, tables (Users, Buses, Bookings), and data population.
*   `utils.py`: Contains all the utility functions, such as SHA-256 password hashing.

## Prerequisites

*   [Python 3.8+](https://www.python.org/downloads/)
*   Virtual environment tools

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Git-ARoy/Bus-Reservation-System.git
    cd Bus-Reservation-System
    ```

2.  **Set up a Virtual Environment (Recommended):**
    MacOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    Windows:
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    To ensure hardcoded credentials are not kept in the source code, create a `.env` file in the root directory to define your default admin credentials.
    ```env
    ADMIN_USERNAME=admin
    ADMIN_PASSWORD=admin123
    ```

5.  **Run the application:**
    ```bash
    python main.py
    ```

## Usage Flow

*   **First Run**: Upon executing `main.py`, the system will automatically initialize the `bus_reservation.db` SQLite database and create a default admin user using the variables provided in your `.env` file.
*   **Admin Setup**: Log in with the configured admin credentials. Create upcoming bus details mapping source and destination cities, dates, times, and total seat capacities.
*   **Customer Booking**: Complete the registration form for a new customer account, log in, search for available routes created by the admin, and book an available seat. A digital ticket will be subsequently generated in your local `tickets/` folder.

## Built With

*   [Python](https://www.python.org/) - Primary language
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) - Modern Python UI-library based on Tkinter
*   [SQLite3](https://docs.python.org/3/library/sqlite3.html) - DB-API 2.0 interface for SQLite databases
*   [python-dotenv](https://pypi.org/project/python-dotenv/) - Secret management tool to load environment variables
