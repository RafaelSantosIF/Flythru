# dictionary.py
def init_fonts(root):
    import customtkinter as ctk
    
    fonts = {
        "logo_font": ctk.CTkFont(
            family="Impact",
            size=64,
            weight="bold"
        ),
        "welcome_font": ctk.CTkFont(
            family="Verdana",
            size=24
        ),
        "input_font": ctk.CTkFont(
            family="Verdana",
            size=14
        ),
        "input_font_login": ctk.CTkFont(
            family="Verdana",
            size=16
        ),
        "button_font": ctk.CTkFont(
            family="Verdana", 
            size=14, 
            weight="bold"
        ),
        "button_font_login": ctk.CTkFont(
            family="Verdana",
            size=20,
            weight= "bold"
        ),
        "link_font": ctk.CTkFont(
            family="Arial",
            size=12
        ),
        "menu_font": ctk.CTkFont(
            family="Verdana", 
            size=16, 
            weight="bold"
        ),
        "header_font": ctk.CTkFont(
            family="Verdana", 
            size=14, 
            weight="bold"
        )
    }
    
    # Esquema de cores padronizado
    colors = {
        # Cores primárias
        "primary": "#FF8C00",         # Laranja (cor principal)
        "primary_hover": "#E57200",   # Laranja escuro (hover)
        "primary_light": "#FFB347",   # Laranja claro
        
        # Cores secundárias
        "secondary": "#00B894",       # Verde-turquesa
        "secondary_hover": "#00A085", # Verde-turquesa escuro
        "secondary_light": "#55EFC4", # Verde-turquesa claro
        
        # Cores de acento
        "accent": "#0984E3",          # Azul
        "accent_hover": "#0770C5",    # Azul escuro
        "accent_light": "#74B9FF",    # Azul claro
        
        # Cores neutras
        "dark_bg": "#1E1E1E",         # Fundo escuro
        "medium_bg": "#2D2D2D",       # Fundo médio
        "light_bg": "#3D3D3D",        # Fundo claro
        
        # Cores de texto
        "text_primary": "#FFFFFF",    # Texto primário (branco)
        "text_secondary": "#CCCCCC",  # Texto secundário (cinza claro)
        "text_disabled": "#888888",   # Texto desabilitado (cinza médio)
        
        # Cores de status
        "success": "#00CC88",         # Sucesso (verde)
        "warning": "#FFCC00",         # Aviso (amarelo)
        "error": "#FF4444",           # Erro (vermelho)
        "info": "#55AAFF",            # Informação (azul claro)
        
        # Cores para elementos específicos
        "selected": "#555555",        # Cor para itens selecionados
        "border": "#555555",          # Cor para bordas
        "link": "#74B9FF",            # Cor para links
        "table_bg": "white",        # Cor para fundo de tabelas
        "table_header": "#3D3D3D",    # Cor para cabeçalho de tabelas
        "table_row_alt": "#383838",   # Cor alternativa para linhas de tabelas
        
        # Mapeamento das cores antigas para manter compatibilidade
        "main_color": "#FF8C00",      # mantém compatibilidade
        "hover_color": "#E57200",     # atualizado
        "second_color": "#00B894",    # atualizado
        "second_hover_color": "#00A085", # atualizado
        "selected_color": "#555555",  # atualizado
        "link_color_login": "#74B9FF",# atualizado
        "menu_bg": "#2D2D2D",         # atualizado
        "link_color": "#74B9FF",      # atualizado
    }
    
    return fonts, colors