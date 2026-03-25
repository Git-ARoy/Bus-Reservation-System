import customtkinter
from database import DatabaseManager
from ui_frames import LoginFrame, RegisterFrame, AdminDashboard, CustomerDashboard

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class BusReservationApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bus Reservation System")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Initialize the database manager
        self.db = DatabaseManager()
        
        # Store information about the currently logged in user
        self.current_user = None

        # Container for all frames
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        # Configure container grid to make frames fill the space
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to keep track of frames
        self.frames = {}
        
        # Initialize the frames
        for F in (LoginFrame, RegisterFrame, AdminDashboard, CustomerDashboard):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Put all frames in the same location; the one drawn last/raised is visible
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with LoginFrame
        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        """Bring a specific frame to the front and initialize its data if needed."""
        frame = self.frames[page_name]
        
        # If the frame has an `on_show` method, call it to refresh data
        if hasattr(frame, "on_show"):
            frame.on_show()
            
        frame.tkraise()

if __name__ == "__main__":
    app = BusReservationApp()
    app.mainloop()
