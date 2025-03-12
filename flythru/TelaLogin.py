# main.py
import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc
from MainMenu import MainMenu

class LoginScreen:
    def __init__(self):        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FlyThru - Login")
        self.root.geometry(self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight())))
        self.root.attributes('-fullscreen', True)    
       
        self.fonts, self.colors = dc.init_fonts(self.root)
        
        self.root.bind('<Escape>', self.toggle_fullscreen)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(current_dir, "assets")  # Store assets_dir as instance variable
        
        self.load_images(self.assets_dir)
        
        #GRID & FRAMES
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.create_frames()
        self.setup_left_frame()
        self.setup_right_frame()
        
    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)    
        
    def load_images(self, assets_path):
        try:
            logo_path = os.path.join(assets_path, "logo.png")
            bottom_icon_path = os.path.join(assets_path, "bottom_icon.png")
            flythru_path = os.path.join(assets_path, "FLYTHRU_W.png")
            print("teste")
            
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
        self.left_frame = ctk.CTkFrame(self.root, fg_color=self.colors["primary"])
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.right_frame = ctk.CTkFrame(self.root, fg_color=self.colors["dark_bg"])
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
    def setup_left_frame(self):     
        self.left_frame.grid_rowconfigure(0, weight=4)  
        self.left_frame.grid_rowconfigure(1, weight=0) 
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_rowconfigure(3, weight=3)  
        self.left_frame.grid_rowconfigure(4, weight=1)  
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        content_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        
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
        logo_label.pack(pady=(10, 10)) 
        
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
        logo_label.pack(pady=(10, 10))  
        
        welcome_label = ctk.CTkLabel(
            content_frame,
            text="☕  Bem Vindo!  ♨️",
            font=self.fonts["welcome_font"],
            text_color=self.colors["text_primary"]
        )
        welcome_label.pack(pady=(30, 20))  
        
        if self.bottom_image:
            bottom_button = ctk.CTkButton(
                self.left_frame,
                image=self.bottom_image,
                text="",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color=self.colors["primary_hover"],
                command=self.bottom_button_click
            )
        else:
            bottom_button = ctk.CTkButton(
                self.left_frame,
                text="[Icon]",
                width=50,
                height=50,
                fg_color="transparent",
                hover_color=self.colors["primary_hover"],
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
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            height=60,
            placeholder_text="Código Empresa",
            font=self.fonts["input_font_login"]
        )
        self.username_entry.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            height=60,
            placeholder_text="Senha",
            show="•",
            font=self.fonts["input_font_login"]
        )
        self.password_entry.pack(pady=10)
        
        login_button = ctk.CTkButton(
            form_frame,
            text="entrar",
            width=200,
            height=50,
            font=self.fonts["button_font_login"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.login
        )
        login_button.pack(pady=(20, 0))
        
        forgot_pwd = ctk.CTkLabel(
            form_frame,
            text="Esqueceu sua senha?",
            font=self.fonts["link_font"],
            text_color=self.colors["link"],
            cursor="hand2"
        )
        forgot_pwd.pack(pady=0)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Hide the login window instead of destroying it
        self.root.withdraw()
        
        # Create a new top-level window for the menu
        menu_window = ctk.CTkToplevel()
        menu_window.title("FlyThru - Menu")
        menu_window.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        menu_window.attributes('-fullscreen', True)
         
        # Initialize the Cartemenu in the new window
        menu_screen = MainMenu(menu_window)
        
        # When menu window is closed, show login window again
        def on_menu_close():
            menu_window.destroy()
            self.root.deiconify()
            
        menu_window.protocol("WM_DELETE_WINDOW", on_menu_close)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginScreen()
    app.run()