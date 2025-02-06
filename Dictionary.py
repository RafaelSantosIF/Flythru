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
    
    colors = {
        "main_color": "#FF8C00",
        "text_primary": "white", 
        "hover_color": "#E55515",
        "second_color" : "#00FF1E",
        "second_hover_color": "#0B951B",
        "dark_bg": "#1E1E1E",
        "link_color_login": "#4A90E2",        
        "menu_bg": "white",  
        "link_color": "#87CEEB",
        "table_bg": "white"
    }
    
    return fonts, colors