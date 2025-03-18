import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc
from api.pedido.pedido import Pedido
from api.cardapio.item_cardapio import Item_Cardapio

pedido = Pedido()
cardapio = Item_Cardapio()

class CarteMenu:
    def __init__(self):
        self.table_container = None
        self.total_price = 0.0
        self.total_label = None
        self.order_items = []
        self.order_id = 1
        self.categories = {
            "Hambúrguer": [
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"])
            ],
            "Batatas": [
                ("BATATA P", 8.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA M", 10.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA M", 10.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA M", 10.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA G", 13.99, "round_logo.png", ["Batata frita", "Molho Especial"])
            ],
            "Refrigerantes": [
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA LATA", 4.00, "round_logo.png", ["350ML"]),
                ("GUARANÁ", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"])
            ]
        }

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
                "qty": f"x{quantity}",
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
        # Access the OrdersMenu instance from MainMenu if available
        if hasattr(self.main_menu, 'orders_menu') and self.main_menu.orders_menu:
            if hasattr(self.main_menu.orders_menu, 'refresh_orders_table'):
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

        # Display order items
        for item in self.order_items:
            item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=5)
            order_description += f'{item['item']} {item['qty']}\n'

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

        # Buttons frame
        buttons_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)

        # Finish order button
        finish_button = ctk.CTkButton(
            buttons_frame,
            text="Finalizar Pedido",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=35,
            command=lambda: [
                pedido.save(order_description, self.total_price, "cartão de Crédito"),
                self.clear_order(order_screen), 
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
        available_ingredients = [
            {"name": "Hambúrguer", "unit": "g", "default_qty": 180},
            {"name": "Queijo", "unit": "g", "default_qty": 30},
            {"name": "Alface", "unit": "g", "default_qty": 20},
            {"name": "Tomate", "unit": "g", "default_qty": 50},
            {"name": "Cebola", "unit": "g", "default_qty": 30},
            {"name": "Picles", "unit": "g", "default_qty": 20},
            {"name": "Bacon", "unit": "g", "default_qty": 40},
            {"name": "Molho Especial", "unit": "ml", "default_qty": 25},
            {"name": "Pão", "unit": "un", "default_qty": 1},
            {"name": "Batata Frita", "unit": "g", "default_qty": 150},
            {"name": "Refrigerante", "unit": "ml", "default_qty": 350},
        ]

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

            # Criar lista de nomes de ingredientes para salvar no formato original
            ingredients_list = [item["name"] for item in selected_ingredients]

            # Add new item to the category
            self.categories[category].append((name, price, "round_logo.png", ingredients_list))

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
        # Increase card height from 300 to 320px
        card = ctk.CTkFrame(parent, fg_color="#2E2E2E", corner_radius=10, width=180, height=320)
        card.grid_propagate(False)  # Prevent the card from resizing based on content

        image = self.load_image(img, (80, 80))
        if image:
            img_label = ctk.CTkLabel(card, image=image, text="")
            img_label.pack(pady=(10, 5))

        name_label = ctk.CTkLabel(card, text=name, font=self.fonts["menu_font"], text_color="white")
        name_label.pack(pady=(5, 0))

        price_label = ctk.CTkLabel(card, text=f"R$ {price:.2f}", font=self.fonts["input_font"], text_color="white")
        price_label.pack(pady=(0, 5))

        # Increase the ingredients frame height from 90 to 120px
        ingredients_frame = ctk.CTkFrame(card, fg_color="transparent", height=120)
        ingredients_frame.pack(pady=(0, 5), fill="x", padx=5)
        ingredients_frame.pack_propagate(False)  # Keep height fixed

        # Increase max visible ingredients if needed
        max_ingredients = 6  # Changed from 5 to 6
        display_ingredients = ingredients[:max_ingredients]

        for ing in display_ingredients:
            ing_label = ctk.CTkLabel(
                ingredients_frame,
                text="• " + ing,
                font=ctk.CTkFont(family="Verdana", size=10),
                text_color="white",
                anchor="w",
                wraplength=150
            )
            ing_label.pack(fill="x", pady=0)

        quantity_frame = ctk.CTkFrame(card, fg_color="transparent")
        quantity_frame.pack(fill="x", padx=10, pady=(5, 0))

        quantity_var = ctk.StringVar(value="0")
        quantity_entry = ctk.CTkEntry(
            quantity_frame,
            textvariable=quantity_var,
            width=50,
            height=25,
            fg_color="#3E3E3E",
            border_color="#555555"
        )
        quantity_entry.pack(side="left")

        # Botões + e - para quantidade
        minus_btn = ctk.CTkButton(
            quantity_frame,
            text="-",
            width=25,
            height=25,
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            command=lambda: quantity_var.set(str(max(0, int(quantity_var.get()) - 1)))
        )
        minus_btn.pack(side="left", padx=(5, 0))

        plus_btn = ctk.CTkButton(
            quantity_frame,
            text="+",
            width=25,
            height=25,
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            command=lambda: quantity_var.set(str(int(quantity_var.get()) + 1))
        )
        plus_btn.pack(side="left", padx=(5, 0))

        # Botões frame
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(5, 10))

        # Botão ADD
        add_button = ctk.CTkButton(
            buttons_frame,
            text="+ ADD",
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            font=self.fonts["button_font"],
            command=lambda n=name, p=price, q=quantity_var: self.add_to_order(n, p, q),
            height=25,
            width=100
        )
        add_button.pack(side="left", fill="x", expand=True)

        # Botão DELETE
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑",
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=self.fonts["button_font"],
            command=lambda cat=category, i=idx: self.delete_menu_item(cat, i),
            height=25,
            width=30
        )
        delete_button.pack(side="right", padx=(5, 0))

        return card

    def create_category_section(self, parent, category, items):
        """Create a section for a category with grid layout"""
        # Section frame
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