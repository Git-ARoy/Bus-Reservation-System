import customtkinter as ctk
from tkinter import messagebox
from utils import generate_ticket

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller

        # Title
        self.label = ctk.CTkLabel(self, text="Bus Reservation System", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(50, 20))
        
        self.subtitle = ctk.CTkLabel(self, text="Login to your account", font=ctk.CTkFont(size=18))
        self.subtitle.pack(pady=(0, 30))

        # Inputs
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        # Buttons
        self.login_btn = ctk.CTkButton(self, text="Login", width=250, command=self.login)
        self.login_btn.pack(pady=(20, 10))

        self.register_btn = ctk.CTkButton(self, text="Create Account", width=250, fg_color="transparent", 
                                          border_width=1,text_color=("gray10", "#DCE4EE"), 
                                          command=lambda: self.controller.show_frame("RegisterFrame"))
        self.register_btn.pack(pady=10)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        user = self.controller.db.login_user(username, password)
        if user:
            self.controller.current_user = user
            # Clear fields
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            
            # Route based on role
            if user['role'] == 'admin':
                self.controller.show_frame("AdminDashboard")
            else:
                self.controller.show_frame("CustomerDashboard")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller

        # Title
        self.label = ctk.CTkLabel(self, text="Create an Account", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(50, 30))

        # Inputs
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*", width=250)
        self.confirm_password_entry.pack(pady=10)

        # Buttons
        self.register_btn = ctk.CTkButton(self, text="Register", width=250, command=self.register)
        self.register_btn.pack(pady=(20, 10))

        self.back_btn = ctk.CTkButton(self, text="Back to Login", width=250, fg_color="transparent", 
                                      border_width=1, text_color=("gray10", "#DCE4EE"),
                                      command=lambda: self.controller.show_frame("LoginFrame"))
        self.back_btn.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_password_entry.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        success = self.controller.db.register_user(username, password, role="customer")
        if success:
            messagebox.showinfo("Success", "Account created successfully. Please login.")
            # Clear fields
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", "Username already exists.")


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Admin Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left")
        
        self.logout_btn = ctk.CTkButton(self.header_frame, text="Logout", width=100, command=self.logout)
        self.logout_btn.pack(side="right")

        # Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.tab_manage = self.tabview.add("Manage Buses")
        self.tab_master = self.tabview.add("Master View")
        self.tab_admins = self.tabview.add("Manage Admins")
        
        self.setup_manage_buses_tab()
        self.setup_master_view_tab()
        self.setup_manage_admins_tab()

    def setup_manage_buses_tab(self):
        # Add Bus Form
        self.add_bus_frame = ctk.CTkFrame(self.tab_manage)
        self.add_bus_frame.pack(fill="x", pady=10)
        
        self.source_entry = ctk.CTkEntry(self.add_bus_frame, placeholder_text="Source")
        self.source_entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.dest_entry = ctk.CTkEntry(self.add_bus_frame, placeholder_text="Destination")
        self.dest_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.date_entry = ctk.CTkEntry(self.add_bus_frame, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.grid(row=0, column=2, padx=5, pady=5)
        
        self.time_entry = ctk.CTkEntry(self.add_bus_frame, placeholder_text="Time (HH:MM)")
        self.time_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.seats_entry = ctk.CTkEntry(self.add_bus_frame, placeholder_text="Total Seats")
        self.seats_entry.grid(row=0, column=4, padx=5, pady=5)
        
        self.add_btn = ctk.CTkButton(self.add_bus_frame, text="Add Bus", command=self.add_bus)
        self.add_btn.grid(row=0, column=5, padx=5, pady=5)

        # Bus List
        self.buses_scroll_frame = ctk.CTkScrollableFrame(self.tab_manage, label_text="Existing Buses")
        self.buses_scroll_frame.pack(fill="both", expand=True, pady=10)

    def setup_master_view_tab(self):
        self.master_scroll_frame = ctk.CTkScrollableFrame(self.tab_master, label_text="All Passenger Bookings")
        self.master_scroll_frame.pack(fill="both", expand=True, pady=10)

    def on_show(self):
        """Called when the frame is raised to the top."""
        self.refresh_buses_list()
        self.refresh_master_view()
        self.refresh_admins_list()

    def add_bus(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        seats = self.seats_entry.get()
        
        if not all([source, dest, date, time, seats]):
            messagebox.showerror("Error", "All fields are required")
            return
            
        try:
            seats = int(seats)
        except ValueError:
            messagebox.showerror("Error", "Total Seats must be an integer")
            return
            
        self.controller.db.add_bus(source, dest, date, time, seats)
        messagebox.showinfo("Success", "Bus added successfully")
        
        # Clear entries
        for entry in [self.source_entry, self.dest_entry, self.date_entry, self.time_entry, self.seats_entry]:
            entry.delete(0, 'end')
            
        self.refresh_buses_list()

    def delete_bus(self, bus_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this bus?"):
            self.controller.db.delete_bus(bus_id)
            self.refresh_buses_list()
            self.refresh_master_view()

    def refresh_buses_list(self):
        # Clear existing
        for widget in self.buses_scroll_frame.winfo_children():
            widget.destroy()
            
        buses = self.controller.db.get_all_buses()
        for i, bus in enumerate(buses):
            bus_text = f"[{bus['bus_id']}] {bus['source']} to {bus['destination']} | {bus['date']} {bus['time']} | Seats: {bus['total_seats']}"
            
            frame = ctk.CTkFrame(self.buses_scroll_frame)
            frame.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(frame, text=bus_text)
            lbl.pack(side="left", padx=10)
            
            del_btn = ctk.CTkButton(frame, text="Delete", fg_color="red", hover_color="darkred", width=60,
                                    command=lambda b_id=bus['bus_id']: self.delete_bus(b_id))
            del_btn.pack(side="right", padx=10, pady=5)

    def refresh_master_view(self):
        # Clear existing
        for widget in self.master_scroll_frame.winfo_children():
            widget.destroy()
            
        bookings = self.controller.db.get_all_bookings()
        for booking in bookings:
            booking_text = (f"Booking #{booking['booking_id']} | User: {booking['username']} | "
                            f"Route: {booking['source']} -> {booking['destination']} | "
                            f"{booking['date']} {booking['time']} | Seat: {booking['seat_number']}")
            
            lbl = ctk.CTkLabel(self.master_scroll_frame, text=booking_text, anchor="w", justify="left")
            lbl.pack(fill="x", padx=10, pady=5)

    def setup_manage_admins_tab(self):
        # Add Admin Form
        self.add_admin_frame = ctk.CTkFrame(self.tab_admins)
        self.add_admin_frame.pack(fill="x", pady=10)
        
        self.admin_username_entry = ctk.CTkEntry(self.add_admin_frame, placeholder_text="Username")
        self.admin_username_entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.admin_password_entry = ctk.CTkEntry(self.add_admin_frame, placeholder_text="Password", show="*")
        self.admin_password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.admin_confirm_entry = ctk.CTkEntry(self.add_admin_frame, placeholder_text="Confirm Password", show="*")
        self.admin_confirm_entry.grid(row=0, column=2, padx=5, pady=5)
        
        self.add_admin_btn = ctk.CTkButton(self.add_admin_frame, text="Add Admin", command=self.add_admin)
        self.add_admin_btn.grid(row=0, column=3, padx=5, pady=5)

        # Admin List
        self.admins_scroll_frame = ctk.CTkScrollableFrame(self.tab_admins, label_text="Existing Admins")
        self.admins_scroll_frame.pack(fill="both", expand=True, pady=10)

    def add_admin(self):
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()
        confirm = self.admin_confirm_entry.get()
        
        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        success = self.controller.db.register_user(username, password, role="admin")
        if success:
            messagebox.showinfo("Success", f"Admin '{username}' added successfully")
            self.admin_username_entry.delete(0, 'end')
            self.admin_password_entry.delete(0, 'end')
            self.admin_confirm_entry.delete(0, 'end')
            self.refresh_admins_list()
        else:
            messagebox.showerror("Error", "Username already exists")

    def delete_admin(self, user_id, username):
        # Prevent currently logged-in admin from deleting themselves
        if self.controller.current_user and self.controller.current_user['id'] == user_id:
            messagebox.showerror("Error", "You cannot delete your own account.")
            return

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete admin '{username}'?"):
            self.controller.db.delete_user(user_id)
            self.refresh_admins_list()

    def refresh_admins_list(self):
        for widget in self.admins_scroll_frame.winfo_children():
            widget.destroy()
            
        admins = self.controller.db.get_all_admins()
        for admin in admins:
            frame = ctk.CTkFrame(self.admins_scroll_frame)
            frame.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(frame, text=f"[{admin['id']}] {admin['username']}")
            lbl.pack(side="left", padx=10)
            
            # Don't show delete button for the current user
            if self.controller.current_user and self.controller.current_user['id'] != admin['id']:
                del_btn = ctk.CTkButton(frame, text="Delete", fg_color="red", hover_color="darkred", width=60,
                                        command=lambda u_id=admin['id'], u_name=admin['username']: self.delete_admin(u_id, u_name))
                del_btn.pack(side="right", padx=10, pady=5)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")


class CustomerDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Customer Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left")
        
        self.logout_btn = ctk.CTkButton(self.header_frame, text="Logout", width=100, command=self.logout)
        self.logout_btn.pack(side="right")

        # Container for swappable views (Search vs Seat Map)
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.setup_search_view()
        self.setup_seat_map_view()
        
        self.show_search_view()

    def setup_search_view(self):
        self.search_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        
        # Search parameters
        self.search_bar_frame = ctk.CTkFrame(self.search_frame)
        self.search_bar_frame.pack(fill="x", pady=(0, 10))
        
        self.source_entry = ctk.CTkEntry(self.search_bar_frame, placeholder_text="Source")
        self.source_entry.pack(side="left", padx=10, pady=10)
        
        self.dest_entry = ctk.CTkEntry(self.search_bar_frame, placeholder_text="Destination")
        self.dest_entry.pack(side="left", padx=10, pady=10)
        
        self.search_btn = ctk.CTkButton(self.search_bar_frame, text="Search Buses", command=self.search_buses)
        self.search_btn.pack(side="left", padx=10, pady=10)
        
        # Results scrollable frame
        self.results_frame = ctk.CTkScrollableFrame(self.search_frame, label_text="Available Buses")
        self.results_frame.pack(fill="both", expand=True)

    def setup_seat_map_view(self):
        self.seat_map_frame = ctk.CTkScrollableFrame(self.view_container, fg_color="transparent")
        
        self.seat_header_frame = ctk.CTkFrame(self.seat_map_frame, fg_color="transparent")
        self.seat_header_frame.pack(fill="x", pady=(0, 10))
        
        self.back_btn = ctk.CTkButton(self.seat_header_frame, text="Back to Search", width=120, command=self.show_search_view)
        self.back_btn.pack(side="left")
        
        self.bus_info_label = ctk.CTkLabel(self.seat_header_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.bus_info_label.pack(side="left", padx=20)
        
        # Legend
        self.legend_frame = ctk.CTkFrame(self.seat_map_frame, fg_color="transparent")
        self.legend_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.legend_frame, text="Legend: ").pack(side="left")
        ctk.CTkButton(self.legend_frame, text="Available", fg_color="green", state="disabled", width=80).pack(side="left", padx=5)
        ctk.CTkButton(self.legend_frame, text="Booked", fg_color="red", state="disabled", width=80).pack(side="left", padx=5)
        ctk.CTkButton(self.legend_frame, text="Selected", fg_color="blue", state="disabled", width=80).pack(side="left", padx=5)

        # Seats grid container
        self.seats_grid_frame = ctk.CTkFrame(self.seat_map_frame)
        self.seats_grid_frame.pack(pady=20)
        
        self.confirm_btn = ctk.CTkButton(self.seat_map_frame, text="Confirm Booking", command=self.confirm_booking)
        self.confirm_btn.pack(pady=10)
        
        self.current_selected_seat = None
        self.current_bus_id = None

    def show_search_view(self):
        self.seat_map_frame.pack_forget()
        self.search_frame.pack(fill="both", expand=True)
        self.search_buses()

    def show_seat_map_view(self, bus):
        self.search_frame.pack_forget()
        self.seat_map_frame.pack(fill="both", expand=True)
        
        self.current_bus_id = bus['bus_id']
        self.current_selected_seat = None
        
        self.bus_info_label.configure(text=f"Route: {bus['source']} -> {bus['destination']} | {bus['date']} {bus['time']}")
        
        self.build_seat_map(bus['total_seats'])

    def on_show(self):
        self.show_search_view()
        self.source_entry.delete(0, 'end')
        self.dest_entry.delete(0, 'end')

    def search_buses(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        
        buses = self.controller.db.search_buses(source, dest)
        if not buses:
            ctk.CTkLabel(self.results_frame, text="No buses found.").pack(pady=20)
            return
            
        for bus in buses:
            frame = ctk.CTkFrame(self.results_frame)
            frame.pack(fill="x", pady=5, padx=5)
            
            info = f"{bus['source']} -> {bus['destination']}  |  {bus['date']} at {bus['time']}  |  Total Seats: {bus['total_seats']}"
            lbl = ctk.CTkLabel(frame, text=info, font=ctk.CTkFont(size=14))
            lbl.pack(side="left", padx=10, pady=10)
            
            btn = ctk.CTkButton(frame, text="Select Seats", width=120, command=lambda b=bus: self.show_seat_map_view(b))
            btn.pack(side="right", padx=10, pady=10)

    def build_seat_map(self, total_seats):
        for widget in self.seats_grid_frame.winfo_children():
            widget.destroy()
            
        booked_seats = self.controller.db.get_booked_seats(self.current_bus_id)
        
        # Typically buses have 4 seats per row
        cols = 4
        
        self.seat_buttons = {}
        
        for i in range(total_seats):
            seat_num = str(i + 1)
            row = i // cols
            col = i % cols
            # Add aisle gap
            if col >= 2:
                col += 1
                
            is_booked = seat_num in booked_seats
            
            btn_color = "red" if is_booked else "green"
            btn_state = "disabled" if is_booked else "normal"
            
            btn = ctk.CTkButton(self.seats_grid_frame, text=seat_num, width=50, height=50,
                                fg_color=btn_color, state=btn_state,
                                command=lambda s=seat_num: self.select_seat(s))
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            self.seat_buttons[seat_num] = btn

    def select_seat(self, seat_num):
        # Deselect previous
        if self.current_selected_seat:
            self.seat_buttons[self.current_selected_seat].configure(fg_color="green")
            
        if self.current_selected_seat == seat_num:
            self.current_selected_seat = None
        else:
            self.current_selected_seat = seat_num
            self.seat_buttons[seat_num].configure(fg_color="blue")

    def confirm_booking(self):
        if not self.current_selected_seat:
            messagebox.showerror("Error", "Please select a seat first.")
            return
            
        user = self.controller.current_user
        bus_id = self.current_bus_id
        seat_num = self.current_selected_seat
        
        booking_id = self.controller.db.book_seat(user['id'], bus_id, seat_num)
        
        if booking_id:
            bus = self.controller.db.get_bus_by_id(bus_id)
            route = f"{bus['source']} to {bus['destination']}"
            dt = f"{bus['date']} {bus['time']}"
            
            ticket_path = generate_ticket(user['username'], route, dt, seat_num, booking_id)
            
            messagebox.showinfo("Success", f"Seat {seat_num} booked successfully!\nTicket saved at: {ticket_path}")
            
            # Refresh map
            self.build_seat_map(bus['total_seats'])
            self.current_selected_seat = None
        else:
            messagebox.showerror("Error", "Seat is already booked. Please choose another.")
            self.build_seat_map(self.controller.db.get_bus_by_id(bus_id)['total_seats'])

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")
