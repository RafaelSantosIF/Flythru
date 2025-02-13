import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc

class SupplierMenu:
    def __init__(self):
        self.table_container = None
        
    def load_image(self, filename, size):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")
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
        self.table_container = ctk.CTkFrame(main_content, fg_color=self.colors["table_bg"]) 
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Table headers
        headers = ["N°", "Data", "Cliente", "Valor (R$)", "Pagamento", " ", " "]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.table_container,
                text=header,
                font=self.fonts["header_font"],
                fg_color=None,
                text_color="black"
            )
            header_label.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
                
        # Configure grid columns to expand properly
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)
            
        # Add supplier button
        add_row_button = ctk.CTkButton(
            main_content,
            text="Cadastrar",
            width=120,
            height=40,
            fg_color=self.colors["second_color"],
            hover_color=self.colors["second_hover_color"],
            text_color="white",
            font=self.fonts["button_font"],
            command=lambda: self.add_supplier_row(root)  
        )
        add_row_button.pack(pady=(0, 20))
        
    def add_supplier_row(self, root):        
        add_window = ctk.CTkToplevel()
        add_window.title("Cadastrar Fornecedor")
        add_window.geometry("300x500")
        add_window.resizable(False, False)
        add_window.overrideredirect(True)
        add_window.grab_set()
        add_window.focus_force()
        
        # Create a main frame 
        main_frame = ctk.CTkFrame(
            add_window,
            fg_color="#FF8C00",  
            corner_radius=10
        )
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Create a title bar frame for dragging
        title_bar = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",  
            height=20,
            corner_radius=0
        )
        title_bar.pack(fill="x", padx=2, pady=0)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Cadastrar Fornecedor",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="white"
        )
        title.pack(pady=(5, 20))
        
        # Add dragging functionality
        from MainMenu import WindowDragging
        WindowDragging(add_window, title_bar) 
        
        # Input frame 
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1E1E1E",  
            corner_radius=5
        )
        input_frame.pack(padx=10, fill="x")

        # Código input
        cdg_label = ctk.CTkLabel(
            input_frame,
            text="Código:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        cdg_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        cdg_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="#F1001",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        cdg_entry.pack(padx=10, pady=(0, 5), fill="x")

        # Nome input
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
        nome_entry.pack(padx=10, pady=(0, 5), fill="x")
        
        cnpj_label = ctk.CTkLabel(
            input_frame,
            text="CNPJ:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        cnpj_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        cnpj_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="xx.xxx.xxx/xxxx-xx",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        cnpj_entry.pack(padx=10, pady=(0, 5), fill="x")
        
        telefone_label = ctk.CTkLabel(
            input_frame,
            text="Telefone:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        telefone_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        telefone_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="(xx) xxxxx-xxxx",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        telefone_entry.pack(padx=10, pady=(0, 5), fill="x")
        
        email_label = ctk.CTkLabel(
            input_frame,
            text="E-Mail:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        email_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        email_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="contato@alimentos.com",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        email_entry.pack(padx=10, pady=(0, 5), fill="x")
        
        def cancel():
            add_window.destroy()

        def save():
            # Get values
            cdg_supplier = cdg_entry.get().strip()
            supplier = nome_entry.get().strip()
            cnpj = cnpj_entry.get().strip()
            telefone = telefone_entry.get().strip()
            email = email_entry.get().strip()        
            
            # Validate inputs
            if not supplier or not cdg_supplier:
                return  # Add error handling if needed

            # Add row to the table
            self.add_row_to_table(cdg_supplier, supplier, cnpj, telefone, email)
            add_window.destroy()
            
        cancel_button = ctk.CTkButton(
            main_frame,
            text="Cancelar",
            font=self.fonts["button_font"],
            width=120,
            height=35,
            fg_color="#FF0000", 
            hover_color="#CC0000",  
            command=cancel
        )
        cancel_button.place(relx=0.25, rely=0.95, anchor="center")

        save_button = ctk.CTkButton(
            main_frame,
            text="Salvar",
            font=self.fonts["button_font"],
            width=120,
            height=35,
            fg_color=self.colors["second_color"],  
            hover_color=self.colors["second_hover_color"],
            command=save
        )
        save_button.place(relx=0.75, rely=0.95, anchor="center")
        
    def add_row_to_table(self, cdg_supplier, supplier, cnpj, telefone, email):
        try:
            # Find the number of existing rows in the table
            current_rows = len([child for child in self.table_container.grid_slaves() if int(child.grid_info()["row"]) > 0])
            new_row = current_rows + 1  
            
            # Add new row to the table
            values = [cdg_supplier, supplier, cnpj, telefone, email]
            for col, value in enumerate(values):
                row_label = ctk.CTkLabel(
                    self.table_container,
                    text=str(value),
                    font=self.fonts["input_font"],
                    fg_color="transparent",
                    text_color="black"
                )
                row_label.grid(row=new_row, column=col, padx=8, pady=5, sticky="ew")
                
            edit_icon = self.load_image("edit_icon.png", size=(30, 30))
            printer = self.load_image("printer.png", size=(30, 30))
            
            edit_button = ctk.CTkButton(
                self.table_container,
                text=" ",
                image=edit_icon,
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="transparent",                
                text_color="white",
                font=self.fonts["input_font"],
                command=lambda r=new_row: self.edit_row(r)  
            )
            edit_button.grid(row=new_row, column=5, padx=2, pady=5, sticky="ew")
            
            print_button = ctk.CTkButton(
                self.table_container,
                text=" ",
                image=printer,
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="transparent",                
                text_color="white",
                font=self.fonts["input_font"],
                command=None  
            )
            print_button.grid(row=new_row, column=6, padx=2, pady=5, sticky="ew")    
                
        except Exception as e:
            print(f"Error adding row to table: {e}")
            
    def edit_row(self, row):
        pass                               