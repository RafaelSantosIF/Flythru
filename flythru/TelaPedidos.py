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

        # Updated search bar usando as fontes e cores do dicionário
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

        # Botão de filtro com as cores do dicionário
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

        # Table container com a cor de fundo da tabela
        self.table_container = ctk.CTkFrame(main_content, fg_color=self.colors["table_bg"])
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Table headers com a fonte header_font
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
                
        # Configure grid columns to expand properly
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)
        
        # Carregar e exibir os pedidos
        self.load_orders()

    # Método para carregar os pedidos do banco de dados
    def load_orders(self):
        # Obter os pedidos do banco de dados
        pedidos = pedido.listar_tudo()
        
        # Adicionar cada pedido como uma linha na tabela
        for row_index, pedido_data in enumerate(pedidos):
            self.add_row(row_index, pedido_data)
    
    # Método para adicionar linha de dados à tabela
    def add_row(self, row_index, data):
        # Aplicar cor alternada nas linhas
        bg_color = self.colors["table_row_alt"] if row_index % 2 == 1 else self.colors["table_bg"]
        
        for col_index, value in enumerate(data):
            text_color = "black" if self.colors["table_bg"] == "white" else self.colors["text_primary"]
            cell = ctk.CTkLabel(
                self.table_container,
                text=str(value),
                font=self.fonts["input_font"],
                fg_color=bg_color,
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