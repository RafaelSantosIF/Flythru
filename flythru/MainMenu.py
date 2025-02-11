import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc
from TelaEstoque import StorageMenu
from TelaCardapio import CarteMenu

class MainMenu:
    def __init__(self, root):
        self.root = root
        # Initialize fonts and colors
        self.fonts, self.colors = dc.init_fonts(self.root)

        # Load images
        self.logo_image = self.load_image("round_logo.png", (70, 70))
        self.close_icon = self.load_image("close_icon.png", (30, 30))
        self.flythru_icon = self.load_image("FLYTHRU.png", (255, 31))
        
        # Variable to track current content frame
        self.current_content = None
        self.track_tela = 4
        
        # Menu instance
        self.storage_menu = StorageMenu()
        self.carte_menu = CarteMenu()        

        # Create Menu Areas
        self.create_top_bar(root)        
        self.create_side_menu(root)        
        self.create_main_content(root)
        
            
    def load_image(self, filename, size):
        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")

        # Load image
        image_path = os.path.join(assets_dir, filename)
        if os.path.exists(image_path):
            print(f"{filename} file found!")
            return ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=size
            )
        else:
            print(f"{filename} file not found at: {image_path}")
            return None

    def create_top_bar(self, root):
        # Top bar frame
        top_bar = ctk.CTkFrame(root, fg_color=self.colors["main_color"], height=80)
        top_bar.pack(side="top", fill="x")

        # Logo
        if self.logo_image:
            logo_label = ctk.CTkLabel(top_bar, image=self.logo_image, text="")
            logo_label.place(relx=0.05, rely=0.5, anchor="center")

        # Title
        if self.flythru_icon:
            logo_label = ctk.CTkLabel(top_bar, image=self.flythru_icon, text="")
            logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Close button
        if self.close_icon:
            close_button = ctk.CTkButton(
                top_bar,
                image=self.close_icon,
                text="",
                width=40,
                height=40,
                fg_color="transparent",
                hover_color=self.colors["hover_color"],
                command=root.destroy
            )
            close_button.place(relx=0.95, rely=0.5, anchor="center")
        else:
            close_button = ctk.CTkButton(
                top_bar,
                text="X",
                width=40,
                height=40,
                fg_color="transparent",
                hover_color=self.colors["hover_color"],
                command=root.destroy
            )
            close_button.place(relx=0.95, rely=0.5, anchor="center")
            
    def create_side_menu(self, root):
        # Side menu frame
        side_menu = ctk.CTkFrame(root, fg_color=self.colors["menu_bg"], width=280)
        side_menu.pack(side="left", fill="both", expand=False)

        # Create a frame for padding and organization
        buttons_frame = ctk.CTkFrame(side_menu, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=20, fill="x")

        # Menu items 
        menu_items = ["Estoque 📦", "Pedidos 📝", "Fornecedores 🚚", "Cardapio 🍔"]
        for item in menu_items:
            menu_button = ctk.CTkButton(
                buttons_frame,
                text=item,
                width=240,
                height=50,
                fg_color=self.colors["main_color"],  
                hover_color=self.colors["hover_color"], 
                text_color="white",
                font=self.fonts["menu_font"],
                corner_radius=10,  # Rounded corners
                command=lambda x=item: self.menu_item_clicked(x)
            )
            menu_button.pack(pady=5)
            
    def create_main_content(self, root):
        # Destroy existing content if it exists
        if self.current_content:
            self.current_content.destroy()
            
        # Create new content frame
        self.current_content = ctk.CTkFrame(root)
        self.current_content.pack(side="right", fill="both", expand=True)
        
        # Default to Cardapio menu
        self.carte_menu.create_main_content(self, self.current_content)    
        
    def menu_item_clicked(self, item):       
        # Switch based on menu item
        if item == "Estoque 📦":
            if self.track_tela != 1:
                self.current_content.destroy()
                self.current_content = ctk.CTkFrame(self.root)
                self.current_content.pack(side="right", fill="both", expand=True) 
                self.storage_menu.create_main_content(self, self.current_content)
                self.track_tela = 1
            else:
                pass    
        elif item == "Pedidos 📝":
            # Add orders menu when implemented
            pass
        elif item == "Fornecedores 🚚":
            # Add suppliers menu when implemented
            pass
        elif item == "Cardapio 🍔":
            if self.track_tela != 4:
                self.current_content.destroy()
                self.current_content = ctk.CTkFrame(self.root)
                self.current_content.pack(side="right", fill="both", expand=True) 
                self.carte_menu.create_main_content(self, self.current_content)
                self.track_tela = 4
            else:
               pass          
    
def main():
    root = ctk.CTk()
    root.title("FlyThru - Menu")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.attributes('-fullscreen', True)
    
    app = MainMenu(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    
            
    
