import pandas as pd
import random

# Define product data options
categorias = ['Anillos', 'Collares', 'Pulseras', 'Pendientes', 'Broches']
materiales = ['Oro', 'Plata', 'Platino', 'Oro Rosa', 'Acero']
estilos = ['Clásico', 'Moderno', 'Vintage', 'Minimalista', 'Bohemio']
ocasiones = ['Diario', 'Fiesta', 'Boda', 'Gala', 'Trabajo']
temporadas = ['Primavera', 'Verano', 'Otoño', 'Invierno', 'Continuo']
nombres_joyas = {
    'Anillos': ['Anillo Solitario', 'Anillo de Compromiso', 'Anillo Eternidad', 'Sello de Oro', 'Anillo Fino'],
    'Collares': ['Collar de Perlas', 'Gargantilla de Diamantes', 'Collar Largo', 'Colgante de Corazón', 'Cadena Fina'],
    'Pulseras': ['Esclava de Plata', 'Pulsera de Charms', 'Brazalete Rígido', 'Pulsera de Tenis', 'Pulsera de Cuero'],
    'Pendientes': ['Pendientes de Aro', 'Perlas Clásicas', 'Pendientes Colgantes', 'Dormilonas de Brillantes', 'Earcuff Moderno'],
    'Broches': ['Broche de Flor', 'Prendedor de Platino', 'Broche Libélula', 'Alfiler de Corbata', 'Broche Vintage']
}

# Generate data for 20 products
productos_data = []
for i in range(1, 21):
    categoria = random.choice(categorias)
    nombre = random.choice(nombres_joyas[categoria])
    material = random.choice(materiales)
    estilo = random.choice(estilos)
    ocasion = random.choice(ocasiones)
    temporada = random.choice(temporadas)
    precio = round(random.uniform(30.0, 1500.0), 2)
    oferta_mes = random.choice([True, False])

    productos_data.append({
        'producto_id': i,
        'nombre': f"{nombre} de {material}",
        'categoria': categoria,
        'material': material,
        'precio': precio,
        'estilo': estilo,
        'ocasion': ocasion,
        'temporada': temporada,
        'oferta_mes': oferta_mes
    })

# Create DataFrame
df_productos = pd.DataFrame(productos_data)

# Save to CSV
df_productos.to_csv('productos.csv', index=False)

print("productos.csv generated successfully.")