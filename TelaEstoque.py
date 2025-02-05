import customtkinter as ctk
from PIL import Image
import os

class StorageMenu:
    def __init__(self, root):
        self.root = root
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
        #self.table_container = table_container
        self.headers = ["ID", "Produto", "Quantidade", "Categoria", "Ação"] 

    def init_fonts(self, root):
        # Initialize fonts
        logo_font = ctk.CTkFont(family="Arial", size=30, weight="bold")
        menu_font = ctk.CTkFont(family="Verdana", size=16, weight="bold")
        input_font = ctk.CTkFont(family="Verdana", size=14)
        header_font = ctk.CTkFont(family="Verdana", size=14, weight="bold")
        button_font = ctk.CTkFont(family="Verdana", size=14, weight="bold")

        # Initialize colors
        main_color = "#FF8C00"
        second_color = "#00FF1E"
        second_hover_color = "#0B951B"         
        hover_color = "#FFA500"
        dark_bg = "#1E1E1E"  
        menu_bg = "white"  
        table_bg = "white"
        link_color = "#87CEEB"

        return {
            "logo_font": logo_font,
            "menu_font": menu_font,
            "input_font": input_font,
            "header_font": header_font,
            "button_font": button_font
        }, {
            "main_color": main_color,
            "second_color": second_color,
            "second_hover_color": second_hover_color,
            "hover_color": hover_color,
            "dark_bg": dark_bg,
            "menu_bg": menu_bg,
            "table_bg": table_bg,
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
                hover_color=self.colors["hover_color"], 
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

        # Table container with white background
        self.table_container = ctk.CTkFrame(main_content, fg_color=self.colors["table_bg"])  # Store as instance variable
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Table headers
        headers = ["ID", "Produto", "Quantidade", "Categoria", "Ação"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.table_container,
                text=header,
                font=self.fonts["header_font"],
                fg_color=None,
                text_color="black"
            )
            header_label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
                
        # Configure grid columns to expand properly
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)

        # Add product button
        add_row_button = ctk.CTkButton(
            main_content,
            text="Cadastrar",
            width=120,
            height=40,
            fg_color=self.colors["second_color"],
            hover_color=self.colors["second_hover_color"],
            text_color="white",
            font=self.fonts["button_font"],
            command=self.add_stock_row
        )
        add_row_button.pack(pady=(0, 20))
        
    def menu_item_clicked(self, item):
        self.root.withdraw()
        
        if item == "Estoque 📦":
            pass
        if item ==  "Cardapio 🍔":         
            menu_window = ctk.CTkToplevel()
            menu_window.title("FlyThru - Estoque")
            menu_window.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            
            # Initialize the Cartemenu in the new window
            from TelaCardapio import Cartemenu
            menu_screen = Cartemenu(menu_window)
        else:
            pass    
            
        # When menu window is closed, show login window again
        def on_menu_close():
            menu_window.destroy()
            self.root.deiconify()
            
        menu_window.protocol("WM_DELETE_WINDOW", on_menu_close)

    def add_stock_row(self):
        # Create a new toplevel window for adding a stock item
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Cadastrar produto")
        add_window.geometry("300x500")
        add_window.resizable(False, False)
        add_window.grab_set()
        add_window.focus_force()
        
        # Create a main frame with orange background
        main_frame = ctk.CTkFrame(
            add_window,
            fg_color="#FF8C00",  
            corner_radius=10
        )
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Cadastrar produto",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(20, 30))

        # Input frame with dark background
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1E1E1E",  # Dark background
            corner_radius=5
        )
        input_frame.pack(padx=10, fill="x")

        # ID input
        id_label = ctk.CTkLabel(
            input_frame,
            text="ID:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        id_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        id_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="#01",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        id_entry.pack(padx=10, pady=(0, 10), fill="x")

        # Nome (Name) input
        nome_label = ctk.CTkLabel(
            input_frame,
            text="Nome:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        nome_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        nome_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        nome_entry.pack(padx=10, pady=(0, 10), fill="x")
        
        quant_label = ctk.CTkLabel(
            input_frame,
            text="Quantidade:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        quant_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        quant_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        quant_entry.pack(padx=10, pady=(0, 10), fill="x")

        # Category dropdown
        categoria_label = ctk.CTkLabel(
            input_frame,
            text="Categoria:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        categoria_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        categorias = ["Carnes", "Bebidas", "Acompanhamentos", "Sobremesas", "Embalagens", "Outros"]
        categoria_var = ctk.StringVar(value="Outros")
        categoria_dropdown = ctk.CTkOptionMenu(
            input_frame,
            values=categorias,
            variable=categoria_var,
            font=self.fonts["input_font"],
            fg_color="black",
            button_color="#FF8C00",
            button_hover_color="#FFA500",
            dropdown_fg_color="black",
            dropdown_hover_color="#333333",
            dropdown_text_color="white"
        )
        categoria_dropdown.pack(padx=10, pady=(0, 20), fill="x")

        def cancel():
            add_window.destroy()

        def save():
            # Get values
            id_produto = id_entry.get().strip()
            produto = nome_entry.get().strip()
            quant = quant_entry.get().strip()
            categoria = categoria_var.get()

            # Validate inputs
            if not produto or not id_produto:
                return  # Add error handling if needed

            # Add row to the table
            self.add_row_to_table(id_produto, produto, quant, categoria)
            add_window.destroy()

        # Create buttons directly in the main_frame
        cancel_button = ctk.CTkButton(
            main_frame,
            text="Cancelar",
            font=self.fonts["button_font"],
            width=120,
            height=35,
            fg_color="#FF0000",  # Red color
            hover_color="#CC0000",  # Darker red for hover
            command=cancel
        )
        cancel_button.place(relx=0.25, rely=0.85, anchor="center")

        save_button = ctk.CTkButton(
            main_frame,
            text="Salvar",
            font=self.fonts["button_font"],
            width=120,
            height=35,
            fg_color=self.colors["second_color"],  # Green color
            hover_color=self.colors["second_hover_color"],
            command=save
        )
        save_button.place(relx=0.75, rely=0.85, anchor="center")

    def add_row_to_table(self, id_produto, produto, quant, categoria):
        try:
            # Find the number of existing rows in the table
            current_rows = len([child for child in self.table_container.grid_slaves() if int(child.grid_info()["row"]) > 0])
            new_row = current_rows + 1  # Add 1 to account for header row
            
            # Add new row to the table
            values = [id_produto, produto, quant, categoria]
            for col, value in enumerate(values):
                row_label = ctk.CTkLabel(
                    self.table_container,
                    text=str(value),
                    font=self.fonts["input_font"],
                    fg_color="transparent",
                    text_color="black"
                )
                row_label.grid(row=new_row, column=col, padx=10, pady=5, sticky="ew")
            
            # Add edit button in the action column
            edit_button = ctk.CTkButton(
                self.table_container,
                text="Editar",
                width=60,
                height=30,
                fg_color=self.colors["main_color"],
                hover_color=self.colors["hover_color"],
                text_color="white",
                font=self.fonts["input_font"],
                command=lambda r=new_row: self.edit_row(r)  # Pass the row number to edit_row method
            )
            edit_button.grid(row=new_row, column=4, padx=10, pady=5, sticky="ew")  # Column 4 is the Action column
            
            # Configure the new row
            self.table_container.grid_rowconfigure(new_row, pad=3)
            
            print(f"Added new row: {values}")  # Debug print
            
        except Exception as e:
            print(f"Error adding row to table: {e}")

    def edit_row(self, row):
        # Get the current values from the row
        current_values = []
        for col in range(4):  # Get values from the first 4 columns (excluding action column)
            cell = [
                widget for widget in self.table_container.grid_slaves()
                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
            ]
            if cell:
                current_values.append(cell[0].cget("text"))
        
        if len(current_values) == 4:
            id_produto, produto, quant, categoria = current_values
            
            # Create edit window (similar to add_stock_row but with pre-filled values)
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar produto")
            edit_window.geometry("300x500")
            edit_window.resizable(False, False)
            edit_window.grab_set()
            edit_window.focus_force()

            # Create a main frame with orange background
            main_frame = ctk.CTkFrame(
                edit_window,
                fg_color="#FF8C00",
                corner_radius=10
            )
            main_frame.pack(padx=10, pady=10, fill="both", expand=True)

            # Title
            title = ctk.CTkLabel(
                main_frame,
                text="Editar produto",
                font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
                text_color="white"
            )
            title.pack(pady=(15, 20))

            # Input frame
            input_frame = ctk.CTkFrame(
                main_frame,
                fg_color="#1E1E1E",
                corner_radius=5
            )
            input_frame.pack(padx=10, fill="x")

            # ID input (disabled since it's the identifier)
            id_label = ctk.CTkLabel(input_frame, text="ID:", font=self.fonts["input_font"], text_color="white")
            id_label.pack(padx=5, pady=(5, 0), anchor="w")
            id_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            id_entry.insert(0, id_produto)
            id_entry.configure(state="disabled")
            id_entry.pack(padx=5, pady=(0, 5), fill="x")

            # Name input
            nome_label = ctk.CTkLabel(input_frame, text="Nome:", font=self.fonts["input_font"], text_color="white")
            nome_label.pack(padx=5, pady=(5, 0), anchor="w")
            nome_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            nome_entry.insert(0, produto)
            nome_entry.pack(padx=5, pady=(0, 5), fill="x")

            # Quantity input
            quant_label = ctk.CTkLabel(input_frame, text="Quantidade:", font=self.fonts["input_font"], text_color="white")
            quant_label.pack(padx=5, pady=(5, 0), anchor="w")
            quant_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            quant_entry.insert(0, quant)
            quant_entry.pack(padx=5, pady=(0, 5), fill="x")

            # Category dropdown
            categoria_label = ctk.CTkLabel(input_frame, text="Categoria:", font=self.fonts["input_font"], text_color="white")
            categoria_label.pack(padx=5, pady=(5, 0), anchor="w")
            categorias = ["Carnes", "Bebidas", "Acompanhamentos", "Sobremesas", "Embalagens", "Outros"]
            categoria_var = ctk.StringVar(value=categoria)
            categoria_dropdown = ctk.CTkOptionMenu(
                input_frame,
                values=categorias,
                variable=categoria_var,
                font=self.fonts["input_font"],
                fg_color="black",
                button_color="#FF8C00",
                button_hover_color="#FFA500",
                dropdown_fg_color="black",
                dropdown_hover_color="#333333",
                dropdown_text_color="white"
            )
            categoria_dropdown.pack(padx=5, pady=(0, 10), fill="x")

            def save_edit():
                # Update the row in the table
                new_values = [
                    id_entry.get(),
                    nome_entry.get(),
                    quant_entry.get(),
                    categoria_var.get()
                ]
                
                # Update labels in the table
                for col, value in enumerate(new_values):
                    cell = [
                        widget for widget in self.table_container.grid_slaves()
                        if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
                    ]
                    if cell:
                        cell[0].configure(text=str(value))
                
                edit_window.destroy()

            # Buttons
            cancel_button = ctk.CTkButton(
                main_frame,
                text="Cancelar",
                font=self.fonts["button_font"],
                width=120,
                height=35,
                fg_color="#FF0000",
                hover_color="#CC0000",
                command=edit_window.destroy
            )
            cancel_button.place(relx=0.25, rely=0.85, anchor="center")

            save_button = ctk.CTkButton(
                main_frame,
                text="Salvar",
                font=self.fonts["button_font"],
                width=120,
                height=35,
                fg_color=self.colors["second_color"],
                hover_color=self.colors["second_hover_color"],
                command=save_edit
            )
            save_button.place(relx=0.75, rely=0.85, anchor="center")

def main():
    root = ctk.CTk()
    root.title("FlyThru - Storage")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    app = StorageMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()