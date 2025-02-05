import customtkinter as ctk
from PIL import Image
import os

class Cartemenu:
    def __init__(self, root):
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

    def init_fonts(self, root):
        # Initialize fonts
        logo_font = ctk.CTkFont(family="Arial", size=30, weight="bold")
        menu_font = ctk.CTkFont(family="Verdana", size=16, weight="bold")
        input_font = ctk.CTkFont(family="Verdana", size=14)
        button_font = ctk.CTkFont(family="Verdana", size=14, weight="bold")

        # Initialize colors
        main_color = "#FF8C00"  # Orange
        hover_color = "#FFA500"
        dark_bg = "#1E1E1E"  # Darker background for main content
        menu_bg = "white"  # White background for side menu
        link_color = "#87CEEB"

        return {
            "logo_font": logo_font,
            "menu_font": menu_font,
            "input_font": input_font,
            "button_font": button_font
        }, {
            "main_color": main_color,
            "hover_color": hover_color,
            "dark_bg": dark_bg,
            "menu_bg": menu_bg,
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
                hover_color="#FF8C00", 
                text_color="white",
                font=self.fonts["menu_font"],
                corner_radius=10,  # Rounded corners
                command=lambda x=item: self.menu_item_clicked(x)
            )
            menu_button.pack(pady=5)

    def create_main_content(self, root):

        self.root = root
        self.order_items = []  # Lista para armazenar os itens pedidos
        self.order_id = 1  # Contador para IDs dos items
        self.quantity_entries = []  # Lista para armazenar todas as entradas de quantidade  # Contador para IDs dos items

        main_frame = ctk.CTkFrame(root, fg_color=self.colors["dark_bg"])
        main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        canvas = ctk.CTkCanvas(main_frame, bg=self.colors["dark_bg"], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, command=canvas.yview)
        scroll_frame = ctk.CTkFrame(canvas, fg_color=self.colors["dark_bg"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.total_price = 0.0
        self.total_label = None

        categories = {
            "Hambúrguer": [
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"]),
                ("AMERICANO", 13.99, "round_logo.png", ["Hambúrguer", "Tomate", "Queijo", "Alface", "Molho Especial"])
            ],
            "Batatas": [
                ("BATATA P", 8.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA M", 10.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("BATATA G", 13.99, "round_logo.png", ["Batata frita", "Molho Especial"]),
                ("EXTRA G", 17.99, "round_logo.png", ["Batata frita", "Molho Extra"])
            ],
            "Refrigerantes": [
                ("COCA COLA", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("COCA LATA", 4.00, "round_logo.png", ["350ML"]),
                ("GUARANÁ", 5.99, "round_logo.png", ["Refrigerante Gelado"]),
                ("FANTA", 5.99, "round_logo.png", ["Refrigerante Gelado"])
            ]
        }

        def update_total():
            self.total_label.configure(text=f"Sub-Total R$ {self.total_price:.2f}")

        def add_to_order(name, price, quantity_var):
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

                update_total()
                quantity_var.set("0")

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

                price_label = ctk.CTkLabel(card, text=f"R$ {price:.2f}", font=self.fonts["input_font"],
                                           text_color="white")
                price_label.pack()

                ingredients_label = ctk.CTkLabel(card, text="\n".join(ingredients), font=self.fonts["input_font"],
                                                 text_color="white")
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
                    command=lambda n=name, p=price, q=quantity_var: add_to_order(n, p, q)
                )
                add_button.pack(pady=5)



        bottom_frame = ctk.CTkFrame(main_frame, fg_color="#D3D3D3", height=50)
        bottom_frame.place(relx=0, rely=1, anchor="sw", relwidth=1.0)

        self.total_label = ctk.CTkLabel(bottom_frame, text=f"Sub-Total R$ {self.total_price:.2f}",
                                        font=self.fonts["menu_font"], text_color="black")
        self.total_label.pack(side="left", padx=20)

        def open_order_screen():
            order_screen = ctk.CTkToplevel()
            order_screen.title("FlyThru - Comanda")
            order_screen.geometry("500x600")
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
            order_label.pack(side="left", padx=10)

            # Main content frame
            content_frame = ctk.CTkFrame(order_screen, fg_color="#2b2b2b")
            content_frame.pack(fill="both", expand=True)

            # Headers
            headers_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            headers_frame.pack(fill="x", padx=20, pady=10)

            # Column labels with grid
            column_widths = [50, 180, 50, 100]  # Approximate widths for each column
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

            # Items frame with grid
            items_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            items_frame.pack(fill="both", expand=True, padx=20)

            def update_order_total():
                self.total_price = sum(float(item["price"].replace("R$ ", "")) for item in self.order_items)
                if self.total_label:
                    self.total_label.configure(text=f"Sub-Total R$ {self.total_price:.2f}")

            def remove_item(item_frame, item):
                # Remove the frame from UI
                item_frame.destroy()

                # Remove item from the list
                self.order_items.remove(item)

                # Update the total price by subtracting the removed item's price
                item_price = float(item["price"].replace("R$ ", ""))
                self.total_price -= item_price

                # Update totals on both screens
                update_total()

                # Update the total amount label in the order screen
                total_amount.configure(text=f"R$ {self.total_price:.2f}")

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
                    command=lambda f=item_frame, i=item: remove_item(f, i)
                )
                delete_button.grid(row=0, column=4, padx=5)

            # Bottom frame for total and buttons
            bottom_frame = ctk.CTkFrame(order_screen, fg_color="white", height=120)
            bottom_frame.pack(side="bottom", fill="x")

            # Total section
            total_label = ctk.CTkLabel(
                bottom_frame,
                text="Total",
                font=ctk.CTkFont(family="Verdana", size=14, weight="bold"),
                text_color="black"
            )
            total_label.pack(anchor="w", padx=20, pady=(10, 0))

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

            def clear_order():
                self.order_items.clear()
                self.total_price = 0.0
                update_total()
                order_screen.destroy()

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
                command=clear_order
            )
            trash_button.pack(side="right")

        generate_order_button = ctk.CTkButton(bottom_frame, text="Gerar Comanda", fg_color="green",
                                              hover_color="darkgreen", font=self.fonts["button_font"],
                                              text_color="white", command=open_order_screen)
        generate_order_button.pack(side="right", padx=20)

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: bottom_frame.lift() if canvas.yview()[1] == 1.0 else None)

    def menu_item_clicked(self, item):
        self.root.withdraw()
        
        if item == "Estoque 📦":
            storage_window = ctk.CTkToplevel()
            storage_window.title("FlyThru - Estoque")
            storage_window.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            
            # Initialize the Cartemenu in the new window
            from TelaEstoque import StorageMenu
            menu_screen = StorageMenu(storage_window)
        if item == "Cardapio 🍔":
            pass
        else:
            pass          
       
        # When menu window is closed, show login window again
        def on_menu_close():
            storage_window.destroy()
            self.root.deiconify()
            
        storage_window.protocol("WM_DELETE_WINDOW", on_menu_close)

def main():
    root = ctk.CTk()
    root.title("FlyThru - Storage")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    app = Cartemenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()