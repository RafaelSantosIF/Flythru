import customtkinter as ctk
import Dictionary as dc

class StorageMenu:
    def __init__(self):
        self.table_container = None
        
    def create_main_content(self, main_menu, root):
        # Use main_menu to access fonts and colors
        self.fonts = main_menu.fonts
        self.colors = main_menu.colors
        self.root = root

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
            command=lambda: self.add_stock_row(root)  # Changed to use instance method
        )
        add_row_button.pack(pady=(0, 20))
    
    def add_stock_row(self, root):
        # Create a new toplevel window for adding a stock item
        add_window = ctk.CTkToplevel()
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