"""REL class"""
class UsuarioContacto:
    def __init__(self, usuario_id, contacto_id):
        self.usuario_id = usuario_id
        self.contacto_id =contacto_id
        
    def get_contact_id_for_user(self, usuario_id):
        return self.contacto_id if self.usuario_id == usuario_id else None
    
    def get_user_id_for_contact(self, contacto_id):
        return self.usuario_id if self.contacto_id == contacto_id else None