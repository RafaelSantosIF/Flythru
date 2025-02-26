import customtkinter as ctk
from PIL import Image
import os
import Dictionary as dc


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

        # Display order items
        for item in self.order_items:
            item_frame = ctk.CTkFrame(items_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=5)

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
            height=35
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

    def add_new_item(self, category):
        """Open a dialog to add a new item to the specified category"""
        # Create a new window for adding an item with the same style as the order screen
        add_window = ctk.CTkToplevel()
        add_window.title(f"Adicionar Item - {category}")
        add_window.geometry("500x500")
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
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Name field
        name_label = ctk.CTkLabel(
            form_frame,
            text="Nome do Item:",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        name_label.pack(fill="x", pady=(10, 5))

        name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            form_frame,
            textvariable=name_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35
        )
        name_entry.pack(fill="x", pady=(0, 15))

        # Price field
        price_label = ctk.CTkLabel(
            form_frame,
            text="Preço (R$):",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        price_label.pack(fill="x", pady=(10, 5))

        price_var = ctk.StringVar()
        price_entry = ctk.CTkEntry(
            form_frame,
            textvariable=price_var,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=35,
            placeholder_text="0.00"
        )
        price_entry.pack(fill="x", pady=(0, 15))

        # Ingredients field
        ingredients_label = ctk.CTkLabel(
            form_frame,
            text="Ingredientes (um por linha):",
            font=ctk.CTkFont(family="Verdana", size=14),
            anchor="w"
        )
        ingredients_label.pack(fill="x", pady=(10, 5))

        ingredients_text = ctk.CTkTextbox(
            form_frame,
            font=ctk.CTkFont(family="Verdana", size=12),
            height=150
        )
        ingredients_text.pack(fill="x", pady=(0, 15))

        # Bottom frame
        bottom_frame = ctk.CTkFrame(add_window, fg_color="white", height=80)
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

            ingredients_content = ingredients_text.get("1.0", "end-1c")
            ingredients_list = [ing.strip() for ing in ingredients_content.split('\n') if ing.strip()]

            if not name or not ingredients_list:
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
            height=35,
            command=confirm_add_item
        )
        add_button.pack(side="left", expand=True, padx=20, pady=10)

        # Cancel button
        cancel_button = ctk.CTkButton(
            bottom_frame,
            text="Cancelar",
            fg_color="#ff4444",
            hover_color="#ff0000",
            font=ctk.CTkFont(family="Verdana", size=12, weight="bold"),
            height=35,
            command=add_window.destroy
        )
        cancel_button.pack(side="right", padx=20, pady=10)

    def refresh_menu(self):
        """Refresh the menu content to reflect changes"""
        if hasattr(self, 'main_content'):
            # First, remove the entire main_content from the root
            self.main_content.pack_forget()

            # Destroy the old main_content frame completely
            self.main_content.destroy()

            # Recreate the menu by calling create_main_content
            self.create_main_content(self.main_menu, self.root)

    def create_card(self, parent, name, price, img, ingredients, idx):
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

        # Aumentar o padding vertical para o botão ADD
        add_button = ctk.CTkButton(
            card,
            text="+ ADD",
            fg_color=self.colors["main_color"],
            hover_color=self.colors["hover_color"],
            font=self.fonts["button_font"],
            command=lambda n=name, p=price, q=quantity_var: self.add_to_order(n, p, q),
            height=25
        )
        add_button.pack(pady=(5, 10), padx=10, fill="x")  # Aumentar o padding inferior

        return card

    def create_horizontal_section(self, parent, category, items):
        """Create a horizontal scrollable section for a category"""
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

        # Create scrollable frame for horizontal scrolling
        # Ajustar a altura do scrollable frame para acomodar o card mais alto
        scroll_container = ctk.CTkScrollableFrame(
            section_frame,
            fg_color=self.colors["dark_bg"],
            orientation="horizontal",
            height=360,  # Increased from 340 to 360
            width=800
        )
        scroll_container.pack(fill="x", pady=5)

        # Create a frame to hold the cards
        cards_frame = ctk.CTkFrame(scroll_container, fg_color=self.colors["dark_bg"])
        cards_frame.pack(fill="both", expand=True, pady=5, padx=5)

        # Create item cards in a horizontal layout
        for idx, (name, price, img, ingredients) in enumerate(items):
            card = self.create_card(cards_frame, name, price, img, ingredients, idx)
            card.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")

            # Set fixed width for each column to ensure consistent card sizing
            cards_frame.grid_columnconfigure(idx, minsize=180)  # Increased from 140 to 180

        # Add the plus card at the end
            # Update the plus card height
            plus_card = ctk.CTkFrame(
                cards_frame,
                border_width=2,
                border_color="#2E2E2E",
                fg_color="transparent",
                corner_radius=10,
                width=180,
                height=320  # Increased from 300 to 320
            )
        plus_card.grid(row=0, column=len(items), padx=10, pady=5, sticky="nsew")
        cards_frame.grid_columnconfigure(len(items), minsize=180)  # Consistent sizing

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

        # Create each category section
        for category, items in self.categories.items():
            self.create_horizontal_section(container_frame, category, items)

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