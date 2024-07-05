"""REL Contacto Usuario module"""


class UsuarioContacto:
    """REL Contacto Usuario class"""
    def __init__(self, usuario_id, contacto_id):
        self.usuario_id = usuario_id
        self.contacto_id = contacto_id

    def get_contacto_id(self):
        return self.contacto_id 

    def get_usuario_id(self):
        return self.usuario_id


class UsuarioContactoRepository:
    """Usuario Contacto repository class"""
    def __init__(self):
        self.usuarios_contactos: list[UsuarioContacto] = []

    def add(self, usuario_contacto: UsuarioContacto):
        self.usuarios_contactos.append(usuario_contacto)

    def get_contact_id_for_user(self, usuario_id):
        for usuario_contacto in self.usuarios_contactos:
            if usuario_contacto.usuario_id == usuario_id:
                return usuario_contacto.contacto_id
        return None

    def get_user_id_for_contact(self, contacto_id):
        for usuario_contacto in self.usuarios_contactos:
            if usuario_contacto.contacto_id == contacto_id:
                return usuario_contacto.usuario_id
        return None
    
    def get_all(self) -> list[UsuarioContacto]:
        return self.usuarios_contactos