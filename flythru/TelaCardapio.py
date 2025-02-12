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
      
    def create_main_content(self, main_menu, root):
        self.fonts = main_menu.fonts
        self.colors = main_menu.colors
        self.root = root

        # Main content frame
        main_content = ctk.CTkFrame(root, fg_color=self.colors["dark_bg"], width=800)
        main_content.pack(side="right", fill="both", expand=True)

        # Create a container frame for the canvas to manage padding
        container_frame = ctk.CTkFrame(main_content, fg_color=self.colors["dark_bg"])
        container_frame.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 1))
        canvas = ctk.CTkCanvas(container_frame, bg=self.colors["dark_bg"], highlightthickness=0)        
        scroll_frame = ctk.CTkFrame(canvas, fg_color=self.colors["dark_bg"])
        
        # Configure scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind mouse wheel to canvas
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Configure scroll frame
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window in canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        
        # Configure canvas to fill the space
        canvas.pack(side="left", fill="both", expand=True)

        categories = {
            "Hambúrguer": [
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
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
                ("BATATA G", 13.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA G", 13.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA G", 13.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("EXTRA G", 17.99, "round_logo.png", ["Batata frita", "Molho Extra"])
            ],
            "Refrigerantes": [
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA LATA", 4.00, "round_logo.png", ["350ML"]),
                ("GUARANÁ", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("FANTA", 5.99, "round_logo.png", ["Refrigerante Gelado"])
            ]
        }

        for category, items in categories.items():
            category_label = ctk.CTkLabel(scroll_frame, text=category, font=self.fonts["menu_font"], text_color="white")
            category_label.pack(anchor="w", pady=5)

            row_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)

            for idx, (name, price, img, ingredients) in enumerate(items):
                card = ctk.CTkFrame(row_frame, fg_color="#2E2E2E", corner_radius=10)
                card.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")

                image = self.load_image(img, (100, 100))
                if image:
                    img_label = ctk.CTkLabel(card, image=image, text="")
                    img_label.pack(pady=5)

                name_label = ctk.CTkLabel(card, text=name, font=self.fonts["menu_font"], text_color="white")
                name_label.pack()

                price_label = ctk.CTkLabel(card, text=f"R$ {price:.2f}", font=self.fonts["input_font"], text_color="white")
                price_label.pack()

                ingredients_label = ctk.CTkLabel(card, text="\n".join(ingredients), font=self.fonts["input_font"], text_color="white")
                ingredients_label.pack(pady=5)

                quantity_var = ctk.StringVar(value="0")
                quantity_entry = ctk.CTkEntry(card, textvariable=quantity_var, width=50)
                quantity_entry.pack(pady=5)

                add_button = ctk.CTkButton(
                    card,
                    text="+ ADD",
                    fg_color=self.colors["main_color"],
                    hover_color=self.colors["hover_color"],
                    font=self.fonts["button_font"],
                    command=lambda n=name, p=price, q=quantity_var: self.add_to_order(n, p, q)
                )
                add_button.pack(pady=5)

         # Bottom frame
        bottom_frame = ctk.CTkFrame(main_content, fg_color="#D3D3D3", height=50, corner_radius=0 )
        bottom_frame.pack(side="bottom", fill="x")
        bottom_frame.lift()  
        
        self.total_label = ctk.CTkLabel(bottom_frame, text=f"Sub-Total R$ {self.total_price:.2f}",
                                      font=self.fonts["menu_font"], text_color="black")
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

        # Update canvas configuration to handle window resizing
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Modify the MouseWheel binding to ensure bottom frame stays visible
        def on_scroll(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            bottom_frame.lift()
            
        canvas.bind_all("<MouseWheel>", on_scroll)
