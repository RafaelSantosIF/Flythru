import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import Dictionary as dc
from api.estoque.estoque import Estoque


estoque = Estoque()

class StorageMenu:
    def __init__(self):
        self.table_container = None
        self.produtos = []
        
        
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
        self.load_data()

    def update_table(self):
        # Limpa as linhas existentes (mantém os headers)
        for child in self.table_container.winfo_children():
            child.destroy()

        # Adiciona as novas linhas com os dados carregados
        for product in self.produtos:
            self.add_row_to_table(*product)

    def load_data(self):
        try:
            products = estoque.listar_tudo()
            if products:
                self.produtos = products # Guarda os produtos carregados
                self.update_table() # Chama a função para atualizar a tabela
            else:
                print("Não tem produtos.")
                # Lidar com a tabela vazia (opcional)

        except Exception as e:
            print(f"Error loading data: {e}")
            messagebox.showerror("Error", f"Falha ao carregar produtos: {e}")

    def add_stock_row(self, root):
        # Create a window for adding a stock item
        add_window = ctk.CTkToplevel()
        add_window.title("Cadastrar produto")
        add_window.geometry("300x400")
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
            text="Cadastrar produto",
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

        # ID input
        '''id_label = ctk.CTkLabel(
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
        id_entry.pack(padx=10, pady=(0, 10), fill="x")'''

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
           # id_produto = id_entry.get().strip()
            produto = nome_entry.get().strip()
            quant = quant_entry.get().strip()
            categoria = categoria_var.get()

            
            try:
                estoque.save(produto, quant, categoria)  # Chama a função save do Estoque
                self.load_data() # Recarrega os dados e atualiza a tabela
                add_window.destroy() # Fecha a janela de cadastro após salvar
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
                print(f"Erro ao salvar no banco: {e}")

        # Create buttons directly in the main_frame
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
        cancel_button.place(relx=0.25, rely=0.90, anchor="center")

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
        save_button.place(relx=0.75, rely=0.90, anchor="center")

    def add_row_to_table(self, id_produto, produto, quant, categoria):
        try:
            # Find the number of existing rows in the table
            current_rows = len([child for child in self.table_container.grid_slaves() if int(child.grid_info()["row"]) > 0])
            new_row = current_rows + 1  
            
            # Add new row to the table
            values = [id_produto, produto,quant, categoria]
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
                width=30,
                height=30,
                fg_color=self.colors["main_color"],
                hover_color=self.colors["hover_color"],
                text_color="white",
                font=self.fonts["input_font"],
                command=lambda r=new_row: self.edit_row(r)  # Pass the row number to edit_row method
            )
            edit_button.grid(row=new_row, column=4, padx=2, pady=5, sticky="ns")  
            
            # Configure the new row
            self.table_container.grid_rowconfigure(new_row, pad=3)
            
            print(f"Added new row: {values}")  # Debug print
            
        except Exception as e:
            print(f"Error adding row to table: {e}")

    def edit_row(self, row):
        # Get the current values from the row
        current_values = []
        for col in range(4):  
            cell = [
                widget for widget in self.table_container.grid_slaves()
                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
            ]
            if cell:
                current_values.append(cell[0].cget("text"))
        
        if len(current_values) == 4:
            id_produto, produto, quant, categoria = current_values
            
            # Create edit window 
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar produto")
            edit_window.geometry("300x450")
            edit_window.resizable(False, False)
            edit_window.overrideredirect(True)
            edit_window.grab_set()
            edit_window.focus_force()

            # Create a main frame 
            main_frame = ctk.CTkFrame(
                edit_window,
                fg_color="#FF8C00",
                corner_radius=10
            )
            main_frame.pack(padx=10, pady=(10, 10), fill="both", expand=True)
            
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
                text="Editar produto",
                font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
                text_color="white"
            )
            title.pack(pady=(5, 15))
            
            # Add dragging functionality
            from MainMenu import WindowDragging
            WindowDragging(edit_window, title_bar)

            # Input frame
            input_frame = ctk.CTkFrame(
                main_frame,
                fg_color="#1E1E1E",
                corner_radius=5
            )
            input_frame.pack(padx=10, fill="x")

            '''# ID input (disabled since it's the identifier)
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
            id_entry.pack(padx=5, pady=(0, 5), fill="x")'''

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
                
                   # id_entry.get(),
                produto = nome_entry.get(),
                quant = quant_entry.get(),
                categoria = categoria_var.get()
                try:
                    # Converte quantidade para o tipo correto (int ou float)
                    try:
                        quant = int(quant_entry.get())
                    except ValueError:
                        quant = float(quant_entry.get())

                    if estoque.update(id_produto, nome_entry.get(), quant, categoria_var.get()):
                        # Atualiza a linha na tabela (como você já faz)
                        new_values = [id_produto, nome_entry.get(), quant, categoria_var.get()] #inclui o id_produto
                        for col, value in enumerate(new_values):
                            cell = [
                                widget for widget in self.table_container.grid_slaves()
                                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
                            ]
                            if cell:
                                cell[0].configure(text=str(value))

                        edit_window.destroy()
                        self.load_data()
                        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao atualizar o produto no banco de dados.")

                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida. Deve ser um número.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
                    print(f"Erro na função save_edit: {e}") # Para debug



            def delete_row():
                # Create confirmation dialog
                confirm = ctk.CTkToplevel(edit_window)
                confirm.title("Confirmar exclusão")
                confirm.geometry("250x150")
                confirm.resizable(False, False)
                confirm.overrideredirect(True)
                confirm.grab_set()
                
                # Center the confirmation window relative to the edit window
                x = edit_window.winfo_x() + (edit_window.winfo_width() // 2) - (300 // 2)
                y = edit_window.winfo_y() + (edit_window.winfo_height() // 2) - (150 // 2)
                confirm.geometry(f"250x150+{x}+{y}")

                # Confirmation message
                msg = ctk.CTkLabel(
                    confirm,
                    text="Tem certeza que deseja excluir este item?",
                    font=self.fonts["input_font"],
                    wraplength=250
                )
                msg.pack(pady=20)

                # Buttons frame
                btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
                btn_frame.pack(pady=10)

                def confirm_delete():
                    # Remove all widgets in the row
                    if estoque.delete(id_produto):
                        for widget in self.table_container.grid_slaves(row=row):
                            widget.destroy()
                        confirm.destroy()
                        edit_window.destroy()
                        self.load_data()
                    else:
                        messagebox.showerror("Erro", "Falha ao excluir o produto do banco de dados.")

                # Confirmation buttons
                ctk.CTkButton(
                    btn_frame,
                    text="Não",
                    font=self.fonts["button_font"],
                    width=100,
                    fg_color=self.colors["second_color"],
                    hover_color=self.colors["second_hover_color"],
                    command=confirm.destroy
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                    btn_frame,
                    text="Sim",
                    font=self.fonts["button_font"],
                    width=100,
                    fg_color="#FF0000",
                    hover_color="#CC0000",
                    command=confirm_delete
                ).pack(side="left", padx=5)
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(side="bottom", pady=(5, 15), fill="x", padx=20)

            trash_icon = self.load_image("trash.png", size=(24, 24))
            
            # Delete button 
            delete_button = ctk.CTkButton(
                buttons_frame,
                text="",  
                image=trash_icon,
                width=40,  
                height=35,
                fg_color="transparent", 
                hover_color=None,
                command=delete_row
            )
            delete_button.pack(side="left", padx=5)
            
            # Cancel button
            cancel_button = ctk.CTkButton(
                buttons_frame,
                text="Cancelar",
                font=self.fonts["button_font"],
                width=80,
                height=35,
                fg_color="#FF0000",
                hover_color="#CC0000",
                command=edit_window.destroy
            )
            cancel_button.pack(side="left", padx=5)            

            # Save button
            save_button = ctk.CTkButton(
                buttons_frame,
                text="Salvar",
                font=self.fonts["button_font"],
                width=80,
                height=35,
                fg_color=self.colors["second_color"],
                hover_color=self.colors["second_hover_color"],
                command=save_edit
            )
            save_button.pack(side="right", padx=5)   


