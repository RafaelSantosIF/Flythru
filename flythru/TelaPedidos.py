import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc
from api.pedido.pedido import Pedido

pedido = Pedido()

class OrdersMenu:
    def __init__(self, root=None):
        self.table_container = None
        
        # Inicializar fontes e cores se o root for fornecido
        if root:
            self.fonts, self.colors = dc.init_fonts(root)
        
        self.filter_icon = self.load_image("filter.png", (28, 28))
        
    def set_main_menu(self, main_menu):
        self.main_menu = main_menu
            
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
        search_container = ctk.CTkFrame(main_content, fg_color="transparent", height=40)
        search_container.pack(side="top", fill="x", padx=20, pady=(15, 5))
        search_container.pack_propagate(False)
        
        # Search bar
        self.search_bar = ctk.CTkEntry(
            search_container,
            placeholder_text="🔎 Pesquisar Pedido",
            font=self.fonts["input_font"],
            height=40,
            fg_color=self.colors["text_primary"],
            text_color=self.colors["dark_bg"],
            placeholder_text_color=self.colors["text_disabled"]
        )
        self.search_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Filter/Search button
        filter_button = ctk.CTkButton(
            search_container,
            image=self.filter_icon,
            text="",
            width=28,
            height=28,
            fg_color=self.colors["text_primary"],
            hover_color=self.colors["primary_hover"],
            corner_radius=0,
            command=self.search_orders
        )
        filter_button.place(relx=0.97, rely=0.5, anchor="center")
        
        # Bind Enter key to search
        self.search_bar.bind("<Return>", lambda event: self.search_orders())
        
        # CTkScrollableFrame
        self.table_container = ctk.CTkScrollableFrame(
            main_content, 
            fg_color=self.colors["table_bg"],
            scrollbar_fg_color=self.colors["table_bg"],
            scrollbar_button_color=self.colors["primary"],
            scrollbar_button_hover_color=self.colors["primary_hover"]
        )
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Headers with updated labels to match backend
        headers = ["Cód", "Data", "Itens", "Quantidade", "Valor (R$)", "Pagamento"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.table_container,
                text=header,
                font=self.fonts["header_font"],
                fg_color=self.colors["table_bg"],
                text_color=self.colors["text_dark"]
            )
            header_label.grid(row=0, column=i, padx=10, pady=5, sticky="ew")                
        
        # Configure grid columns 
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)
        
        # Load orders data
        self.load_orders()
    
    def load_orders(self):
        # Clear existing rows
        for widget in self.table_container.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.grid_info()["row"] > 0:
                widget.destroy()
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Obter os pedidos do banco de dados
        pedidos = pedido.listar_tudo()
        print(pedidos)
        
        # Adicionar cada pedido como uma linha na tabela
        for row_index, pedido_data in enumerate(pedidos):
            self.add_row(row_index, pedido_data)
    
    def search_orders(self):
        # Clear existing rows
        for widget in self.table_container.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.grid_info()["row"] > 0:
                widget.destroy()
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Get search term
        search_term = self.search_bar.get().strip()
        
        # If search term is empty, load all orders
        if not search_term:
            self.load_orders()
            return
        
        # Search orders using the backend method
        pedidos = pedido.buscar(search_term)
        
        # Add matching orders to the table
        for row_index, pedido_data in enumerate(pedidos):
            self.add_row(row_index, pedido_data)
    
    def refresh_orders_table(self):
        # Reset search bar
        self.search_bar.delete(0, 'end')
        
        # Reload all orders
        self.load_orders()
    
    def add_row(self, row_index, data):      
        for col_index, value in enumerate(data):
            text_color = "black" 
            cell = ctk.CTkLabel(
                self.table_container,
                text=str(value),
                font=self.fonts["input_font"],
                fg_color=self.colors["table_bg"],
                text_color=text_color
            )
            cell.grid(row=row_index + 1, column=col_index, padx=10, pady=5, sticky="ew")