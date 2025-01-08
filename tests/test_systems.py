from app import db

# Limpiar la sesión de SQLAlchemy
db.session.remove()
db.session.flush()
db.session.commit()
print("Sesión limpiada y cambios comprometidos")
