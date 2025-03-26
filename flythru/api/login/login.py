
def verify_login(username, password):
    """
    Verifica as credenciais de login.

    Args:
        username (str): O nome de usuário inserido pelo usuário.
        password (str): A senha inserida pelo usuário.

    Returns:
        bool: True se o login for bem-sucedido, False caso contrário.
    """
    if username == "admin" and password == "admin":
        return True
    else:
        return False