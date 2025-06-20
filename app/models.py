from flask_sqlalchemy import SQLAlchemy #ORM
from datetime import datetime #Para manejar fechas y horas

db = SQLAlchemy() #Instancia principal de SQLAlchemy para manejar la base de datos
#La cual se importa en __init__.py para inicializar la base de datos con la aplicación Flask



class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # Relaciones para obtener datos fácilmente
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria_id': self.categoria_id,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria.to_dict() if self.categoria else None
        }