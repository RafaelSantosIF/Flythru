import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import Dictionary as dc
from api.fornecedor.fornecedor import Fornecedor

fornecedor = Fornecedor()

class SupplierMenu:
    def __init__(self):
        self.table_container = None
        self.fornecedores = []
        
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

        # Updated search bar
        search_bar = ctk.CTkEntry(
            search_container,
            placeholder_text="🔎 Pesquisar Produto",
            font=self.fonts["input_font"],
            height=40,
            fg_color="white",
            text_color="black",
            placeholder_text_color="gray"
        )
        search_bar.place(relx=0, rely=0, relwidth=1, relheight=1)

        filter_button = ctk.CTkButton(
            search_container,
            image=self.filter_icon,
            text="",
            width=28,
            height=28,
            fg_color="white",
            corner_radius=0,
            hover_color=self.colors["hover_color"],
            command=None
        )
        filter_button.place(relx=0.97, rely=0.5, anchor="center")

        # Table container with white background
        self.table_container = ctk.CTkFrame(main_content, fg_color=self.colors["table_bg"]) 
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Table headers
        headers = ["Código", "Nome", "CNPJ", "Email", "Telefone", " "]
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
        self.load_data()
        
    def update_table(self):
        for child in self.table_container.winfo_children():
            if child.grid_info()["row"] > 0:
                child.destroy()

        for fornecedor in self.fornecedores:
            self.add_row_to_table(*fornecedor)
            
    def load_data(self):
        try:
            fornece = fornecedor.listar_tudo()
            if fornece:
                self.fornecedores = fornece
                self.update_table()
            else:
                print("Não há fornecedores cadastrados.")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {e}")
        
    def add_supplier_row(self, root):        
        add_window = ctk.CTkToplevel()
        add_window.title("Cadastrar Fornecedor")
        add_window.geometry("300x450")
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
        
        telefone_label = ctk.CTkLabel(
            input_frame,
            text="CNPJ:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        telefone_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        telefone_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="xx.xxx.xxx/xxxx-xx",
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
        
        cnpj_label = ctk.CTkLabel(
            input_frame,
            text="Telefone:",
            font=self.fonts["input_font"],
            text_color="white"
        )
        cnpj_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        cnpj_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="(xx) xxxxx-xxxx",
            font=self.fonts["input_font"],
            height=30,
            fg_color="black",
            text_color="white",
            border_color="gray"
        )
        cnpj_entry.pack(padx=10, pady=(0, 5), fill="x")       
             
                
        def cancel():
            add_window.destroy()

        def save():
            nome = nome_entry.get().strip()
            telefone = telefone_entry.get().strip()
            email = email_entry.get().strip()
            cnpj = cnpj_entry.get().strip()

            try:
                fornecedor.save(nome, telefone, email, cnpj)
                self.load_data()
                add_window.destroy()
            except Exception as e:
                print(f"Erro ao salvar no banco: {e}")
            
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
            
            # Configure grid columns - Add this to maintain consistent column widths
            self.table_container.grid_columnconfigure(0, weight=1)  # N°
            self.table_container.grid_columnconfigure(1, weight=2)  # Nome
            self.table_container.grid_columnconfigure(2, weight=2)  # CNPJ
            self.table_container.grid_columnconfigure(3, weight=2)  # Telefone
            self.table_container.grid_columnconfigure(4, weight=2)  # Email
            self.table_container.grid_columnconfigure(5, weight=1)  # Actions column
            
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
                row_label.grid(row=new_row, column=col, padx=8, pady=5, sticky="we")
            
            # Create a frame to hold both buttons 
            button_frame = ctk.CTkFrame(
                self.table_container,
                fg_color="transparent",
                width=50,  
                height=35  
            )
            button_frame.grid(row=new_row, column=5, padx=(8, 2), pady=(5), sticky="we")
            button_frame.grid_propagate(False)  # Prevent frame from resizing
                
            edit_icon = self.load_image("edit_icon.png", size=(25, 25))
            printer = self.load_image("printer.png", size=(25, 25))
            
            edit_button = ctk.CTkButton(
                button_frame,
                text="",
                image=edit_icon,
                width=35,
                height=35,
                fg_color="transparent",
                hover_color="#E5E5E5",
                corner_radius=5,               
                command=lambda r=new_row: self.edit_row(r)  
            )
            edit_button.pack(side="left", padx=(0, 2))
            
            print_button = ctk.CTkButton(
                button_frame,
                text="",
                image=printer,
                width=35,
                height=35,
                fg_color="transparent",
                hover_color="#E5E5E5",
                corner_radius=5,               
                command=None  
            )
            print_button.pack(side="left", padx=(2, 0))
                
        except Exception as e:
            print(f"Error adding row to table: {e}")
            
    def edit_row(self, row):
        # Get the current values from the row
        current_values = []
        for col in range(5):  # We have 5 columns of data (code, name, CNPJ, phone, email)
            cell = [
                widget for widget in self.table_container.grid_slaves()
                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
            ]
            if cell:
                current_values.append(cell[0].cget("text"))
        
        if len(current_values) == 5:
            cdg_supplier, supplier, cnpj, telefone, email = current_values
            
            # Create edit window 
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar Fornecedor")
            edit_window.geometry("300x500")
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
                text="Editar Fornecedor",
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
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            nome_entry.insert(0, supplier)
            nome_entry.pack(padx=5, pady=(0, 5), fill="x")

            # CNPJ input
            cnpj_label = ctk.CTkLabel(
                input_frame, 
                text="CNPJ:", 
                font=self.fonts["input_font"], 
                text_color="white"
            )
            cnpj_label.pack(padx=5, pady=(5, 0), anchor="w")
            cnpj_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            cnpj_entry.insert(0, cnpj)
            cnpj_entry.pack(padx=5, pady=(0, 5), fill="x")

            # Telefone input
            telefone_label = ctk.CTkLabel(
                input_frame, 
                text="Email:", 
                font=self.fonts["input_font"], 
                text_color="white"
            )
            telefone_label.pack(padx=5, pady=(5, 0), anchor="w")
            telefone_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            telefone_entry.insert(0, telefone)
            telefone_entry.pack(padx=5, pady=(0, 5), fill="x")

            # Email input
            email_label = ctk.CTkLabel(
                input_frame, 
                text="Telefone:", 
                font=self.fonts["input_font"], 
                text_color="white"
            )
            email_label.pack(padx=5, pady=(5, 0), anchor="w")
            email_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color="black",
                text_color="white",
                border_color="gray"
            )
            email_entry.insert(0, email)
            email_entry.pack(padx=5, pady=(0, 10), fill="x")

            def save_edit():
                try:
                    new_nome = nome_entry.get().strip()
                    new_cnpj = cnpj_entry.get().strip()
                    new_telefone = telefone_entry.get().strip()
                    new_email = email_entry.get().strip()

                    if fornecedor.update(cdg_supplier, new_nome, new_cnpj, new_telefone, new_email):
                        # Update the row in the table
                        new_values = [cdg_supplier, new_nome, new_cnpj, new_telefone, new_email]
                        for col, value in enumerate(new_values):
                            cell = [
                                widget for widget in self.table_container.grid_slaves()
                                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
                            ]
                            if cell:
                                cell[0].configure(text=str(value))

                        edit_window.destroy()
                        self.load_data()
                        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Falha ao atualizar o fornecedor no banco de dados.")

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar fornecedor: {e}")
                    print(f"Erro na função save_edit: {e}")  # Para debug

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
                    text="Tem certeza que deseja excluir este fornecedor?",
                    font=self.fonts["input_font"],
                    wraplength=250
                )
                msg.pack(pady=20)

                # Buttons frame
                btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
                btn_frame.pack(pady=10)

                def confirm_delete():
                    if fornecedor.delete(cdg_supplier):
                        for widget in self.table_container.grid_slaves(row=row):
                            widget.destroy()
                        confirm.destroy()
                        edit_window.destroy()
                        self.load_data()
                    else:
                        messagebox.showerror("Erro", "Falha ao excluir o fornecedor do banco de dados.")

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