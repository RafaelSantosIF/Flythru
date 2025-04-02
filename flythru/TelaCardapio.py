import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc
from api.pedido.pedido import Pedido
from api.cardapio.item_cardapio import Item_Cardapio
from api.estoque.estoque import Estoque

pedido = Pedido()
cardapio = Item_Cardapio()
estoque = Estoque()

class CarteMenu:
    def __init__(self):
        self.table_container = None
        self.total_price = 0.0
        self.total_label = None
        self.order_items = []
        self.order_id = 1
        self.categories = {}  
        self.fonts = None
        self.colors = None
        self.root = None
        self.main_menu = None
        self.main_content = None
        self.load_menu_items()  
    
    def set_main_menu(self, main_menu):
        self.main_menu = main_menu
            
    def load_menu_items(self):
        """Carrega os itens do cardápio a partir do banco de dados."""
        itens_cardapio = cardapio.listar_tudo()  # Busca os itens do cardápio
        
        # Define default categories that should always appear
        default_categories = ["Hambúrguer", "Batatas", "Refrigerantes", "Outros"]
        
        # Initialize categories dictionary with empty lists for each default category
        self.categories = {categoria: [] for categoria in default_categories}
        
        # Organize items from database into appropriate categories
        for item in itens_cardapio:
            codCardapio, nome, preco, listaProdutos, listaQuantidades, category = item
            # Define a categoria com base no nome do item
            if "Hambúrguer" in category:
                categoria = "Hambúrguer"
            elif "Batatas" in category:
                categoria = "Batatas"
            elif "Refrigerantes" in category:
                categoria = "Refrigerantes"
            else:
                categoria = "Outros"  # Categoria padrão para itens que não se encaixam nas outras

            # Processar ingredientes que agora incluem quantidades
            produtos_lista = listaProdutos.split("--")
            produtos_formatados = []
            for prod in produtos_lista:
                if prod:  # Verificar se não está vazio
                    produtos_formatados.append(prod)

            # Adiciona o item à categoria correspondente
            self.categories[categoria].append((nome, preco, "round_logo.png", produtos_formatados))
            
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

    def update_total(self):
        if self.total_label:
            self.total_label.configure(text=f"Sub-Total R$ {self.total_price:.2f}")

    def add_to_order(self, name, price, quantity_var):
        quantity = int(quantity_var.get())
        if quantity > 0:
            total_item_price = price * quantity
            self.total_price += total_item_price

            self.order_items.append({
                "id": f"#{self.order_id:02d}",
                "item": name,
                "qty": f"{quantity}",
                "price": f"R$ {total_item_price:.2f}"
            })
            self.order_id += 1

            self.update_total()
            quantity_var.set("0")

    def remove_item(self, item_frame, item):
        item_frame.destroy()
        self.order_items.remove(item)
        item_price = float(item["price"].replace("R$ ", ""))
        self.total_price -= item_price
        self.update_total()

    def clear_order(self, order_screen):
        self.order_items.clear()
        self.total_price = 0.0
        self.update_total()
        order_screen.destroy()

    def refresh_orders_after_save(self):
        if self.main_menu and hasattr(self.main_menu, 'orders_menu'):
            self.main_menu.orders_menu.refresh_orders_table()
    
    def open_order_screen(self):
        order_screen = ctk.CTkToplevel()
        order_screen.title("FlyThru - Comanda")
        order_screen.geometry("500x600")
        order_screen.resizable(False, False)
        order_screen.overrideredirect(True)
        order_screen.grab_set()
        order_screen.focus_force()

        # Top bar
        top_bar = ctk.CTkFrame(order_screen, fg_color=self.colors["main_color"], height=50)
        top_bar.pack(side="top", fill="x")

        # Header frame
        header_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=30,
            fg_color="transparent",
            hover_color=self.colors["hover_color"],
            command=order_screen.destroy
        )
        back_button.pack(side="left")

        # Order number
        order_label = ctk.CTkLabel(
            header_frame,
            text="Comanda #2308",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="white"
        )
        order_label.pack(fill="x", side="left", padx=10)

        # Add dragging functionality
        from MainMenu import WindowDragging
        WindowDragging(order_screen, header_frame)

        # Main content frame
        content_frame = ctk.CTkFrame(order_screen, fg_color="#2b2b2b")
        content_frame.pack(fill="both", expand=True)

        # Headers
        headers_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        headers_frame.pack(fill="x", padx=20, pady=10)

        # Column labels
        column_widths = [50, 180, 50, 100]
        headers = ["ID", "Item", "Qnt.", "Preço"]

        for i, (header, width) in enumerate(zip(headers, column_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(family="Verdana", size=12),
                text_color="gray",
                width=width
            )
            header_label.grid(row=0, column=i, sticky="w", padx=5)

        # Items frame
        items_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        items_frame.pack(fill="both", expand=True, padx=20)

        order_description = ''
        quantidade_description = ''

        # Display order items
        for item in self.order_items:
            item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=5)
            order_description+= f"{item['item']}\n"
            quantidade_description += f"{item['qty']}\n"

            ctk.CTkLabel(item_frame, text=item["id"], width=50).grid(row=0, column=0, padx=5, sticky="w")
            ctk.CTkLabel(item_frame, text=item["item"], width=180).grid(row=0, column=1, padx=5, sticky="w")
            ctk.CTkLabel(item_frame, text=item["qty"], width=50).grid(row=0, column=2, padx=5, sticky="w")
            ctk.CTkLabel(item_frame, text=item["price"], width=100).grid(row=0, column=3, padx=5, sticky="w")

            delete_button = ctk.CTkButton(
                item_frame,
                text="✕",
                width=20,
                fg_color="transparent",
                hover_color="#ff4444",
                command=lambda f=item_frame, i=item: self.remove_item(f, i)
            )
            delete_button.grid(row=0, column=4, padx=5)

        # Bottom frame
        bottom_frame = ctk.CTkFrame(order_screen, fg_color="white", height=120)
        bottom_frame.pack(side="bottom", fill="x")

        # Total amount label
        total_amount = ctk.CTkLabel(
            bottom_frame,
            text=f"R$ {self.total_price:.2f}",
            font=ctk.CTkFont(family="Verdana", size=14, weight="bold"),
            text_color="black"
        )
        total_amount.pack(anchor="e", padx=20)

        # Payment method selection
        payment_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        payment_frame.pack(fill="x", padx=20, pady=(5, 0))
        
        payment_label = ctk.CTkLabel(
            payment_frame,
            text="Forma de Pagamento:",
            font=ctk.CTkFont(family="Verdana", size=12),
            text_color="black"
        )
        payment_label.pack(anchor="w")
        
        # Payment options
        payment_options_frame = ctk.CTkFrame(payment_frame, fg_color="transparent")
        payment_options_frame.pack(fill="x", pady=(0, 5))
        
        payment_method_var = ctk.StringVar(value="cartão de Crédito")
        
        credit_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Cartão de Crédito",
            variable=payment_method_var,
            value="cartão de Crédito",
            font=ctk.CTkFont(family="Verdana", size=11),
            text_color="black"
        )
        credit_radio.pack(side="left", padx=(0, 15))
        
        debit_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Cartão de Débito",
            variable=payment_method_var,
            value="cartão de Débito",
            font=ctk.CTkFont(family="Verdana", size=11),
            text_color="black"
        )
        debit_radio.pack(side="left", padx=(0, 15))
        
        cash_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="Dinheiro",
            variable=payment_method_var,
            value="dinheiro",
            font=ctk.CTkFont(family="Verdana", size=11),
            text_color="black"
        )
        cash_radio.pack(side="left", padx=(0, 15))
        
        pix_radio = ctk.CTkRadioButton(
            payment_options_frame,
            text="PIX",
            variable=payment_method_var,
            value="PIX",
            font=ctk.CTkFont(family="Verdana", size=11),
            text_color="black"
        )
        pix_radio.pack(side="left")

        # Buttons frame
        buttons_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)       

        finish_button = ctk.CTkButton(
            buttons_frame,
            text="Finalizar Pedido",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=35,
            command=lambda: [
                # Primeiro salva o pedido
                pedido.save(order_description, quantidade_description, self.total_price, payment_method_var.get()),
                
                # Atualiza o estoque imediatamente (antes de mostrar a confirmação)
                self.update_inventory_from_order(),
                
                # Mostra a tela de confirmação
                self.show_confirmation_screen(
                    order_screen, 
                    order_description, 
                    quantidade_description, 
                    self.total_price, 
                    payment_method_var.get()
                ),
                
                # Limpa o pedido atual
                self.clear_order(order_screen),
                
                # Atualiza a lista de pedidos
                self.refresh_orders_after_save()
            ]
        )
        finish_button.pack(side="left", expand=True, padx=(0, 10))

        # Trash button
        trash_button = ctk.CTkButton(
            buttons_frame,
            text="🗑",
            width=35,
            height=35,
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            command=lambda: self.clear_order(order_screen)
        )
        trash_button.pack(side="right")

    def delete_menu_item(self, category, index):
        """Delete an item from the menu category"""
        if 0 <= index < len(self.categories[category]):
            cardapio.delete(self.categories[category][index][0])
            del self.categories[category][index]
            self.refresh_menu()

    def add_new_item(self, category):
        """Open a dialog to add a new item to the specified category"""
        # Create a new window for adding an item with the same style as the order screen
        add_window = ctk.CTkToplevel()
        add_window.title(f"Adicionar Item - {category}")

        # Get screen dimensions
        screen_width = add_window.winfo_screenwidth()
        screen_height = add_window.winfo_screenheight()

        # Set a more appropriate window size
        window_width = 450  # Reduced from 500
        window_height = 550  # Reduced from 600

        # Calculate position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set window geometry with position and size
        add_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        add_window.resizable(False, False)
        add_window.overrideredirect(True)
        add_window.grab_set()
        add_window.focus_force()

        # Top bar
        top_bar = ctk.CTkFrame(add_window, fg_color=self.colors["main_color"], height=50)
        top_bar.pack(side="top", fill="x")

        # Header frame
        header_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=30,
            fg_color="transparent",
            hover_color=self.colors["hover_color"],
            command=add_window.destroy
        )
        back_button.pack(side="left")

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"Adicionar Novo {category}",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="white"
        )
        title_label.pack(fill="x", side="left", padx=10)

        # Add dragging functionality
        from MainMenu import WindowDragging
        WindowDragging(add_window, header_frame)

        # Main content frame
        content_frame = ctk.CTkFrame(add_window, fg_color="#2b2b2b")
        content_frame.pack(fill="both", expand=True)

        # Form fields
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=15, pady=15)  # Reduced padding

        # Name field
        name_label = ctk.CTkLabel(
            form_frame,
            text="Nome do Item:",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        name_label.pack(fill="x", pady=(5, 5))  # Reduced padding

        name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            form_frame,
            textvariable=name_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35
        )
        name_entry.pack(fill="x", pady=(0, 10))  # Reduced from 15

        # Price field
        price_label = ctk.CTkLabel(
            form_frame,
            text="Preço (R$):",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        price_label.pack(fill="x", pady=(5, 5))  # Reduced padding

        price_var = ctk.StringVar()
        price_entry = ctk.CTkEntry(
            form_frame,
            textvariable=price_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35,
            placeholder_text="0.00"
        )
        price_entry.pack(fill="x", pady=(0, 10))  # Reduced from 15

        # Ingredients selection section
        ingredients_label = ctk.CTkLabel(
            form_frame,
            text="Ingredientes:",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        ingredients_label.pack(fill="x", pady=(5, 5))  # Reduced padding

        # Lista de ingredientes disponíveis com suas quantidades
        ingredientes_back = estoque.listar_tudo()
        available_ingredients = []
        for ingrediente in ingredientes_back:
            ingrediente_unidade = ''
            if ingrediente[3] == "Bebidas":
                ingrediente_unidade = 'ml'
            elif ingrediente[3] == "Carnes" or ingrediente[3] == "Laticíneos" or ingrediente[3] == "Verduras" or ingrediente[3] == "Laticínios":
                ingrediente_unidade = 'g'
            else:
                ingrediente_unidade = 'un'
            
            available_ingredients.append({
                "name": ingrediente[1],
                "unit": ingrediente_unidade,#categoria
                "default_qty": ingrediente[2]
            })

        # Lista para armazenar ingredientes selecionados com suas quantidades
        selected_ingredients = []

        # Frame para seleção de ingredientes
        selection_frame = ctk.CTkFrame(form_frame, fg_color="#3E3E3E")
        selection_frame.pack(fill="x", pady=(0, 5))

        # Combobox para selecionar ingredientes
        ingredient_var = ctk.StringVar()
        ingredient_names = [item["name"] for item in available_ingredients]
        ingredient_dropdown = ctk.CTkComboBox(
            selection_frame,
            values=ingredient_names,
            variable=ingredient_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35,
            width=180  # Reduced from 200
        )
        ingredient_dropdown.pack(side="left", padx=(10, 5), pady=10)

        # Variável e campo para a quantidade
        quantity_var = ctk.StringVar(value="")
        quantity_entry = ctk.CTkEntry(
            selection_frame,
            textvariable=quantity_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            width=50,  # Reduced from 60
            height=35,
            placeholder_text="Qtd"
        )
        quantity_entry.pack(side="left", padx=(0, 5), pady=10)
        
        # Rótulo de unidade (será atualizado dinamicamente)
        unit_label = ctk.CTkLabel(
            selection_frame,
            text="",
            font=ctk.CTkFont(family="Verdana", size=12),
            width=30
        )
        unit_label.pack(side="left", pady=10)

        # Função para atualizar o valor padrão e a unidade quando o ingrediente é selecionado
        def update_quantity_default(*args):
            selected = ingredient_var.get()
            for ing in available_ingredients:
                if ing["name"] == selected:
                    quantity_var.set(str(ing["default_qty"]))
                    unit_label.configure(text=ing["unit"])
                    break

        # Vincular a função ao ComboBox
        ingredient_var.trace_add("write", update_quantity_default)

        # Definir o valor inicial
        if ingredient_names:
            ingredient_var.set(ingredient_names[0])
            update_quantity_default()

        # Função para adicionar ingrediente à lista
        def add_ingredient():
            selected = ingredient_var.get()
            quantity = quantity_var.get().strip()

            # Verificar se os campos estão preenchidos
            if not selected or not quantity:
                return

            try:
                quantity = float(quantity.replace(',', '.'))
            except ValueError:
                # Mostrar mensagem de erro
                error_label = ctk.CTkLabel(
                    selection_frame,
                    text="Quantidade inválida!",
                    font=ctk.CTkFont(family="Verdana", size=10),
                    text_color="red"
                )
                error_label.pack(side="right", padx=5)
                selection_frame.after(2000, error_label.destroy)
                return

            # Encontrar a unidade do ingrediente selecionado
            unit = ""
            for ing in available_ingredients:
                if ing["name"] == selected:
                    unit = ing["unit"]
                    break

            # Verificar se o ingrediente já está na lista
            for i, item in enumerate(selected_ingredients):
                if item["name"] == selected:
                    # Atualizar a quantidade
                    selected_ingredients[i]["quantity"] = quantity
                    update_ingredients_list()
                    return

            # Adicionar à lista de ingredientes selecionados
            selected_ingredients.append({
                "name": selected,
                "quantity": quantity,
                "unit": unit
            })
            update_ingredients_list()

        # Botão para adicionar ingrediente
        add_ingredient_button = ctk.CTkButton(
            selection_frame,
            text="+",
            width=30,  # Reduced from 35
            height=30,  # Reduced from 35
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=add_ingredient
        )
        add_ingredient_button.pack(side="right", padx=10, pady=10)

        # Frame para exibir os ingredientes selecionados
        ingredients_display_frame = ctk.CTkFrame(form_frame, fg_color="#3E3E3E",
                                                 height=100)  # Reduced from 180 to 100
        ingredients_display_frame.pack(fill="x", pady=(0, 10))  # Reduced from 15
        ingredients_display_frame.pack_propagate(False)  # Manter altura fixa

        # Função para atualizar a lista de ingredientes
        def update_ingredients_list():
            # Limpar o frame primeiro
            for widget in ingredients_display_frame.winfo_children():
                widget.destroy()

            # Criar um frame para scrolling
            scroll_frame = ctk.CTkScrollableFrame(ingredients_display_frame, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True)

            # Mostrar ingredientes selecionados
            for i, ingredient in enumerate(selected_ingredients):
                ingredient_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                ingredient_row.pack(fill="x", padx=5, pady=2)

                # Mostrar nome e quantidade
                ingredient_text = f"• {ingredient['name']} - {ingredient['quantity']} {ingredient['unit']}"
                ingredient_label = ctk.CTkLabel(
                    ingredient_row,
                    text=ingredient_text,
                    font=ctk.CTkFont(family="Verdana", size=12),
                    text_color="white",
                    anchor="w"
                )
                ingredient_label.pack(side="left", fill="x", expand=True)

                # Botão para remover ingrediente
                def remove_ingredient(idx=i):
                    selected_ingredients.pop(idx)
                    update_ingredients_list()

                remove_button = ctk.CTkButton(
                    ingredient_row,
                    text="✕",
                    width=20,  # Reduced from 25
                    height=20,  # Reduced from 25
                    fg_color="transparent",
                    hover_color="#ff4444",
                    command=lambda idx=i: remove_ingredient(idx)
                )
                remove_button.pack(side="right")

        # Inicializar o frame de ingredientes
        update_ingredients_list()

        # Bottom frame
        bottom_frame = ctk.CTkFrame(add_window, fg_color="white", height=60)  # Reduced from 80
        bottom_frame.pack(side="bottom", fill="x")

        # Add item button
        def confirm_add_item():
            # Get values from form
            name = name_var.get()

            try:
                price = float(price_var.get().replace(',', '.'))
            except ValueError:
                # Show error if price is invalid
                error_label = ctk.CTkLabel(
                    bottom_frame,
                    text="Preço inválido!",
                    font=ctk.CTkFont(family="Verdana", size=12),
                    text_color="red"
                )
                error_label.pack(side="left", padx=20)
                bottom_frame.after(2000, error_label.destroy)
                return

            if not name or not selected_ingredients:
                # Show error if name or ingredients are empty
                error_label = ctk.CTkLabel(
                    bottom_frame,
                    text="Nome e ingredientes são obrigatórios!",
                    font=ctk.CTkFont(family="Verdana", size=12),
                    text_color="red"
                )
                error_label.pack(side="left", padx=20)
                bottom_frame.after(2000, error_label.destroy)
                return

            # Criar lista de nomes de ingredientes para salvar no formato original (Mudei aqui)
            ingredients_list = []
            quantidade_list = []
            lista_ingredientes = ''
            ingredients_quant = ""
            for item in selected_ingredients:
                # Formato: nome_ingrediente(quantidade unidade)
                ing_with_qty = f"{item['name']}"
                ingredients_list.append(ing_with_qty)
                lista_ingredientes += ing_with_qty + "--"

                numberQuantidade = f"{item['quantity']}"
                quantidade_list.append(numberQuantidade)
                ingredients_quant += numberQuantidade + "--"

            # O resto permanece similar
            self.categories[category].append((name, price, "round_logo.png", ingredients_list))
            cardapio.save(name, price, lista_ingredientes,ingredients_quant, category)

            # Refresh the menu
            self.refresh_menu()

            # Close the window
            add_window.destroy()

        add_button = ctk.CTkButton(
            bottom_frame,
            text="Confirmar",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=30,  # Reduced from 35
            command=confirm_add_item
        )
        add_button.pack(side="left", expand=True, padx=15, pady=15)  # Reduced padding

        # Cancel button
        cancel_button = ctk.CTkButton(
            bottom_frame,
            text="Cancelar",
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=30,  # Reduced from 35
            command=add_window.destroy
        )
        cancel_button.pack(side="right", padx=15, pady=15)  # Reduced padding

    def refresh_menu(self):
        """Refresh the menu content to reflect changes"""
        if hasattr(self, 'main_content'):
            # First, remove the entire main_content from the root
            self.main_content.pack_forget()

            # Destroy the old main_content frame completely
            self.main_content.destroy()

            # Recreate the menu by calling create_main_content
            self.create_main_content(self.main_menu, self.root)

    def create_card(self, parent, name, price, img, ingredients, idx, category):
        """Create a menu item card with fixed dimensions"""
        # Compact card with reduced height
        card = ctk.CTkFrame(parent, fg_color="#2E2E2E", corner_radius=10, width=180, height=280)
        card.grid_propagate(False)  # Prevent the card from resizing based on content

        # Smaller image with reduced padding
        image = self.load_image(img, (70, 70))
        if image:
            img_label = ctk.CTkLabel(card, image=image, text="")
            img_label.pack(pady=(5, 2))

        # Name with reduced padding
        name_label = ctk.CTkLabel(card, text=name, font=self.fonts["menu_font"], text_color="white")
        name_label.pack(pady=(2, 0))

        # Price with reduced padding
        price_label = ctk.CTkLabel(card, text=f"R$ {price:.2f}", font=self.fonts["input_font"], text_color="white")
        price_label.pack(pady=(0, 2))

        # Compact ingredients frame
        ingredients_frame = ctk.CTkFrame(card, fg_color="transparent", height=80)
        ingredients_frame.pack(pady=(0, 2), fill="x", padx=5)
        ingredients_frame.pack_propagate(False)  # Keep height fixed

        # Reduced max visible ingredients
        max_ingredients = 4
        display_ingredients = ingredients[:max_ingredients]

        # Smaller font for ingredients
        for ing in display_ingredients:
            ing_label = ctk.CTkLabel(
                ingredients_frame,
                text="• " + ing,
                font=ctk.CTkFont(family="Verdana", size=9),
                text_color="white",
                anchor="w",
                wraplength=150
            )
            ing_label.pack(fill="x", pady=0)

        # Compact quantity frame
        quantity_frame = ctk.CTkFrame(card, fg_color="transparent")
        quantity_frame.pack(fill="x", padx=10, pady=(2, 0))

        quantity_var = ctk.StringVar(value="0")
        quantity_entry = ctk.CTkEntry(
            quantity_frame,
            textvariable=quantity_var,
            width=40,
            height=22,
            fg_color="#3E3E3E",
            border_color="#555555"
        )
        quantity_entry.pack(side="left")

        # Smaller quantity buttons
        minus_btn = ctk.CTkButton(
            quantity_frame,
            text="-",
            width=22,
            height=22,
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            command=lambda: quantity_var.set(str(max(0, int(quantity_var.get()) - 1)))
        )
        minus_btn.pack(side="left", padx=(5, 0))

        plus_btn = ctk.CTkButton(
            quantity_frame,
            text="+",
            width=22,
            height=22,
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            command=lambda: quantity_var.set(str(int(quantity_var.get()) + 1))
        )
        plus_btn.pack(side="left", padx=(5, 0))

        # Buttons frame with reduced padding
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(2, 5))

        # ADD button
        add_button = ctk.CTkButton(
            buttons_frame,
            text="+ ADD",
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            font=self.fonts["button_font"],
            command=lambda n=name, p=price, q=quantity_var: self.add_to_order(n, p, q),
            height=22,
            width=100
        )
        add_button.pack(side="left", fill="x", expand=True)
        
        # Edit button - moved back to bottom
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="✎",
            fg_color="#4CAF50",
            hover_color="#45a049",
            text_color="white",
            font=self.fonts["button_font"],
            command=lambda cat=category, i=idx: self.edit_menu_item(cat, i),
            height=22,
            width=22,
            corner_radius=4
        )
        edit_button.pack(side="right", padx=(5, 0))
        
        # Delete button - moved back to bottom
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑",
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=self.fonts["button_font"],
            command=lambda cat=category, i=idx: self.delete_menu_item(cat, i),
            height=22,
            width=22
        )
        delete_button.pack(side="right", padx=(5, 0))

        return card

    def update_inventory_from_order(self):
        """
        Atualiza o estoque subtraindo os ingredientes utilizados no pedido atual.
        Chamado quando um pedido é finalizado.
        """
        if not self.order_items:
            return
        
        # Dicionário para acumular o uso total de ingredientes em todos os itens do pedido
        total_ingredient_usage = {}
        
        # Processa cada item no pedido
        for order_item in self.order_items:
            item_name = order_item["item"]
            item_quantity = int(order_item["qty"].replace("x", ""))
            
            # Encontra o item nas categorias do menu
            for category, items in self.categories.items():
                for name, price, img, ingredients in items:
                    if name == item_name:
                        # Processa cada ingrediente neste item do menu
                        for ingredient_str in ingredients:
                            # Analisa a string do ingrediente - formato é "Nome(quantidadeunidade)"
                            # Extrai nome e quantidade
                            if "(" in ingredient_str and ")" in ingredient_str:
                                ingredient_name = ingredient_str.split("(")[0]
                                quantity_str = ingredient_str.split("(")[1].split(")")[0]
                                
                                # Extrai quantidade numérica e unidade
                                # Lida com diferentes formatos (ex: "100g", "250ml")
                                import re
                                match = re.match(r"([\d.]+)([a-zA-Z]+)", quantity_str)
                                if match:
                                    try:
                                        ingredient_quantity = float(match.group(1))
                                        ingredient_unit = match.group(2)
                                        
                                        # Calcula o uso total para este ingrediente neste item do pedido
                                        total_usage = ingredient_quantity * item_quantity
                                        
                                        # Acumula no dicionário de uso total
                                        if ingredient_name in total_ingredient_usage:
                                            total_ingredient_usage[ingredient_name] += total_usage
                                        else:
                                            total_ingredient_usage[ingredient_name] = total_usage
                                    except ValueError:
                                        print(f"Erro ao converter quantidade: {quantity_str}")
        
        # Agora atualiza o estoque no banco de dados subtraindo todos os ingredientes acumulados
        for ingredient_name, usage_amount in total_ingredient_usage.items():
            # Obtém o nível atual de estoque para este ingrediente
            current_inventory = self.get_quantidade_by_nome(ingredient_name)
            if current_inventory is not None:
                # Calcula o novo nível de estoque
                new_quantity = max(0, current_inventory - usage_amount)
                # Atualiza o estoque no banco de dados
                self.update_quantidade(ingredient_name, new_quantity)
                print(f"Atualizado estoque: {ingredient_name} de {current_inventory} para {new_quantity}")


    def get_quantidade_by_nome(self, nome):
       
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT quantidade FROM estoque WHERE nome = ?", (nome,))
            result = cursor.fetchone()
            
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Erro ao buscar quantidade: {e}")
            return None
        finally:
            if conn:
                conn.close()

    
    def update_quantidade(self, nome, nova_quantidade):
     
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE estoque SET quantidade = ? WHERE nome = ?", 
                        (nova_quantidade, nome))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar quantidade: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def create_category_section(self, parent, category, items):
        
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", pady=10, padx=10)

        # Category heading
        category_label = ctk.CTkLabel(
            section_frame,
            text=category,
            font=self.fonts["menu_font"],
            text_color="white"
        )
        category_label.pack(anchor="w", pady=5)

        # Create a frame to hold the cards in a grid layout
        cards_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        cards_container.pack(fill="x", pady=5)

        # Define max cards per row
        max_cards_per_row = 6
        rows = (len(items) + 1) // max_cards_per_row + 1  # +1 for the plus card

        # Create item cards in a grid layout
        for idx, (name, price, img, ingredients) in enumerate(items):
            row = idx // max_cards_per_row
            col = idx % max_cards_per_row

            card = self.create_card(cards_container, name, price, img, ingredients, idx, category)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Add the plus card at the appropriate position
        row = len(items) // max_cards_per_row
        col = len(items) % max_cards_per_row

        # Adicionar o card de "+"
        plus_card = ctk.CTkFrame(
            cards_container,
            border_width=2,
            border_color="#2E2E2E",
            fg_color="transparent",
            corner_radius=10,
            width=180,
            height=320
        )
        plus_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        plus_card.grid_propagate(False)  # Prevent resizing

        # Center the plus button
        plus_image = self.load_image("plus_square.png", (45, 45))
        add_button_frame = ctk.CTkFrame(plus_card, fg_color="transparent")
        add_button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add plus button
        if plus_image:
            add_new_button = ctk.CTkButton(
                add_button_frame,
                image=plus_image,
                text="",
                fg_color="transparent",
                width=50,
                height=50,
                corner_radius=10,
                command=lambda cat=category: self.add_new_item(cat)
            )
        else:
            add_new_button = ctk.CTkButton(
                add_button_frame,
                text="+",
                fg_color=self.colors["main_color"],
                hover_color=None,
                width=50,
                height=50,
                corner_radius=10,
                font=ctk.CTkFont(family="Verdana", size=24),
                command=lambda cat=category: self.add_new_item(cat)
            )
        add_new_button.pack()

        # Configure grid for proper spacing
        for i in range(max_cards_per_row):
            cards_container.grid_columnconfigure(i, minsize=180, weight=1)

        return section_frame

    def create_main_content(self, main_menu, root):
        self.fonts = main_menu.fonts
        self.colors = main_menu.colors
        self.root = root
        self.main_menu = main_menu

        # Main content frame
        self.main_content = ctk.CTkFrame(root, fg_color=self.colors["dark_bg"])
        self.main_content.pack(side="right", fill="both", expand=True)

        # Create scrollable container for vertical scrolling
        container_frame = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color=self.colors["dark_bg"],
            orientation="vertical"
        )
        container_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Create each category section with grid layout
        for category, items in self.categories.items():
            self.create_category_section(container_frame, category, items)

        # Bottom frame
        bottom_frame = ctk.CTkFrame(self.main_content, fg_color="#D3D3D3", height=50, corner_radius=0)
        bottom_frame.pack(side="bottom", fill="x")

        self.total_label = ctk.CTkLabel(
            bottom_frame,
            text=f"Sub-Total R$ {self.total_price:.2f}",
            font=self.fonts["menu_font"],
            text_color="black"
        )
        self.total_label.pack(side="left", padx=20)

        generate_order_button = ctk.CTkButton(
            bottom_frame,
            text="Gerar Comanda",
            fg_color="green",
            hover_color="darkgreen",
            font=self.fonts["button_font"],
            text_color="white",
            command=self.open_order_screen
        )
        generate_order_button.pack(side="right", padx=20, pady=5)

    def edit_menu_item(self, category, index):
        """Open a dialog to edit an existing menu item with optimized performance"""
        # Get the item to edit
        item = self.categories[category][index]
        name, price, img, ingredients = item

        # Create a new window for editing an item
        edit_window = ctk.CTkToplevel()
        edit_window.title(f"Editar Item - {name}")

        # Window configuration
        edit_window.geometry("450x550")
        edit_window.resizable(False, False)
        edit_window.overrideredirect(True)
        edit_window.grab_set()
        edit_window.focus_force()
        
        # Center window
        edit_window.update_idletasks()
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()
        x = (screen_width - edit_window.winfo_width()) // 2
        y = (screen_height - edit_window.winfo_height()) // 2
        edit_window.geometry(f"+{x}+{y}")

        # Colors
        main_color = self.colors["main_color"]
        hover_color = self.colors["hover_color"]
        bg_color = "#2b2b2b"
        frame_color = "#3E3E3E"

        # Top bar
        top_bar = ctk.CTkFrame(edit_window, fg_color=main_color, height=50)
        top_bar.pack(side="top", fill="x")

        # Header frame
        header_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=30,
            fg_color="transparent",
            hover_color=hover_color,
            command=edit_window.destroy
        )
        back_button.pack(side="left")

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"Editar {name}",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="white"
        )
        title_label.pack(fill="x", side="left", padx=10)

        # Add dragging functionality
        from MainMenu import WindowDragging
        WindowDragging(edit_window, header_frame)

        # Main content frame
        content_frame = ctk.CTkFrame(edit_window, fg_color=bg_color)
        content_frame.pack(fill="both", expand=True)

        # Form fields
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Name field
        name_var = ctk.StringVar(value=name)
        name_label = ctk.CTkLabel(
            form_frame,
            text="Nome do Item:",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        name_label.pack(fill="x", pady=(5, 5))

        name_entry = ctk.CTkEntry(
            form_frame,
            textvariable=name_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35
        )
        name_entry.pack(fill="x", pady=(0, 10))

        # Price field
        price_var = ctk.StringVar(value=str(price))
        price_label = ctk.CTkLabel(
            form_frame,
            text="Preço (R$):",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        price_label.pack(fill="x", pady=(5, 5))

        price_entry = ctk.CTkEntry(
            form_frame,
            textvariable=price_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35,
            placeholder_text="0.00"
        )
        price_entry.pack(fill="x", pady=(0, 10))

        # Ingredients section
        ingredients_label = ctk.CTkLabel(
            form_frame,
            text="Ingredientes:",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        ingredients_label.pack(fill="x", pady=(5, 5))

        # Get available ingredients (optimized to run once)
        ingredientes_back = estoque.listar_tudo()
        available_ingredients = []
        for ingrediente in ingredientes_back:
            unit = 'ml' if ingrediente[3] == "Bebidas" else 'g' if ingrediente[3] in ["Carnes", "Laticíneos", "Verduras", "Laticínios"] else 'un'
            available_ingredients.append({
                "name": ingrediente[1],
                "unit": unit,
                "default_qty": ingrediente[2]
            })

        # Get current item ingredients
        current_item_db = cardapio.listByName(name)
        selected_ingredients = []
        if current_item_db and current_item_db[0]:
            db_ingredients = current_item_db[0][3].split('--') if current_item_db[0][3] else []
            db_quantities = current_item_db[0][4].split('--') if current_item_db[0][4] else []
            
            for ing, qty in zip(db_ingredients, db_quantities):
                if ing and ing.strip():
                    selected_ingredients.append({
                        "name": ing.strip(),
                        "quantity": qty.strip()
                    })

        # Ingredients selection frame
        selection_frame = ctk.CTkFrame(form_frame, fg_color=frame_color)
        selection_frame.pack(fill="x", pady=(0, 5))

        # Ingredient dropdown
        ingredient_var = ctk.StringVar()
        ingredient_names = [item["name"] for item in available_ingredients]
        ingredient_dropdown = ctk.CTkComboBox(
            selection_frame,
            values=ingredient_names,
            variable=ingredient_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35,
            width=180
        )
        ingredient_dropdown.pack(side="left", padx=(10, 5), pady=10)

        # Quantity field
        quantity_var = ctk.StringVar(value="")
        quantity_entry = ctk.CTkEntry(
            selection_frame,
            textvariable=quantity_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            width=50,
            height=35,
            placeholder_text="Qtd"
        )
        quantity_entry.pack(side="left", padx=(0, 5), pady=10)
        
        # Unit label
        unit_label = ctk.CTkLabel(
            selection_frame,
            text="",
            font=ctk.CTkFont(family="Verdana", size=12),
            width=30
        )
        unit_label.pack(side="left", pady=10)

        # Update quantity default value
        def update_quantity_default(*args):
            selected = ingredient_var.get()
            for ing in available_ingredients:
                if ing["name"] == selected:
                    quantity_var.set(str(ing["default_qty"]))
                    unit_label.configure(text=ing["unit"])
                    break

        ingredient_var.trace_add("write", update_quantity_default)
        if ingredient_names:
            ingredient_var.set(ingredient_names[0])
            update_quantity_default()

        # Add ingredient button
        add_ingredient_button = ctk.CTkButton(
            selection_frame,
            text="+",
            width=30,
            height=30,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: self._add_ingredient(
                ingredient_var, quantity_var, selected_ingredients, 
                available_ingredients, ingredients_display_frame
            )
        )
        add_ingredient_button.pack(side="right", padx=10, pady=10)

        # Ingredients display frame
        ingredients_display_frame = ctk.CTkFrame(form_frame, fg_color=frame_color, height=100)
        ingredients_display_frame.pack(fill="x", pady=(0, 10))
        ingredients_display_frame.pack_propagate(False)

        # Initial update of ingredients list
        self._update_ingredients_list(selected_ingredients, ingredients_display_frame)

        # Bottom frame (ensure it's always visible)
        bottom_frame = ctk.CTkFrame(edit_window, fg_color="white", height=60)
        bottom_frame.pack(side="bottom", fill="x", pady=(0, 0))  # Explicit pady=0 to prevent overlap

        # Confirm edit button
        edit_button = ctk.CTkButton(
            bottom_frame,
            text="Confirmar Edição",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=30,
            command=lambda: self._confirm_edit_item(
                edit_window, category, index, name_var, price_var, 
                selected_ingredients, name, category
            )
        )
        edit_button.pack(side="left", expand=True, padx=15, pady=15)

        # Cancel button
        cancel_button = ctk.CTkButton(
            bottom_frame,
            text="Cancelar",
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=30,
            command=edit_window.destroy
        )
        cancel_button.pack(side="right", padx=15, pady=15)

        # Make sure the window is properly rendered
        edit_window.update()

    def _add_ingredient(self, ingredient_var, quantity_var, selected_ingredients, available_ingredients, display_frame):
        """Helper method to add an ingredient to the list"""
        selected = ingredient_var.get()
        quantity = quantity_var.get().strip()

        if not selected or not quantity:
            return

        try:
            quantity = float(quantity.replace(',', '.'))
        except ValueError:
            error_label = ctk.CTkLabel(
                display_frame,
                text="Quantidade inválida!",
                font=ctk.CTkFont(family="Verdana", size=10),
                text_color="red"
            )
            error_label.pack()
            display_frame.after(2000, error_label.destroy)
            return

        # Check if ingredient already exists
        for i, item in enumerate(selected_ingredients):
            if item["name"] == selected:
                selected_ingredients[i]["quantity"] = str(quantity)
                self._update_ingredients_list(selected_ingredients, display_frame)
                return

        # Add new ingredient
        selected_ingredients.append({"name": selected, "quantity": str(quantity)})
        self._update_ingredients_list(selected_ingredients, display_frame)

    def _update_ingredients_list(self, selected_ingredients, display_frame):
        """Helper method to update the ingredients list display"""
        # Clear the frame
        for widget in display_frame.winfo_children():
            widget.destroy()

        # Create scrollable frame if there are many ingredients
        if len(selected_ingredients) > 3:
            scroll_frame = ctk.CTkScrollableFrame(display_frame, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True)
            parent_frame = scroll_frame
        else:
            parent_frame = display_frame

        # Add ingredients
        for i, ingredient in enumerate(selected_ingredients):
            row_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=5, pady=2)

            # Ingredient label
            ctk.CTkLabel(
                row_frame,
                text=f"• {ingredient['name']} - {ingredient['quantity']}",
                font=ctk.CTkFont(family="Verdana", size=12),
                text_color="white",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            # Remove button
            ctk.CTkButton(
                row_frame,
                text="✕",
                width=20,
                height=20,
                fg_color="transparent",
                hover_color="#ff4444",
                command=lambda idx=i: self._remove_ingredient(idx, selected_ingredients, display_frame)
            ).pack(side="right")

    def _remove_ingredient(self, index, selected_ingredients, display_frame):
        """Helper method to remove an ingredient"""
        selected_ingredients.pop(index)
        self._update_ingredients_list(selected_ingredients, display_frame)

    def _confirm_edit_item(self, window, category, index, name_var, price_var, selected_ingredients, old_name, category_name):
        """Helper method to confirm item editing"""
        new_name = name_var.get().strip()

        try:
            new_price = float(price_var.get().replace(',', '.'))
        except ValueError:
            self._show_error("Preço inválido!")
            return

        if not new_name:
            self._show_error("O nome do item é obrigatório!")
            return

        if not selected_ingredients:
            self._show_error("Pelo menos um ingrediente é obrigatório!")
            return

        # Prepare ingredients strings
        try:
            ingredients_str = "--".join([item['name'].strip() for item in selected_ingredients])
            quantities_str = "--".join([str(item['quantity']).strip() for item in selected_ingredients])
            
            # Debug print (pode remover depois)
            print(f"Enviando para o banco de dados:")
            print(f"Nome: {new_name}, Preço: {new_price}")
            print(f"Ingredientes: {ingredients_str}")
            print(f"Quantidades: {quantities_str}")
            print(f"Categoria: {category_name}")
            print(f"Old Name: {old_name}")

            # Update local data - corrigido para manter a estrutura de tupla
            self.categories[category][index] = (new_name, new_price, "round_logo.png", [item['name'] for item in selected_ingredients])

            # Update database
            success = cardapio.edit(old_name, new_name, new_price, ingredients_str, quantities_str, category_name)
            
            if not success:
                self._show_error("Erro ao atualizar no banco de dados!")
                return

            # Refresh menu and close window
            self.refresh_menu()
            window.destroy()

        except Exception as e:
            print(f"Erro ao preparar dados para edição: {e}")
            self._show_error(f"Erro ao editar item: {str(e)}")

    def _show_error(self, message):
        """Helper method to show error messages"""
        error_window = ctk.CTkToplevel()
        error_window.title("Erro")
        error_window.geometry("300x100")
        error_window.resizable(False, False)
        
        ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(family="Verdana", size=12),
            text_color="red"
        ).pack(pady=20)
        
        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        ).pack(pady=5)
        
        error_window.grab_set()

    def show_confirmation_screen(self, order_screen, order_description, quantidade_description, total_price, payment_method):
        """Mostra uma tela simples de confirmação com botão OK"""
        confirmation_screen = ctk.CTkToplevel()
        confirmation_screen.title("Pedido Confirmado")
        confirmation_screen.geometry("350x300")
        confirmation_screen.resizable(False, False)
        confirmation_screen.grab_set()
        confirmation_screen.focus_force()
        
        # Centralizar a janela
        confirmation_screen.update_idletasks()
        screen_width = confirmation_screen.winfo_screenwidth()
        screen_height = confirmation_screen.winfo_screenheight()
        x = (screen_width - 350) // 2
        y = (screen_height - 300) // 2
        confirmation_screen.geometry(f"+{x}+{y}")

        # Main frame
        main_frame = ctk.CTkFrame(confirmation_screen)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Success icon
        success_icon = self.load_image("success_icon.png", (60, 60))
        if success_icon:
            icon_label = ctk.CTkLabel(main_frame, image=success_icon, text="")
            icon_label.pack(pady=(20, 10))

        # Success message
        success_label = ctk.CTkLabel(
            main_frame,
            text="Pedido confirmado!",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        success_label.pack(pady=(0, 15))

        # Summary message
        summary_label = ctk.CTkLabel(
            main_frame,
            text=f"Total: R$ {total_price:.2f}\n{payment_method}",
            font=ctk.CTkFont(size=14)
        )
        summary_label.pack(pady=(0, 20))

        # OK button
        ok_button = ctk.CTkButton(
            main_frame,
            text="OK",
            width=100,
            command=lambda: [
                order_screen.destroy(),
                confirmation_screen.destroy(),
                self.update_inventory_from_order(),
                self.clear_order(order_screen),
                self.refresh_orders_after_save()
            ]
        )
        ok_button.pack(pady=(0, 10))