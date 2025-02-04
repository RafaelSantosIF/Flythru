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
            family="Arial",
            size=24
        ),
        "input_font": ctk.CTkFont(
            family="Arial",
            size=16
        ),
        "button_font": ctk.CTkFont(
            family="Arial",
            size=20,
            weight= "bold"
        ),
        "link_font": ctk.CTkFont(
            family="Arial",
            size=12
        )
    }
    
    colors = {
        "main_color": "#FF5F1F",
        "text_primary": "white", 
        "hover_color": "#E55515",
        "dark_bg": "#1E1E1E",
        "link_color": "#4A90E2"
    }
    
    return fonts, colors