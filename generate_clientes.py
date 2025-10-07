import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker('es_ES')

# Define options for simulated data
estilos = ['Clásico', 'Moderno', 'Vintage', 'Minimalista', 'Bohemio']
materiales = ['Oro', 'Plata', 'Platino', 'Oro Rosa', 'Acero']
frecuencias = ['Semanal', 'Mensual', 'Bimestral', 'Ocasional']

# Generate data for 10 clients
clientes_data = []
for i in range(1, 11):
    nombre = fake.first_name()
    edad = random.randint(20, 65)
    estilo_preferido = random.choice(estilos)
    material_favorito = random.choice(materiales)
    frecuencia_compra = random.choice(frecuencias)
    fecha_ultima_compra = (datetime.now() - timedelta(days=random.randint(5, 365))).strftime('%Y-%m-%d')
    valor_promedio_compra = round(random.uniform(50.0, 500.0), 2)

    clientes_data.append({
        'cliente_id': i,
        'nombre': nombre,
        'edad': edad,
        'estilo_preferido': estilo_preferido,
        'material_favorito': material_favorito,
        'frecuencia_compra': frecuencia_compra,
        'fecha_ultima_compra': fecha_ultima_compra,
        'valor_promedio_compra': valor_promedio_compra
    })

# Create DataFrame
df_clientes = pd.DataFrame(clientes_data)

# Save to CSV
df_clientes.to_csv('clientes.csv', index=False)

print("clientes.csv generated successfully.")