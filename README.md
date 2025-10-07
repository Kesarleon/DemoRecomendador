# Rosa Oliva: Demo de Recomendador de Joyas Personalizado

Este proyecto es una demostración interactiva de un sistema de recomendación de joyas para la marca **Rosa Oliva**, construido con Streamlit.

## ¿Qué hace este tablero?

El tablero simula una experiencia de cliente personalizada en la que un usuario puede introducir su ID de cliente para recibir recomendaciones de joyas a medida. El objetivo es mostrar cómo Rosa Oliva puede aprovechar los datos para ofrecer una experiencia de compra única y relevante.

### Características Principales

*   **Recomendaciones Personalizadas**: El motor de recomendación analiza el perfil de cada cliente, incluyendo su estilo preferido (`Clásico`, `Moderno`, `Vintage`, etc.) y su material favorito (`Oro`, `Plata`, etc.).
*   **Análisis de Contexto**: Las recomendaciones no solo se basan en el perfil del cliente, sino que también consideran factores contextuales como:
    *   La **temporada actual** (Primavera, Verano, Otoño, Invierno).
    *   **Ofertas especiales** del mes.
*   **Interfaz Interactiva**: Los usuarios pueden introducir un ID de cliente (del 1 al 10 para esta demo) y obtener al instante una nueva serie de recomendaciones.
*   **Explicaciones Transparentes**: Junto a las recomendaciones, la aplicación proporciona una breve explicación de por qué se sugirieron esas piezas específicas, aumentando la confianza del cliente.

## ¿Cómo funciona?

La aplicación utiliza un **modelo de recomendación basado en contenido**. Calcula un "puntaje de afinidad" para cada joya del catálogo en función de:

1.  La similitud entre los atributos del producto (estilo, material) y las preferencias del cliente.
2.  La relevancia del producto para la temporada actual y si está en oferta.
3.  Un ligero factor de aleatoriedad para añadir variedad y descubrimiento.

Este tablero es un prototipo funcional que ilustra el potencial de la personalización para mejorar la interacción con el cliente e impulsar las ventas en Rosa Oliva.