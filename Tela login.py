# main.py
import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc

class LoginScreen:
    def __init__(self):
        # Initialize the customtkinter framework
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("FlyThru - Login")
        self.root.geometry("1080x720")
        
        # Initialize fonts and colors AFTER root creation
        self.fonts, self.colors = dc.init_fonts(self.root)
        
        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")
        
        # Load images with absolute path
        self.load_images(assets_dir)
        
        # Create main grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create frames
        self.create_frames()
        self.setup_left_frame()
        self.setup_right_frame()
        
    def load_images(self, assets_path):
        """Load images from the assets folder"""
        try:
            # Construct full paths using correct path joining
            logo_path = os.path.join(assets_path, "logo.png")
            bottom_icon_path = os.path.join(assets_path, "bottom_icon.png")
            flythru_path = os.path.join(assets_path, "FLYTHRU_W.png")
            
            # Check if files exist
            if os.path.exists(logo_path):
                print("Logo file found!")
                self.logo_image = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(265, 130)
                )
            else:
                print(f"Logo file not found at: {logo_path}")
                self.logo_image = None
                
            if os.path.exists(bottom_icon_path):
                print("Bottom icon file found!")
                self.bottom_image = ctk.CTkImage(
                    light_image=Image.open(bottom_icon_path),
                    dark_image=Image.open(bottom_icon_path),
                    size=(50, 50)
                )
            else:
                print(f"Bottom icon file not found at: {bottom_icon_path}")
                self.bottom_image = None
                
            if os.path.exists(flythru_path):
                print("Flythru file found!")
                self.flythru_image = ctk.CTkImage(
                    light_image=Image.open(flythru_path),
                    dark_image=Image.open(flythru_path),
                    size=(255, 31)
                )
            else:
                print(f"Logo file not found at: {flythru_path}")
                self.logo_image = None    
                
        except Exception as e:
            print(f"Error loading images: {str(e)}")
            self.logo_image = None
            self.bottom_image = None   
           
    def create_frames(self):
        self.left_frame = ctk.CTkFrame(self.root, fg_color=self.colors["main_color"])
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.right_frame = ctk.CTkFrame(self.root, fg_color=self.colors["dark_bg"])
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
    def setup_left_frame(self):
        # Configure grid weights to push content to top 40%
        # First row (0) gets more weight to center content in upper portion
        self.left_frame.grid_rowconfigure(0, weight=3)  # More weight pushes content down from top
        self.left_frame.grid_rowconfigure(1, weight=0)  # No weight for content rows to keep them compact
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=3)  # More weight for bottom space
        self.left_frame.grid_rowconfigure(4, weight=1)  # Space for bottom button
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        # Create a container frame for the main content to keep it together
        content_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        
        # Logo
        if self.logo_image:
            logo_label = ctk.CTkLabel(
                content_frame,
                image=self.logo_image,
                text=""
            )
        else:
            logo_label = ctk.CTkLabel(
                content_frame,
                text="[Logo]",
                font=self.fonts["logo_font"]
            )
        logo_label.pack(pady=(0, 10)) 
        
        # FLYTHRU logo
        if self.flythru_image:
            logo_label = ctk.CTkLabel(
                content_frame,
                image=self.flythru_image,
                text=""
            )
        else:
            logo_label = ctk.CTkLabel(
                content_frame,
                text="[FLYTHRU]",
                font=self.fonts["logo_font"]
            )
        logo_label.pack(pady=(0, 10))  
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            content_frame,
            text="☕  Bem Vindo!  ♨️",
            font=self.fonts["welcome_font"],
            text_color="white"
        )
        welcome_label.pack(pady=(20, 20))  # Slightly more padding after welcome text
        
        # Bottom button (kept at the bottom)
        if self.bottom_image:
            bottom_button = ctk.CTkButton(
                self.left_frame,
                image=self.bottom_image,
                text="",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color=self.colors["hover_color"],
                command=self.bottom_button_click
            )
        else:
            bottom_button = ctk.CTkButton(
                self.left_frame,
                text="[Icon]",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color=self.colors["hover_color"],
                command=self.bottom_button_click
            )
        bottom_button.grid(row=4, column=0, pady=(0, 20), padx=(20, 0), sticky="w")
        
    def bottom_button_click(self):
        print("Bottom button clicked!")
        
    def setup_right_frame(self):
        self.right_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        
        form_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        form_frame.grid(row=2, column=0)
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            height=60,
            placeholder_text="Código Empresa",
            font=self.fonts["input_font"]
        )
        self.username_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            height=60,
            placeholder_text="Senha",
            show="•",
            font=self.fonts["input_font"]
        )
        self.password_entry.pack(pady=10)
        
        # Login button
        login_button = ctk.CTkButton(
            form_frame,
            text="entrar",
            width=200,
            height=50,
            font=self.fonts["button_font"],
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            command=self.login
        )
        login_button.pack(pady=(20, 0))
        
        # Forgot password link
        forgot_pwd = ctk.CTkLabel(
            form_frame,
            text="Esqueceu sua senha?",
            font=self.fonts["link_font"],
            text_color=self.colors["link_color"],
            cursor="hand2"
        )
        forgot_pwd.pack(pady=0)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Login attempt with username: {username}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginScreen()
    app.run()