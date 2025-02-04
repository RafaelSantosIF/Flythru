import customtkinter as ctk
from PIL import Image
import os

class StorageMenu:
    def __init__(self, root):
        # Initialize fonts and colors
        self.fonts, self.colors = self.init_fonts(root)

        # Load images
        self.logo_image = self.load_image("round_logo.png", (70, 70))
        self.close_icon = self.load_image("close_icon.png", (30, 30))
        self.flythru_icon = self.load_image("FLYTHRU.png", (255, 31))

        # Create top bar
        self.create_top_bar(root)

        # Create side menu
        self.create_side_menu(root)

        # Create main content area
        self.create_main_content(root)

    def init_fonts(self, root):
        # Initialize fonts
        logo_font = ctk.CTkFont(family="Arial", size=30, weight="bold")
        menu_font = ctk.CTkFont(family="Verdana", size=16, weight="bold")
        input_font = ctk.CTkFont(family="Verdana", size=14)
        button_font = ctk.CTkFont(family="Verdana", size=14, weight="bold")

        # Initialize colors
        main_color = "#FF8C00"  # Orange
        hover_color = "#FFA500"
        dark_bg = "#1E1E1E"  # Darker background for main content
        menu_bg = "white"  # White background for side menu
        link_color = "#87CEEB"

        return {
            "logo_font": logo_font,
            "menu_font": menu_font,
            "input_font": input_font,
            "button_font": button_font
        }, {
            "main_color": main_color,
            "hover_color": hover_color,
            "dark_bg": dark_bg,
            "menu_bg": menu_bg,
            "link_color": link_color
        }

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

        # Menu items with updated styling
        menu_items = ["Estoque 📦", "Pedidos 📝", "Fornecedores 🚚", "Cardapio 🍔"]
        for item in menu_items:
            menu_button = ctk.CTkButton(
                buttons_frame,
                text=item,
                width=240,
                height=50,
                fg_color=self.colors["main_color"],  
                hover_color="#FF8C00", 
                text_color="white",
                font=self.fonts["menu_font"],
                corner_radius=10,  # Rounded corners
                command=lambda x=item: self.menu_item_clicked(x)
            )
            menu_button.pack(pady=5)

    def create_main_content(self, root):
        # Main content frame
        main_content = ctk.CTkFrame(root, fg_color=self.colors["dark_bg"], width=800)
        main_content.pack(side="right", fill="both", expand=True)

        # Search bar container for padding
        search_container = ctk.CTkFrame(main_content, fg_color="transparent")
        search_container.pack(fill="x", padx=20, pady=(20, 10))

        # Updated search bar
        search_bar = ctk.CTkEntry(
            search_container,
            placeholder_text="Pesquisar Produto",
            font=self.fonts["input_font"],
            height=40,
            fg_color="white",
            text_color="black",
            placeholder_text_color="gray"
        )
        search_bar.pack(fill="x")

        # Stock table container for proper spacing
        table_container = ctk.CTkFrame(main_content, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Table headers
        headers = ["Produto", "Quantidade", "Categoria", "Ação"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_container,
                text=header,
                font=self.fonts["input_font"],
                fg_color=self.colors["main_color"],
                text_color="white"
            )
            header_label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        # Configure grid columns to expand properly
        for i in range(len(headers)):
            table_container.grid_columnconfigure(i, weight=1)

        # Add row button
        add_row_button = ctk.CTkButton(
            main_content,
            text="Add Row",
            width=120,
            height=40,
            fg_color="#00FF1E",
            hover_color=self.colors["hover_color"],
            text_color="white",
            font=self.fonts["button_font"],
            command=self.add_stock_row
        )
        add_row_button.pack(pady=(0, 20))
        
    def menu_item_clicked(self, item):
        print(f"Clicked menu item: {item}")

    def add_stock_row(self):
        # Add a new row to the stock table
        pass

def main():
    root = ctk.CTk()
    root.title("FlyThru - Storage")
    root.geometry("1080x720")

    app = StorageMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()