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
        
    def validate_cnpj(self, event=None, entry_widget=None):        
        if not entry_widget:
            return
            
        value = entry_widget.get().replace(".", "").replace("/", "").replace("-", "")        
        value = ''.join(filter(str.isdigit, value))        
        
        if len(value) > 14:
            value = value[:14]
        
        # Format with separators
        formatted = ""
        if len(value) > 0:
            formatted = value[:2]
            if len(value) > 2:
                formatted += "." + value[2:5]
                if len(value) > 5:
                    formatted += "." + value[5:8]
                    if len(value) > 8:
                        formatted += "/" + value[8:12]
                        if len(value) > 12:
                            formatted += "-" + value[12:14]
                
        entry_widget.delete(0, "end")
        entry_widget.insert(0, formatted)
        
        return True

    def validate_phone(self, event=None, entry_widget=None):        
        if not entry_widget:
            return
            
        value = entry_widget.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")        
        value = ''.join(filter(str.isdigit, value))        
        
        if len(value) > 11:
            value = value[:11]
        
        # Format with separators
        formatted = ""
        if len(value) > 0:
            formatted = "(" + value[:2]
            if len(value) > 2:
                formatted += ") " + value[2:7]
                if len(value) > 7:
                    formatted += "-" + value[7:11]
                
        entry_widget.delete(0, "end")
        entry_widget.insert(0, formatted)
        
        return True

    def validate_text_length(self, event=None, entry_widget=None, max_length=40):        
        if not entry_widget:
            return
            
        value = entry_widget.get()
        
        if len(value) > max_length:
            entry_widget.delete(max_length, "end")
            
        return True

    def validate_email(self, event=None, entry_widget=None):        
        if not entry_widget:
            return
            
        value = entry_widget.get()
        
        if len(value) > 40:
            value = value[:40]
            entry_widget.delete(0, "end")
            entry_widget.insert(0, value)
            
        return True        
        
    def create_main_content(self, main_menu, root):        
        self.fonts = main_menu.fonts
        self.colors = main_menu.colors
        self.root = root       
        
        # Main content frame
        main_content = ctk.CTkFrame(root, fg_color=self.colors["dark_bg"], width=800)
        main_content.pack(side="right", fill="both", expand=True)

        # Search bar container 
        search_container = ctk.CTkFrame(main_content, fg_color="transparent", height=40)
        search_container.pack(side="top", fill="x", padx=20, pady=(15, 5))
        search_container.pack_propagate(False)

        # Search bar
        search_bar = ctk.CTkEntry(
            search_container,
            placeholder_text="🔎 Pesquisar Fornecedor",
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
            corner_radius=0,
            hover_color=self.colors["primary_hover"],
            command=None
        )
        filter_button.place(relx=0.97, rely=0.5, anchor="center")

        # Table container 
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
                text_color=self.colors["dark_bg"]
            )
            header_label.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
                
        # Configure grid columns 
        for i in range(len(headers)):
            self.table_container.grid_columnconfigure(i, weight=1)
            
        # Supplier button
        btn_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        btn_frame.pack(pady=(0, 5), padx=20, fill="x")
        
        add_row_button = ctk.CTkButton(
            btn_frame,
            text="Cadastrar",
            width=120,
            height=40,
            fg_color=self.colors["secondary"],
            hover_color=self.colors["secondary_hover"],
            text_color=self.colors["text_primary"],
            font=self.fonts["button_font"],
            command=lambda: self.add_supplier_row(root)  
        )
        add_row_button.place(relx=0.425, rely=0.2, anchor="s")
        
        print_supplier_button = ctk.CTkButton(
            btn_frame,
            text="Imprimir",
            width=120,
            height=40,
            fg_color=self.colors["text_primary"],
            hover_color=self.colors["selected"],
            text_color=self.colors["dark_bg"],
            font=self.fonts["button_font"],
            command=lambda: self.add_supplier_row(root)  
        )
        print_supplier_button.place(relx=0.575, rely=0.2, anchor="s")
        
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
            messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {e}")
        
    def add_supplier_row(self, root):        
        add_window = ctk.CTkToplevel()
        add_window.title("Cadastrar Fornecedor")
        add_window.geometry("300x450")
        add_window.resizable(False, False)
        add_window.overrideredirect(True)
        add_window.grab_set()
        add_window.focus_force()
        
        # Main frame 
        main_frame = ctk.CTkFrame(
            add_window,
            fg_color=self.colors["dark_bg"],  
            corner_radius=10
        )
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Title bar frame 
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
            font=self.fonts["menu_font"],
            text_color=self.colors["text_primary"]
        )
        title.pack(pady=(5, 20))        
        
        from MainMenu import WindowDragging
        WindowDragging(add_window, title_bar) 
        
        # Input frame 
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["dark_bg"],  
            corner_radius=5
        )
        input_frame.pack(padx=10, fill="x")
               
        nome_label = ctk.CTkLabel(
            input_frame,
            text="Nome:",
            font=self.fonts["input_font"],
            text_color=self.colors["text_primary"]
        )
        nome_label.pack(padx=5, pady=(5, 0), anchor="w")        
        
        nome_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="",
            font=self.fonts["input_font"],
            height=30,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"]
        )
        nome_entry.pack(padx=10, pady=(0, 5), fill="x")
        nome_entry.bind("<KeyRelease>", lambda event, widget=nome_entry: self.validate_text_length(event, widget, 40))
        
        telefone_label = ctk.CTkLabel(
            input_frame,
            text="CNPJ:",
            font=self.fonts["input_font"],
            text_color=self.colors["text_primary"]
        )
        telefone_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        telefone_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="xx.xxx.xxx/xxxx-xx",
            font=self.fonts["input_font"],
            height=30,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"]
        )
        telefone_entry.pack(padx=10, pady=(0, 5), fill="x")
        telefone_entry.bind("<KeyRelease>", lambda event, widget=telefone_entry: self.validate_cnpj(event, widget))
        
        email_label = ctk.CTkLabel(
            input_frame,
            text="E-Mail:",
            font=self.fonts["input_font"],
            text_color=self.colors["text_primary"]
        )
        email_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        email_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="contato@alimentos.com",
            font=self.fonts["input_font"],
            height=30,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"]
        )
        email_entry.pack(padx=10, pady=(0, 5), fill="x")
        email_entry.bind("<KeyRelease>", lambda event, widget=email_entry: self.validate_email(event, widget))
        
        cnpj_label = ctk.CTkLabel(
            input_frame,
            text="Telefone:",
            font=self.fonts["input_font"],
            text_color=self.colors["text_primary"]
        )
        cnpj_label.pack(padx=5, pady=(5, 0), anchor="w")
        
        cnpj_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="(xx) xxxxx-xxxx",
            font=self.fonts["input_font"],
            height=30,
            fg_color=self.colors["medium_bg"],
            text_color=self.colors["text_primary"],
            border_color=self.colors["border"]
        )
        cnpj_entry.pack(padx=10, pady=(0, 5), fill="x")
        cnpj_entry.bind("<KeyRelease>", lambda event, widget=cnpj_entry: self.validate_phone(event, widget))       
             
                
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
            fg_color=self.colors["error"], 
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
            fg_color=self.colors["secondary"],  
            hover_color=self.colors["secondary_hover"],
            command=save
        )
        save_button.place(relx=0.75, rely=0.95, anchor="center")
        
    def add_row_to_table(self, cdg_supplier, supplier, cnpj, telefone, email):
        try:
            # Find the number of existing rows in the table
            current_rows = len([child for child in self.table_container.grid_slaves() if int(child.grid_info()["row"]) > 0])
            new_row = current_rows + 1  
            
            # Configure grid columns 
            self.table_container.grid_columnconfigure(0, weight=1)  # N°
            self.table_container.grid_columnconfigure(1, weight=2)  # Nome
            self.table_container.grid_columnconfigure(2, weight=2)  # CNPJ
            self.table_container.grid_columnconfigure(3, weight=2)  # Telefone
            self.table_container.grid_columnconfigure(4, weight=2)  # Email
            self.table_container.grid_columnconfigure(5, weight=1)  # Actions
            
            # Add new row to the table
            values = [cdg_supplier, supplier, cnpj, telefone, email]
            for col, value in enumerate(values):
                row_label = ctk.CTkLabel(
                    self.table_container,
                    text=str(value),
                    font=self.fonts["input_font"],
                    fg_color="transparent",
                    text_color=self.colors["dark_bg"]
                )
                row_label.grid(row=new_row, column=col, padx=8, pady=5, sticky="we")
                       
            button_frame = ctk.CTkFrame(
                self.table_container,
                fg_color="transparent",
                width=50,  
                height=35  
            )
            button_frame.grid(row=new_row, column=5, padx=(8, 2), pady=(5), sticky="we")
            button_frame.grid_propagate(False)  
                
            edit_icon = self.load_image("edit_icon.png", size=(25, 25))
            trash_icon = self.load_image("trash.png", size=(24, 24)) 
            
            def delete_row():                
                confirm = ctk.CTkToplevel(self.root)
                confirm.title("Confirmar exclusão")
                confirm.geometry("250x150")
                confirm.resizable(False, False)
                confirm.overrideredirect(True)
                confirm.grab_set()             
                                
                x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (250 // 2)
                y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (150 // 2)
                confirm.geometry(f"250x150+{x}+{y}")
               
                msg = ctk.CTkLabel(
                    confirm,
                    text="Tem certeza que deseja excluir este fornecedor?",
                    font=self.fonts["input_font"],
                    wraplength=250
                )
                msg.pack(pady=20)
               
                btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
                btn_frame.pack(pady=10)

                def confirm_delete():
                    if fornecedor.delete(cdg_supplier):
                        for widget in self.table_container.grid_slaves(row=new_row):
                            widget.destroy()
                        confirm.destroy()
                        self.load_data()
                    else:
                        messagebox.showerror("Erro", "Falha ao excluir o fornecedor do banco de dados.")
                                
                ctk.CTkButton(
                    btn_frame,
                    text="Não",
                    font=self.fonts["button_font"],
                    width=100,
                    fg_color=self.colors["secondary"],
                    hover_color=self.colors["secondary_hover"],
                    command=confirm.destroy
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                    btn_frame,
                    text="Sim",
                    font=self.fonts["button_font"],
                    width=100,
                    fg_color=self.colors["error"],
                    hover_color="#CC0000",
                    command=confirm_delete
                ).pack(side="right", padx=5)
            
            edit_button = ctk.CTkButton(
                button_frame,
                text="",
                image=edit_icon,
                width=35,
                height=35,
                fg_color="transparent",
                hover_color=self.colors["selected"],
                corner_radius=5,               
                command=lambda r=new_row: self.edit_row(r)  
            )
            edit_button.pack(side="left", padx=(0, 2))          
                                
            delete_button = ctk.CTkButton(
                button_frame,
                text="",  
                image=trash_icon,
                width=40,  
                height=35,
                fg_color="transparent", 
                hover_color=self.colors["selected"],  
                command=delete_row
            )
            delete_button.pack(side="left", padx=(2, 0))
                
        except Exception as e:
            print(f"Error adding row to table: {e}")
                
    def edit_row(self, row):        
        current_values = []
        for col in range(5):  
            cell = [
                widget for widget in self.table_container.grid_slaves()
                if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == col
            ]
            if cell:
                current_values.append(cell[0].cget("text"))
        
        if len(current_values) == 5:
            cdg_supplier, supplier, cnpj, telefone, email = current_values
            
            # Edit window 
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar Fornecedor")
            edit_window.geometry("300x500")
            edit_window.resizable(False, False)
            edit_window.overrideredirect(True)
            edit_window.grab_set()
            edit_window.focus_force()

            # Main frame 
            main_frame = ctk.CTkFrame(
                edit_window,
                fg_color=self.colors["dark_bg"],
                corner_radius=10
            )
            main_frame.pack(padx=10, pady=(10, 10), fill="both", expand=True)            
            
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
                font=self.fonts["menu_font"],
                text_color=self.colors["text_primary"]
            )
            title.pack(pady=(5, 15))            
            
            from MainMenu import WindowDragging
            WindowDragging(edit_window, title_bar)

            # Input frame
            input_frame = ctk.CTkFrame(
                main_frame,
                fg_color=self.colors["dark_bg"],
                corner_radius=5
            )
            input_frame.pack(padx=10, fill="x")

            # Nome input
            nome_label = ctk.CTkLabel(
                input_frame, 
                text="Nome:", 
                font=self.fonts["input_font"], 
                text_color=self.colors["text_primary"]
            )
            nome_label.pack(padx=5, pady=(5, 0), anchor="w")
            nome_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["border"]
            )
            nome_entry.insert(0, supplier)
            nome_entry.pack(padx=5, pady=(0, 5), fill="x")
            nome_entry.bind("<KeyRelease>", lambda event, widget=nome_entry: self.validate_text_length(event, widget, 40))

            # CNPJ input
            cnpj_label = ctk.CTkLabel(
                input_frame, 
                text="CNPJ:", 
                font=self.fonts["input_font"], 
                text_color=self.colors["text_primary"]
            )
            cnpj_label.pack(padx=5, pady=(5, 0), anchor="w")
            cnpj_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["border"]
            )
            cnpj_entry.insert(0, cnpj)
            cnpj_entry.pack(padx=5, pady=(0, 5), fill="x")
            cnpj_entry.bind("<KeyRelease>", lambda event, widget=cnpj_entry: self.validate_cnpj(event, widget))

            # Telefone input
            telefone_label = ctk.CTkLabel(
                input_frame, 
                text="Email:", 
                font=self.fonts["input_font"], 
                text_color=self.colors["text_primary"]
            )
            telefone_label.pack(padx=5, pady=(5, 0), anchor="w")
            telefone_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["border"]
            )
            telefone_entry.insert(0, telefone)
            telefone_entry.pack(padx=5, pady=(0, 5), fill="x")
            telefone_entry.bind("<KeyRelease>", lambda event, widget=telefone_entry: self.validate_email(event, widget))

            # Email input
            email_label = ctk.CTkLabel(
                input_frame, 
                text="Telefone:", 
                font=self.fonts["input_font"], 
                text_color=self.colors["text_primary"]
            )
            email_label.pack(padx=5, pady=(5, 0), anchor="w")
            email_entry = ctk.CTkEntry(
                input_frame,
                font=self.fonts["input_font"],
                height=30,
                fg_color=self.colors["medium_bg"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["border"]
            )
            email_entry.insert(0, email)
            email_entry.pack(padx=5, pady=(0, 10), fill="x")
            email_entry.bind("<KeyRelease>", lambda event, widget=email_entry: self.validate_phone(event, widget))

            def save_edit():
                try:
                    new_nome = nome_entry.get().strip()
                    new_cnpj = cnpj_entry.get().strip()
                    new_telefone = telefone_entry.get().strip()
                    new_email = email_entry.get().strip()

                    if fornecedor.update(cdg_supplier, new_nome, new_cnpj, new_telefone, new_email):                        
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
                    print(f"Erro na função save_edit: {e}")                        
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(side="bottom", pady=(5, 15), fill="x", padx=20)         
                                   
            # Cancel button
            cancel_button = ctk.CTkButton(
                buttons_frame,
                text="Cancelar",
                font=self.fonts["button_font"],
                width=80,
                height=35,
                fg_color=self.colors["error"],
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
                fg_color=self.colors["secondary"],
                hover_color=self.colors["secondary_hover"],
                command=save_edit
            )
            save_button.pack(side="right", padx=5)