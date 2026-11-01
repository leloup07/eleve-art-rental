# Eleve Art — web pública

Web pública de [eleve-art.com](https://eleve-art.com): servicio de alquiler de arte moderno y contemporáneo.

**Esta web no contiene imágenes de las obras ni precios.** Las obras se presentan como placas tipográficas y en formato índice.

- Las imágenes, fichas completas y condiciones están en el repositorio privado `eleve-art-coleccion` (colección privada con acceso por email).
- **Prohibido subir a este repositorio** fotografías de obras (ni recortes, montajes o recreaciones) y precios. Única excepción: obras marcadas `image_licensed: true` en el panel de gestión, con licencia de reproducción (VEGAP) acreditada.
- Las placas de las obras son dibujos del marco o vitrina a la proporción real de cada pieza (generados en `index.html` a partir de las medidas). No reproducen la obra.
- **Fotos documentales** (`DOCS` en `index.html`, archivos en `img/documentos/`): solo reverso, sellos, etiquetas de galería, certificados o marco de canto. Nunca el anverso de la obra ni un detalle de ella. Si un certificado incluye una foto de la obra, taparla o recortarla.
- **Fotos de espacios** (`img/espacios/`): solo interiores sin obras de terceros visibles, propias o con licencia que permita uso comercial.
- **Enlaces externos** (`ref_url`, `ref_label`, `ref_note` en cada obra): solo enlazar, nunca incrustar ni descargar la imagen. Solo fuentes autorizadas (museo, fundación del artista, catálogo razonado, editor, casa de subastas). Si es otro ejemplar de la misma edición, indicarlo en `ref_note`.
- El índice de la colección y los datos estructurados están pre-renderizados en el HTML. Tras editar obras desde el panel, usar **Exportar HTML** para regenerarlos.
- Cada obra tiene página propia en `/obra/<id>.html` (para Google). Tras cualquier cambio de obras, regenerarlas con `node _tools/generar-fichas.js`, que también actualiza `sitemap.xml`.
- Tipografías alojadas en `/fonts` (sin Google Fonts).
- Versión inglesa en `/en/`: se genera desde `index.html` con `python3 _tools/generar-en.py` (traducciones de obras en `_tools/i18n/en-collection.json`). Si se añade o cambia una obra o un texto, actualizar ahí la traducción y volver a generar; después, pre-renderizar el índice como en la versión española.
