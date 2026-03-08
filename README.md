# Eleve Art Rental

Colección privada de arte moderno y contemporáneo con obras disponibles para alquiler para hoteles, empresas, interioristas y proyectos culturales.

## Estructura

```
├── index.html          ← Web principal (single-page)
├── collection.json     ← Base de datos de obras (con campos rental)
├── README.md
└── [imágenes .jpg]     ← Fotos de las obras
```

## Gestión de obras

Editar `collection.json` para añadir, modificar o eliminar obras. Campos rental:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `rental_available` | boolean | Obra disponible para alquiler |
| `rental_price_month_from` | number | Precio mensual orientativo (€) |
| `rental_price_event_from` | number | Precio evento orientativo (€) |
| `rental_priority` | string | `high` / `medium` / `low` |
| `rental_usage` | array | Usos: `hotel`, `office`, `interiorismo`, `corporate`, `evento` |
| `featured_rental` | boolean | Aparece en sección Destacadas |
| `highlight_home` | boolean | Aparece en portada |

## Deploy

Hosting estático (GitHub Pages, Netlify, Cloudflare Pages).

```bash
git add .
git commit -m "Actualizar colección"
git push
```
