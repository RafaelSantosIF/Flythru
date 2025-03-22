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
        
        search_bar = ctk.CTkEntry(
            search_container,
            placeholder_text="🔎 Pesquisar Produto",
            font=self.fonts["input_font"],
            height=40,
            fg_color=self.colors["text_primary"],
            text_color=self.colors["dark_bg"],
            placeholder_text_color=self.colors["text_disabled"]
        )
        search_bar.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        filter_button = ctk.CTkButton(
            search_container,
            image=self.filter_icon,
            text="",
            width=28,
            height=28,
            fg_color=self.colors["text_primary"],
            hover_color=self.colors["primary_hover"],
            corner_radius=0,
            command=None
        )
        filter_button.place(relx=0.97, rely=0.5, anchor="center")
        
        self.table_container = ctk.CTkFrame(main_content, fg_color=self.colors["table_bg"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        headers = ["N°", "Data", "Descrição", "Valor (R$)", "Pagamento", " "]
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
        
        # Clear existing rows if any (important for reloading)
        for widget in self.table_container.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.grid_info()["row"] > 0:
                widget.destroy()
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Load orders data
        self.load_orders()
    
    # Método para carregar os pedidos do banco de dados
    def load_orders(self):
        # Obter os pedidos do banco de dados
        pedidos = pedido.listar_tudo()
        #pedidos_formatados = [pedidos[0],pedidos[1],f'{pedidos[2]} x{pedidos[3]}',pedidos[4]]
        print(pedidos)
        
        # Adicionar cada pedido como uma linha na tabela
        for row_index, pedido_data in enumerate(pedidos):
            self.add_row(row_index, pedido_data)
    
    def refresh_orders_table(self):
        # Clear existing rows
        for widget in self.table_container.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.grid_info()["row"] > 0:
                widget.destroy()
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Reload orders data
        self.load_orders()
    
    # Método para adicionar linha de dados à tabela
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
            
        # Adicionar botão de ações na última coluna
        action_button = ctk.CTkButton(
            self.table_container,
            text="Detalhes",
            font=self.fonts["button_font"],
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            corner_radius=8,
            width=100,
            command=lambda idx=row_index: self.show_order_details(idx)
        )
        action_button.grid(row=row_index + 1, column=len(data), padx=10, pady=5)
    
    def show_order_details(self, order_index):
        # Função para exibir detalhes do pedido
        print(f"Exibindo detalhes do pedido {order_index}")
        # Implementar a lógica para exibir detalhes do pedido