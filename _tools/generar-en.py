# Genera la versión inglesa (/en/index.html) a partir de index.html.
# Uso: python3 _tools/generar-en.py   (después, pre-renderizar con el navegador; ver README)
# Las traducciones de las obras están en _tools/i18n/en-collection.json.
import json, re, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
s = src
missing = []

def raw(es, en, required=True):
    """Sustitución literal en todo el documento (para frases largas e inequívocas)."""
    global s
    if es in s:
        s = s.replace(es, en)
    elif required:
        missing.append(es[:70])

def ui(es, en, required=True):
    """Sustitución solo como texto de elemento o valor de atributo (para palabras cortas)."""
    global s
    n0 = s
    s = s.replace('>' + es + '<', '>' + en + '<')
    for attr in ('placeholder', 'alt', 'aria-label', 'title', 'value'):
        s = s.replace(f'{attr}="{es}"', f'{attr}="{en}"')
    if s == n0 and required:
        missing.append(es[:70])

# ---------- cabecera ----------
raw('<html lang="es">', '<html lang="en">')
raw('<title>Eleve Art · Alquiler de arte original moderno y contemporáneo | Barcelona · Madrid</title>',
    '<title>Eleve Art · Original modern and contemporary art rental | Barcelona · Madrid</title>')
raw('content="Alquiler de obra original de Picasso, Miró, Tàpies, Barceló, Warhol, Plensa y más de 30 artistas para hoteles, oficinas, despachos e interiorismo. Colección privada documentada. Barcelona, Madrid y toda España."',
    'content="Rent original works by Picasso, Miró, Tàpies, Barceló, Warhol, Plensa and 30 more artists for hotels, offices, professional firms and interior design projects. A documented private collection. Barcelona, Madrid and across Spain."')
raw('<link rel="canonical" href="https://eleve.art/">', '<link rel="canonical" href="https://eleve.art/en/">')
raw('<meta property="og:url" content="https://eleve.art/">', '<meta property="og:url" content="https://eleve.art/en/">')
raw('<meta property="og:locale" content="es_ES">', '<meta property="og:locale" content="en_GB">')
s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Eleve Art | Original modern and contemporary art rental">', s)
s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="A private collection of more than 90 original works available to rent for hotels, offices, interior designers and cultural projects. Barcelona · Madrid · Spain.">', s)
s = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="Eleve Art | Original modern and contemporary art rental">', s)
s = re.sub(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="A private collection of more than 90 original works available to rent for hotels, offices, interior designers and cultural projects.">', s)
s = re.sub(r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="art rental, art rental Spain, art rental Barcelona, art for hotels, art for offices, art leasing, interior design art, Picasso, Tàpies, Miró, Barceló, Plensa">', s)

# rutas relativas (la página vive en /en/)
for a, b in [('href="img/', 'href="../img/'), ('src="img/', 'src="../img/'), ('url(img/', 'url(../img/'),
             ('href="fonts/', 'href="../fonts/'), ('href="obra/', 'href="../obra/'), ("'obra/' + item.id", "'../obra/' + item.id"),
             ('href="privacidad.html"', 'href="../privacidad.html"'), ('href="terminos-legales.html"', 'href="../terminos-legales.html"'),
             ('href="en-la-ciudad.html"', 'href="../en-la-ciudad.html"')]:
    s = s.replace(a, b)

# ---------- navegación y portada ----------
for es, en in [('Ethos', 'Ethos'), ('Colección', 'Collection'), ('Espacios', 'Spaces'), ('Modalidades', 'Plans'), ('Proceso', 'Process'),
               ('Preguntas', 'FAQ'), ('Solicitar dossier', 'Request the dossier')]:
    s = s.replace(f'">{es}</a>\n', f'">{en}</a>\n', 1) if f'">{es}</a>\n' in s else s
raw('<span>ES</span> · <a href="en/" hreflang="en" lang="en">EN</a>', '<a href="../" hreflang="es" lang="es">ES</a> · <span>EN</span>')
raw('Alquiler de arte <em>original</em>, moderno y contemporáneo', 'Original <em>art</em> to rent, modern and contemporary')
raw('Una colección privada de más de 90 obras —pintura, dibujo, escultura y obra gráfica— disponible para hoteles, oficinas, despachos e interiorismo. Barcelona · Madrid · toda España.',
    'A private collection of more than 90 works —painting, drawing, sculpture and original prints— available for hotels, offices, professional firms and interior design. Barcelona · Madrid · across Spain.')
ui('Solicitar el dossier', 'Request the dossier')
ui('Por qué existimos', 'Why we exist')
raw('<span class="hero-artists-label">En la colección</span>', '<span class="hero-artists-label">In the collection</span>')
raw('aria-label="Artistas de la colección"', 'aria-label="Artists in the collection"')
raw('aria-label="Principal"', 'aria-label="Main"')
raw('Imagen ilustrativa · Foto:', 'Illustrative image · Photo:')
s = s.replace('filtro de color aplicado; la versión modificada se ofrece bajo la misma licencia', 'colour filter applied; the modified version is offered under the same licence')
s = s.replace('filtro de color aplicado', 'colour filter applied')
for es, en in [('Obras originales', 'Original works'), ('Artistas reconocidos', 'Renowned artists'), ('Un siglo de arte', 'A century of art'), ('Cobertura nacional', 'Nationwide service')]:
    raw(f'>{es}</div>', f'>{en}</div>')

# ---------- ETHOS ----------
T = [
('const USAGE_LABELS = {"hotel":"Hotel boutique","oficina":"Oficina / Despacho","interiorismo":"Interiorismo residencial","evento":"Evento / Rodaje"};',
 'const USAGE_LABELS = {"hotel":"Boutique hotel","oficina":"Office / Professional firm","interiorismo":"Residential interiors","evento":"Event / Shoot"};'),
('<option>Interiorismo residencial</option>', '<option>Residential interiors</option>'),
('>Contactar por esta obra →<', '>Email us about this work →<'),
('El arte no está hecho para esperar en un <em>almacén</em>', 'Art was not made to wait in a <em>storeroom</em>'),
('Manifiesto Eleve Art', 'The Eleve Art manifesto'),
('data-open="Leer el manifiesto completo" data-close="Cerrar el manifiesto"><span>Leer el manifiesto completo</span>', 'data-open="Read the full manifesto" data-close="Close the manifesto"><span>Read the full manifesto</span>'),
('Pasillo de un archivo con estanterías llenas de cajas', 'Archive corridor with shelves full of boxes'),
('Gran parte del arte original del siglo XX vive hoy a oscuras: en cajas, guardamuebles y reservas, a la espera de un momento que casi nunca llega. Mientras tanto, los lugares donde pasamos la vida —hoteles, oficinas, despachos, casas— se llenan de reproducciones y de decoración intercambiable. Eleve Art nace para unir esas dos realidades.',
 'Much of the original art of the twentieth century now lives in the dark: in boxes, storage units and museum stores, waiting for a moment that almost never comes. Meanwhile, the places where we spend our lives —hotels, offices, studios, homes— fill up with reproductions and interchangeable decoration. Eleve Art was created to bring those two realities together.'),
('aria-label="Principios"', 'aria-label="Principles"'),
('Lo original importa', 'The original matters'),
('Circular en lugar de acumular', 'Circulate, don’t accumulate'),
('El arte, donde está la gente', 'Art where people are'),
('Por qué no mostramos imágenes', 'Why we don’t show images'),
('Curaduría, no decoración', 'Curation, not decoration'),
('Una obra original no es una imagen: es un objeto. Tiene materia, escala, peso y la huella de una mano. En un aguafuerte, la presión de la plancha deja un relieve en el papel; en un óleo, la luz se queda atrapada en el empaste; en un dibujo de Derain todavía se adivina la duda del lápiz. Esa diferencia se percibe aunque no se sepa explicar, y cambia la manera en que se habita un espacio, cómo se conversa en él y cómo se recuerda.',
 'An original work is not an image: it is an object. It has material, scale, weight and the trace of a hand. In an etching, the pressure of the plate leaves a relief in the paper; in an oil painting, light is caught in the impasto; in a Derain drawing you can still sense the hesitation of the pencil. That difference is felt even when it cannot be explained, and it changes how a space is lived in, how people talk in it and how it is remembered.'),
('Por eso trabajamos solo con obra original: pinturas, dibujos, esculturas, cerámicas y obra gráfica de edición limitada, con procedencia documentada.',
 'That is why we work only with original works: paintings, drawings, sculptures, ceramics and limited-edition prints, with documented provenance.'),
('Durante siglos, coleccionar ha sido sinónimo de poseer y guardar. Proponemos otra ética: que las obras circulen, que trabajen, que sean vistas. Una pieza colgada en un lobby recibe en una semana más miradas que en diez años dentro de una caja.',
 'For centuries, collecting has meant owning and storing. We propose a different ethic: that works circulate, that they work, that they are seen. A piece hanging in a lobby receives more glances in a week than in ten years inside a crate.'),
('El alquiler permite a hoteles, empresas y estudios de interiorismo convivir con obras de primer nivel sin inmovilizar capital, adaptar la selección a cada proyecto y a cada etapa, y apostar por algo más duradero que la decoración de temporada. Reutilizar lo que ya existe es, también, una forma de responsabilidad.',
 'Renting allows hotels, companies and interior design studios to live with first-rate works without tying up capital, to adapt the selection to each project and each stage, and to invest in something more lasting than seasonal decoration. Reusing what already exists is also a form of responsibility.'),
('Para muchas personas, el primer encuentro con un Tàpies, un Miró o un Warhol no ocurre en un museo, sino en la recepción de una empresa, en la sala de espera de una notaría o en el pasillo de un hotel. Llevar arte a los espacios cotidianos es una forma discreta de mediación cultural: abre preguntas, provoca conversaciones y devuelve a las obras su función primera, que es ser miradas.',
 'For many people, their first encounter with a Tàpies, a Miró or a Warhol does not happen in a museum, but in a company reception, a notary’s waiting room or a hotel corridor. Bringing art into everyday spaces is a quiet form of cultural mediation: it raises questions, starts conversations and gives works back their first purpose, which is to be looked at.'),
('Los derechos de reproducción de una obra pertenecen a sus autores y herederos, no a quien posee el original. Por respeto a ellos, esta web no reproduce las obras sin licencia. Solo publicamos fotografías de una obra cuando está permitido: si la obra es de dominio público, si contamos con licencia de la entidad de gestión de derechos (VEGAP) o con autorización expresa del artista o de sus herederos. Cuando otro ejemplar de la misma edición está publicado de forma autorizada —por un museo, una fundación o una casa de subastas—, enlazamos a esa página en lugar de copiar la imagen.',
 'The reproduction rights of a work belong to its authors and their heirs, not to whoever owns the original. Out of respect for them, this website does not reproduce works without a licence. We only publish photographs of a work when it is allowed: if the work is in the public domain, if we hold a licence from the collecting society (VEGAP) or express permission from the artist or their heirs. When another copy of the same edition has been published with authorisation —by a museum, a foundation or an auction house— we link to that page instead of copying the image.'),
('Lo que encontrarás aquí son textos, fichas, medidas y documentación; las fotografías se comparten en un dossier privado, en el marco de un proyecto concreto.',
 'What you will find here are texts, records, dimensions and documentation; photographs are shared in a private dossier, in the context of a specific project.'),
('Hay también una convicción detrás: una pantalla no sustituye la experiencia de estar frente a una obra. Esta web es un índice y una invitación. El encuentro de verdad ocurre cuando la obra cuelga en tu pared: en el hotel, la oficina o la casa donde va a vivir.',
 'There is also a conviction behind it: a screen cannot replace the experience of standing in front of a work. This website is an index and an invitation. The real encounter happens when the work hangs on your wall: in the hotel, office or home where it is going to live.'),
('No elegimos obras para que combinen con el sofá. Cada propuesta empieza por el lugar: su arquitectura, su luz, su uso y las personas que lo habitan. Buscamos diálogo entre obras, contexto y relato, de forma que cada pieza tenga sentido en el espacio y el espacio gane sentido con ella.',
 'We don’t choose works to match the sofa. Every proposal starts with the place: its architecture, its light, its use and the people who inhabit it. We look for dialogue between works, context and story, so that each piece makes sense in the space and the space gains meaning with it.'),
('Una obra colgada es una obra viva. Una obra guardada es solo inventario.', 'A work on the wall is a living work. A work in storage is just inventory.'),
('<b>Obra original</b><span>Piezas únicas y ediciones limitadas, nunca reproducciones.</span>', '<b>Original work</b><span>Unique pieces and limited editions, never reproductions.</span>'),
('<b>Procedencia</b><span>Certificados, sellos de taller, catálogos razonados y archivos de artista.</span>', '<b>Provenance</b><span>Certificates, studio stamps, catalogues raisonnés and artist archives.</span>'),
('<b>Derechos de autor</b><span>Sin reproducciones públicas no autorizadas. Imágenes solo en dossier privado.</span>', '<b>Copyright</b><span>No unauthorised public reproductions. Images only in a private dossier.</span>'),
('<b>Servicio integral</b><span>Propuesta curada, transporte e instalación profesionales en toda España.</span>', '<b>Full service</b><span>Curated proposal, professional transport and installation across Spain.</span>'),
# ---------- colección ----------
('<div class="section-label">Índice</div>', '<div class="section-label">Index</div>'),
('id="coleccion-title">La colección</h2>', 'id="coleccion-title">The collection</h2>'),
('Más de 90 obras en tres secciones. Busca por artista, título o técnica, o filtra por estilo, y abre cada ficha para leer su historia, sus medidas y su documentación. Cada obra cuenta con su documentación: certificados, sellos de taller, catálogos razonados o archivos de artista.',
 'More than 90 works in three sections. Search by artist, title or technique, or filter by style, and open each record to read its story, dimensions and documentation. Every work comes with its documentation: certificates, studio stamps, catalogues raisonnés or artist archives.'),
('Sin fotografías por respeto a los derechos de reproducción de los artistas: solo las publicamos con licencia (VEGAP), autorización expresa o si la obra es de dominio público. Cuando existe, cada ficha enlaza a otro ejemplar publicado por un museo o una casa de subastas.',
 'No photographs, out of respect for the artists’ reproduction rights: we only publish them with a licence (VEGAP), express permission or when the work is in the public domain. Where available, each record links to another copy published by a museum or an auction house.'),
('aria-label="Buscar en la colección"', 'aria-label="Search the collection"'),
('placeholder="Artista, obra o técnica…"', 'placeholder="Artist, work or technique…"'),
# ---------- en la ciudad ----------
('<div class="section-label">Los artistas en la ciudad</div>', '<div class="section-label">The artists in the city</div>'),
('Miró en la Rambla, Tàpies en el Passeig de Picasso, Plensa en Zaragoza: dónde ver en la calle a los artistas de la colección.',
 'Miró on the Rambla, Tàpies on Passeig de Picasso, Plensa in Zaragoza: where to see the collection’s artists in the street (page in Spanish).'),
('>Ver la ruta →<', '>See the route →<'),
# ---------- espacios ----------
('<div class="section-label">Para cada espacio</div>', '<div class="section-label">For every space</div>'),
('<h2 class="section-title">Espacios</h2>', '<h2 class="section-title">Spaces</h2>'),
('El mismo cuadro no dice lo mismo en un lobby que en una sala de juntas. Así trabajamos en cada tipo de proyecto.',
 'The same painting doesn’t say the same thing in a lobby as in a boardroom. This is how we work on each type of project.'),
('El arte define la personalidad de un hotel antes incluso que la recepción. Proponemos obras para lobby, zonas nobles, restaurante y habitaciones, con un relato coherente con el proyecto y plazos adaptados a cada temporada.',
 'Art defines a hotel’s personality even before the front desk does. We propose works for the lobby, public areas, restaurant and rooms, with a narrative consistent with the project and terms adapted to each season.'),
('Lobby · Habitaciones · Restauración', 'Lobby · Rooms · Restaurant'),
('Despachos y notarías', 'Law firms and notaries'),
('Bufetes, notarías, consultoras y family offices: obra gráfica y pintura de autores consagrados que transmiten solidez y criterio. Tàpies, Plensa, Valdés o la abstracción catalana para salas de juntas, recepciones y despachos de dirección.',
 'Law firms, notaries, consultancies and family offices: prints and paintings by established artists that convey solidity and judgement. Tàpies, Plensa, Valdés or Catalan abstraction for boardrooms, receptions and executive offices.'),
('Recepción · Sala de juntas · Dirección', 'Reception · Boardroom · Executive'),
('Interiorismo residencial', 'Residential interiors'),
('Para estudios de interiorismo, home staging y viviendas de alto nivel: piezas originales que completan un proyecto sin obligar a comprar. Ideal para presentar una vivienda, una promoción o amueblar una segunda residencia.',
 'For interior design studios, home staging and high-end homes: original pieces that complete a project without having to buy. Ideal for presenting a property or a development, or furnishing a second home.'),
('Interioristas · Home staging · Promotoras', 'Interior designers · Home staging · Developers'),
('Oficinas y coworking', 'Offices and coworking'),
('Sedes corporativas y espacios de trabajo creativos: pop, figuración y arte contemporáneo que generan conversación, refuerzan la cultura de empresa y dan carácter a espacios abiertos.',
 'Corporate headquarters and creative workspaces: pop, figuration and contemporary art that spark conversation, strengthen company culture and give character to open spaces.'),
('Sedes · Agencias · Coworking', 'Headquarters · Agencies · Coworking'),
('Eventos y rodajes', 'Events and shoots'),
('Alquiler temporal para eventos, ferias, presentaciones, sesiones fotográficas y producciones audiovisuales, con transporte e instalación coordinados. Los rodajes y sesiones en los que aparezcan las obras están siempre sujetos a que el cliente obtenga los permisos de los titulares de derechos.',
 'Short-term rental for events, fairs, launches, photo shoots and audiovisual productions, with coordinated transport and installation. Shoots and sessions in which the works appear are always subject to the client obtaining permission from the rights holders.'),
('Eventos · Ferias · Producciones', 'Events · Fairs · Productions'),
('alt="Lobby de hotel con sofás y lámpara de araña"', 'alt="Hotel lobby with sofas and chandelier"'),
('alt="Sala de reuniones con mesa y sillas"', 'alt="Meeting room with table and chairs"'),
('alt="Salón luminoso con sofá y suelo de madera"', 'alt="Bright living room with sofa and wooden floor"'),
('alt="Espacio de coworking en un antiguo banco"', 'alt="Coworking space in a former bank"'),
('alt="Montaje de una sala de exposición"', 'alt="Installing an exhibition room"'),
# ---------- modalidades ----------
('<div class="section-label">Modalidades</div>', '<div class="section-label">Plans</div>'),
('Tres niveles, una misma exigencia', 'Three levels, one standard'),
('Elige el nivel que encaja con tu proyecto y tu presupuesto. En todos, obra original y documentada, seleccionada para tu espacio. Las condiciones económicas se detallan en la propuesta personalizada.',
 'Choose the level that fits your project and budget. In all of them: original, documented works selected for your space. Terms and fees are set out in a tailored proposal.'),
('>Nivel I<', '>Level I<'), ('>Nivel II<', '>Level II<'), ('>Nivel III<', '>Level III<'),
('<div class="pack-title">Esencial</div>', '<div class="pack-title">Essential</div>'),
('<div class="pack-title">Colección</div>', '<div class="pack-title">Collection</div>'),
('<div class="pack-title">Maestros</div>', '<div class="pack-title">Masters</div>'),
('Obra original de autores reconocidos para dar carácter a un espacio desde el primer día.', 'Original works by recognised artists to give a space character from day one.'),
('3 a 5 piezas de series del mismo formato', '3 to 5 pieces from same-format series'),
('Rotación hasta 4 veces al año', 'Rotation up to 4 times a year'),
('Duración mínima: 6 meses', 'Minimum term: 6 months'),
('Transporte, instalación y cambios incluidos', 'Transport, installation and changes included'),
('<span>Artistas</span>', '<span>Artists</span>'),
('<span>Ideal para</span>', '<span>Ideal for</span>'),
('Recepciones, pasillos, habitaciones, coworkings, home staging', 'Receptions, corridors, rooms, coworking spaces, home staging'),
('Firmas de primer nivel internacional para espacios que quieren ser recordados.', 'Internationally renowned names for spaces that want to be remembered.'),
('2 a 4 piezas de firma', '2 to 4 signature pieces'),
('Rotación 2 veces al año', 'Rotation twice a year'),
('Duración mínima: 12 meses', 'Minimum term: 12 months'),
('Lobbies, salas de juntas, despachos de dirección, restaurantes', 'Lobbies, boardrooms, executive offices, restaurants'),
('Piezas únicas de los grandes nombres del siglo XX, con procedencia documentada.', 'Unique pieces by the great names of the twentieth century, with documented provenance.'),
('1 a 3 obras únicas o de edición muy limitada', '1 to 3 unique works or very limited editions'),
('Sin rotación: la obra se queda contigo', 'No rotation: the work stays with you'),
('Transporte, instalación e informe de estado de la obra', 'Transport, installation and a condition report'),
('Zonas nobles, presidencia, suites, proyectos singulares', 'Prestige areas, chairman’s office, suites, special projects'),
("onclick=\"scrollToContact('Nivel Esencial')\">Solicitar propuesta Esencial", "onclick=\"scrollToContact('Level Essential')\">Request an Essential proposal"),
("onclick=\"scrollToContact('Nivel Colección')\">Solicitar propuesta Colección", "onclick=\"scrollToContact('Level Collection')\">Request a Collection proposal"),
("onclick=\"scrollToContact('Nivel Maestros')\">Solicitar propuesta Maestros", "onclick=\"scrollToContact('Level Masters')\">Request a Masters proposal"),
('Joan-Josep Tharrats · Manolo Valdés (obra gráfica)', 'Joan-Josep Tharrats · Manolo Valdés (prints)'),
('Antoni Tàpies (obra gráfica) · Andy Warhol', 'Antoni Tàpies (prints) · Andy Warhol'),
('Antoni Tàpies (obra única)', 'Antoni Tàpies (unique works)'),
('<div class="section-label">Suscripción con rotación</div>', '<div class="section-label">Subscription with rotation</div>'),
('Un espacio que cambia sin hacer obras', 'A space that changes without building work'),
('En los niveles Esencial y Colección, las obras se renuevan periódicamente: tus clientes, empleados o huéspedes descubren piezas nuevas cada temporada, y el espacio se mantiene vivo.',
 'At the Essential and Collection levels, the works are renewed periodically: your clients, staff or guests discover new pieces every season, and the space stays alive.'),
('Trabajamos con series del mismo formato —como las estampas de Manolo Valdés o las composiciones de Joan-Josep Tharrats—, de modo que cada cambio se hace sobre los mismos anclajes, sin nuevos agujeros ni molestias.',
 'We work with series in the same format —such as Manolo Valdés’s prints or Joan-Josep Tharrats’s compositions— so each change uses the same fixings, with no new holes and no disruption.'),
('La frecuencia de rotación respeta la conservación de las obras: cuanto más valiosa y delicada es una pieza, menos se manipula. Por eso el nivel Maestros no rota.',
 'Rotation frequency respects the conservation of the works: the more valuable and delicate a piece, the less it is handled. That is why the Masters level does not rotate.'),
('¿Necesitas otra cosa? También alquilamos obras sueltas, por plazos más cortos o para eventos, y preparamos selecciones a medida.',
 'Need something else? We also rent individual works, for shorter terms or for events, and prepare bespoke selections.'),
# ---------- proceso ----------
('<div class="section-label">Proceso</div>', '<div class="section-label">Process</div>'),
('<h2 class="section-title">Cómo Funciona</h2>', '<h2 class="section-title">How it works</h2>'),
('<div class="step-title">Selecciona</div>', '<div class="step-title">Select</div>'),
('Elige una o varias obras del catálogo o solicita una propuesta a medida. ¿No sabes por dónde empezar? Cuéntanos el espacio y te hacemos una selección curada sin compromiso.',
 'Choose one or more works from the catalogue or ask for a bespoke proposal. Not sure where to start? Tell us about the space and we’ll put together a curated selection, with no obligation.'),
('<div class="step-title">Consulta</div>', '<div class="step-title">Enquire</div>'),
('Solicita disponibilidad y condiciones a través del formulario o por email.', 'Ask about availability and terms through the form or by email.'),
('<div class="step-title">Propuesta</div>', '<div class="step-title">Proposal</div>'),
('Recibe propuesta detallada con precios, plazos y condiciones de alquiler.', 'Receive a detailed proposal with prices, terms and rental conditions.'),
('<div class="step-title">Entrega</div>', '<div class="step-title">Delivery</div>'),
('Coordinamos transporte, instalación profesional y duración del alquiler.', 'We coordinate transport, professional installation and the rental period.'),
('<b>Embalaje y transporte</b>', '<b>Packing and transport</b>'),
('<b>Manipulación profesional</b>', '<b>Professional handling</b>'),
('<b>Instalación en tu espacio</b>', '<b>Installation in your space</b>'),
('alt="Desembalaje de una obra enmarcada"', 'alt="Unpacking a framed work"'),
('alt="Manipulación de una pintura enmarcada en una sala"', 'alt="Handling a framed painting in a gallery"'),
('alt="Equipo colgando un cuadro en la pared"', 'alt="Team hanging a painting on the wall"'),
('También disponible para alquiler temporal, rodajes y proyectos especiales. Los rodajes están siempre sujetos a la obtención de los permisos de los titulares de derechos.',
 'Also available for short-term rental, shoots and special projects. Shoots are always subject to obtaining permission from the rights holders.'),
# ---------- interioristas ----------
('<div class="section-label">Profesionales</div>', '<div class="section-label">Professionals</div>'),
('<h2 class="section-title">Interioristas</h2>', '<h2 class="section-title">Interior designers</h2>'),
('Trabajamos con estudios de interiorismo y arquitectura que buscan incorporar arte original de artistas reconocidos en sus proyectos.',
 'We work with interior design and architecture studios looking to bring original art by recognised artists into their projects.'),
('Selección curada', 'Curated selection'),
('Acceso a una colección con obras de Picasso, Tàpies, Barceló, Plensa, Miró y otros maestros.', 'Access to a collection with works by Picasso, Tàpies, Barceló, Plensa, Miró and other masters.'),
('Servicio flexible', 'Flexible service'),
('Alquiler mensual, temporal o para proyectos específicos. Adaptamos plazos y condiciones.', 'Monthly, short-term or project-based rental. We adapt terms and conditions.'),
('Apoyo en proyecto', 'Project support'),
('Asesoramiento curatorial para integrar las obras en el concepto del espacio.', 'Curatorial advice to integrate the works into the concept of the space.'),
('Elaboramos selecciones a medida según las necesidades del proyecto y el espacio.', 'We prepare bespoke selections according to the needs of the project and the space.'),
('>Presentar proyecto<', '>Present a project<'),
# ---------- FAQ (HTML y JSON-LD) ----------
('<div class="section-label">Preguntas frecuentes</div>', '<div class="section-label">Frequently asked questions</div>'),
('Alquilar arte, paso a paso', 'Renting art, step by step'),
('¿Qué es el alquiler de arte?', 'What is art rental?'),
('Es un servicio que permite disponer de obras de arte originales durante un periodo determinado —desde un evento puntual hasta más de un año— sin necesidad de comprarlas. Eleve Art selecciona las obras con criterio curatorial, coordina el transporte y la instalación y prepara una propuesta a medida para cada espacio.',
 'It is a service that lets you have original works of art for a set period —from a one-off event to more than a year— without having to buy them. Eleve Art selects the works with curatorial judgement, coordinates transport and installation, and prepares a bespoke proposal for each space.'),
('¿Para quién es el servicio?', 'Who is the service for?'),
('Para hoteles y proyectos de hospitality, despachos profesionales y notarías, oficinas y coworkings, estudios de interiorismo y arquitectura, promotoras inmobiliarias (home staging), eventos, rodajes y proyectos culturales.',
 'For hotels and hospitality projects, professional firms and notaries, offices and coworking spaces, interior design and architecture studios, property developers (home staging), events, shoots and cultural projects.'),
('¿Durante cuánto tiempo puedo alquilar una obra?', 'How long can I rent a work for?'),
('Trabajamos con alquileres de 1 a 3 meses, de 3 a 6 meses, de 6 a 12 meses y de más de un año, además de alquileres para eventos puntuales y rodajes (estos, siempre sujetos a la obtención de los permisos de los titulares de derechos). El plazo y las condiciones se concretan en la propuesta personalizada.',
 'We offer rentals of 1 to 3 months, 3 to 6 months, 6 to 12 months and more than a year, as well as rentals for one-off events and shoots (the latter always subject to obtaining permission from the rights holders). The term and conditions are set out in the tailored proposal.'),
('¿Las obras son originales?', 'Are the works originals?'),
('Sí. La colección reúne pinturas, dibujos, esculturas y cerámicas originales, y obra gráfica original de edición limitada (aguafuertes, litografías, serigrafías), con certificados, sellos de taller o referencias de catálogo razonado. No alquilamos reproducciones.',
 'Yes. The collection brings together original paintings, drawings, sculptures and ceramics, and limited-edition original prints (etchings, lithographs, screenprints), with certificates, studio stamps or catalogue raisonné references. We do not rent reproductions.'),
('¿Por qué la web no muestra fotografías de las obras?', 'Why doesn’t the website show photographs of the works?'),
('Porque los derechos de reproducción pertenecen a los artistas y a sus herederos, no al propietario de la obra. Solo publicamos fotografías de una obra cuando está permitido: si la obra es de dominio público, si contamos con licencia de la entidad de gestión de derechos (VEGAP) o con autorización expresa del artista o de sus herederos. En los demás casos, las fotografías se facilitan en un dossier privado a quienes tienen un proyecto concreto y, cuando existe, enlazamos a otro ejemplar publicado de forma autorizada por un museo o una casa de subastas.',
 'Because reproduction rights belong to the artists and their heirs, not to the owner of the work. We only publish photographs of a work when it is allowed: if the work is in the public domain, if we hold a licence from the collecting society (VEGAP) or express permission from the artist or their heirs. Otherwise, photographs are provided in a private dossier to those with a specific project and, where available, we link to another copy published with authorisation by a museum or an auction house.'),
('¿Cuánto cuesta alquilar una obra de arte?', 'How much does it cost to rent a work of art?'),
('Depende de la obra, del número de piezas, de la duración y de la logística del proyecto. Enviamos las condiciones en una propuesta personalizada; respondemos en menos de 24 horas.',
 'It depends on the work, the number of pieces, the term and the logistics of the project. We send the conditions in a tailored proposal; we reply within 24 hours.'),
('¿En qué ciudades trabajáis?', 'Which cities do you work in?'),
('Tenemos base en Barcelona y Madrid y trabajamos en toda España, con transporte e instalación profesionales coordinados por nuestro equipo.',
 'We are based in Barcelona and Madrid and work across Spain, with professional transport and installation coordinated by our team.'),
('¿Puedo fotografiar o filmar las obras alquiladas?', 'Can I photograph or film the rented works?'),
('El alquiler no incluye derechos de imagen sobre las obras: Eleve Art es propietaria de los originales, pero los derechos de reproducción pertenecen a los artistas y a sus herederos. Cualquier fotografía con fines comerciales, publicación en web o redes sociales, rodaje o uso publicitario requiere la autorización previa de los titulares de los derechos (en España, normalmente a través de VEGAP), que tramita el cliente. Te ayudamos a identificar a quién dirigirte.',
 'The rental does not include image rights over the works: Eleve Art owns the originals, but reproduction rights belong to the artists and their heirs. Any photograph for commercial purposes, publication on a website or social media, filming or advertising use requires prior permission from the rights holders (in Spain, usually through VEGAP), which the client must obtain. We help you identify whom to contact.'),
('¿Puedo comprar una obra después de alquilarla?', 'Can I buy a work after renting it?'),
('En algunas obras existe opción de compra tras el periodo de alquiler. Indícanos tu interés en la solicitud y te informaremos de las piezas disponibles.',
 'Some works can be purchased after the rental period. Let us know in your request and we will tell you which pieces are available.'),
# ---------- contacto ----------
('<div class="section-label">Contacto</div>', '<div class="section-label">Contact</div>'),
('Solicita el dossier y una propuesta', 'Request the dossier and a proposal'),
('Déjanos tu nombre y tu email y te enviaremos el acceso a la colección privada, con fotografías, fichas y condiciones. Si nos cuentas tu proyecto, te respondemos en menos de 24 horas con una selección adaptada a tu espacio.',
 'Leave us your name and email and we will send you access to the private collection, with photographs, records and conditions. If you tell us about your project, we will reply within 24 hours with a selection tailored to your space.'),
('alt="Pasillo de piedra que conduce a una puerta iluminada"', 'alt="Stone corridor leading to a lit doorway"'),
('>Nombre *<', '>Name *<'), ('>Email *<', '>Email *<'), ('>Empresa / Estudio<', '>Company / Studio<'), ('>Teléfono<', '>Phone<'),
('>Tipo de proyecto<', '>Project type<'), ('>Duración estimada<', '>Estimated term<'), ('>Obras o nivel de interés<', '>Works or level of interest<'), ('>Mensaje<', '>Message<'),
('placeholder="Nombre completo"', 'placeholder="Full name"'), ('placeholder="nombre@empresa.com"', 'placeholder="name@company.com"'),
('placeholder="Opcional"', 'placeholder="Optional"'),
('placeholder="Opcional: una obra, un artista o un nivel (Esencial, Colección, Maestros)"', 'placeholder="Optional: a work, an artist or a level (Essential, Collection, Masters)"'),
('placeholder="Opcional: cuéntanos el espacio, el estilo o el plazo"', 'placeholder="Optional: tell us about the space, the style or the timing"'),
('<option value="">Seleccionar…</option>', '<option value="">Select…</option>'),
('<option>Oficina / Despacho</option>', '<option>Office / Professional firm</option>'),
('<option>Evento / Rodaje</option>', '<option>Event / Shoot</option>'),
('<option>Staging / Promoción inmobiliaria</option>', '<option>Staging / Property development</option>'),
('<option>Proyecto cultural</option>', '<option>Cultural project</option>'),
('<option>Solo quiero ver la colección</option>', '<option>I just want to see the collection</option>'),
('<option>Otro</option>', '<option>Other</option>'),
('<option>1-3 meses</option>', '<option>1-3 months</option>'), ('<option>3-6 meses</option>', '<option>3-6 months</option>'),
('<option>6-12 meses</option>', '<option>6-12 months</option>'), ('<option>Más de 12 meses</option>', '<option>More than 12 months</option>'),
('<option>Evento puntual</option>', '<option>One-off event</option>'), ('<option>Aún no lo sé</option>', '<option>Not sure yet</option>'),
('He leído y acepto la <a href="../privacidad.html" target="_blank">política de privacidad</a>. *', 'I have read and accept the <a href="../privacidad.html" target="_blank">privacy policy</a> (in Spanish). *'),
('>Solicitar dossier</button>', '>Request the dossier</button>'),
('<b>Protección de datos.</b> Responsable: Enrique Aznar (Eleve Art). Finalidad: responder a tu solicitud y enviarte la información pedida. Legitimación: tu consentimiento y la aplicación de medidas precontractuales. Destinatarios: proveedores tecnológicos que prestan el servidor y el envío de correo, algunos en EE. UU. con las garantías del RGPD. Derechos: acceso, rectificación, supresión, oposición y demás, escribiendo a coleccion@eleve.art. Más información en la <a href="../privacidad.html" target="_blank">política de privacidad</a>.',
 '<b>Data protection.</b> Controller: Enrique Aznar (Eleve Art). Purpose: to answer your request and send you the information requested. Legal basis: your consent and pre-contractual measures. Recipients: technology providers supplying the server and email delivery, some in the USA with GDPR safeguards. Rights: access, rectification, erasure, objection and others, by writing to coleccion@eleve.art. More information in the <a href="../privacidad.html" target="_blank">privacy policy</a> (in Spanish).'),
('Qué incluye el dossier privado', 'What the private dossier includes'),
('Fotografías de cada obra y de sus detalles', 'Photographs of each work and its details'),
('Ficha técnica completa: técnica, medidas, edición y estado', 'Full technical record: technique, dimensions, edition and condition'),
('Documentación: certificados, procedencia y referencias de catálogo', 'Documentation: certificates, provenance and catalogue references'),
('Disponibilidad y condiciones de alquiler', 'Availability and rental conditions'),
('Una primera selección curada para tu proyecto', 'A first curated selection for your project'),
# ---------- ficha (lightbox) ----------
('aria-label="Cerrar"', 'aria-label="Close"'), ('aria-label="Obra anterior"', 'aria-label="Previous work"'), ('aria-label="Obra siguiente"', 'aria-label="Next work"'),
('Fotografía no publicada por respeto a los derechos de reproducción del artista. Disponible en el dossier privado, a solicitud.', 'Photograph not published out of respect for the artist’s reproduction rights. Available in the private dossier on request.'),
('>Página de la obra →<', '>Page of the work (in Spanish) →<'),
('<div class="lb-rental-title">Disponible para alquiler</div>', '<div class="lb-rental-title">Available to rent</div>'),
('Opción de compra disponible tras alquiler.', 'Purchase option available after rental.'),
('>Solicitar acceso a esta obra<', '>Request the dossier for this work<'),
("content:'Catalogación y procedencia'", "content:'Cataloguing and provenance'"),
# ---------- pie ----------
('Eleve Art · Todos los derechos reservados', 'Eleve Art · All rights reserved'),
('Los derechos de reproducción de las obras pertenecen a sus autores y herederos. Esta web no publica imágenes de las obras salvo dominio público, licencia de VEGAP o autorización expresa. Los enlaces externos remiten a publicaciones de terceros autorizadas. Eleve Art no está vinculada a los museos, fundaciones o webs enlazadas.',
 'Reproduction rights in the works belong to their authors and heirs. This website does not publish images of the works except in the public domain, under a VEGAP licence or with express permission. External links point to authorised third-party publications. Eleve Art is not affiliated with the museums, foundations or websites linked.'),
('>Términos legales<', '>Legal terms (ES)<'), ('>Privacidad<', '>Privacy (ES)<'),
('<div class="footer-email">Contacto:', '<div class="footer-email">Contact:'),
# ---------- chat ----------
('<p>Asistente de colección</p>', '<p>Collection assistant</p>'),
('title="Asistente Eleve Art"', 'title="Eleve Art assistant"'),
('<p>Para enviarte la propuesta completa:</p>', '<p>So we can send you the full proposal:</p>'),
('placeholder="tu@email.com"', 'placeholder="you@email.com"'),
('>Enviar</button>', '>Send</button>'),
('<span>Acepto la <a href="../privacidad.html" target="_blank">política de privacidad</a>. Usaremos tu email y la conversación solo para responderte.</span>',
 '<span>I accept the <a href="../privacidad.html" target="_blank">privacy policy</a> (in Spanish). We will use your email and the conversation only to reply to you.</span>'),
('placeholder="Cuéntame tu proyecto..."', 'placeholder="Tell me about your project..."'),
("Hola. Soy el asistente de Eleve Art.\\n\\nCuéntame tu espacio (hotel, oficina, casa…), el estilo que buscas y el plazo, y te sugiero un nivel y obras de la colección.",
 "Hello. I am the Eleve Art assistant.\\n\\nTell me about your space (hotel, office, home…), the style you are after and the timing, and I will suggest a level and works from the collection."),
("'Gracias. Te escribiremos a '+em+' en menos de 24 horas con una propuesta.'", "'Thank you. We will write to '+em+' within 24 hours with a proposal.'"),
("Ha habido un problema. Contacta a coleccion@eleve.art", "Something went wrong. Please contact coleccion@eleve.art"),
# ---------- JS: textos de interfaz ----------
("iconic: {label:\"Sección I\", title:\"Piezas Icónicas\", desc:\"Obras originales de los maestros: óleos, pinturas y grabados de autoría singular. Piezas con certificación y procedencia documentada.\"",
 "iconic: {label:\"Section I\", title:\"Iconic Pieces\", desc:\"Original works by the masters: oils, paintings and prints of singular authorship. Pieces with certification and documented provenance.\""),
("graphic: {label:\"Sección II\", title:\"Obra Gráfica\", desc:\"Grabados, aguafuertes y ediciones limitadas de artistas consagrados. Obra múltiple de alta calidad con certificados de autenticidad.\"",
 "graphic: {label:\"Section II\", title:\"Original Prints\", desc:\"Engravings, etchings and limited editions by established artists. High-quality multiples with certificates of authenticity.\""),
("available: {label:\"Sección III\", title:\"Obra Accesible\", desc:\"Piezas de artistas reconocidos en condiciones accesibles. Ideales para completar proyectos de interiorismo y coleccionismo.\"",
 "available: {label:\"Section III\", title:\"Accessible Works\", desc:\"Pieces by recognised artists on accessible terms. Ideal for completing interior design and collecting projects.\""),
("<div class=\"section-label\">${sec.label} · ${items.length} obras</div>", "<div class=\"section-label\">${sec.label} · ${items.length} works</div>"),
("${allItems.length} obra${allItems.length > 1 ? 's' : ''}</div><h2 class=\"finder-main-title\">Resultados</h2>", "${allItems.length} work${allItems.length > 1 ? 's' : ''}</div><h2 class=\"finder-main-title\">Results</h2>"),
("No se han encontrado obras con ese criterio. <a href=\"#contacto\" style=\"color:var(--gold);\">Cuéntanos qué buscas</a> y te ayudamos.", "No works match that search. <a href=\"#contacto\" style=\"color:var(--gold);\">Tell us what you are looking for</a> and we will help."),
(">Ver ficha</a>", ">View record</a>"),
("'Consultar disponibilidad' : 'Solicitar alquiler'", "'Check availability' : 'Request to rent'"),
(">Solicitar acceso</button>`)", ">Request the dossier</button>`)"),
("'<span class=\"cat-tag\">Alquilado</span>' : gst === 'reservado' ? '<span class=\"cat-tag\">Reservado</span>'", "'<span class=\"cat-tag\">Rented</span>' : gst === 'reservado' ? '<span class=\"cat-tag\">Reserved</span>'"),
("[['Año', item.year],['Técnica', item.medium],['Dimensiones', item.dimensions],['Estilo', item.style],['Edición', item.edition]]",
 "[['Year', item.year],['Technique', item.medium],['Dimensions', item.dimensions],['Style', item.style],['Edition', item.edition]]"),
("ref.innerHTML = `Ver la obra en ${", "ref.innerHTML = `See the work at ${"),
("alEl.textContent = `Sobre ${item.artist}: ${al.label} ↗`", "alEl.textContent = `About ${item.artist}: ${al.label} ↗`"),
("secBtn.textContent = 'Solicitar dossier de esta obra →';", "secBtn.textContent = 'Email us about this work →';"),
("secBtn.textContent = 'Contactar por esta obra →';", "secBtn.textContent = 'Email us about this work →';"),
("'Indica un email válido para poder responderte.'", "'Please enter a valid email so we can reply.'"),
("'Para enviar la solicitud debes aceptar la política de privacidad.'", "'To send your request you must accept the privacy policy.'"),
("'Indica tu nombre.'", "'Please enter your name.'"),
("btn.textContent = 'Enviando…';", "btn.textContent = 'Sending…';"),
("'Gracias. Hemos recibido tu solicitud y te responderemos en menos de 24 horas.'", "'Thank you. We have received your request and will reply within 24 hours.'"),
("'Gracias. Te hemos enviado a ' + payload.email + ' un enlace personal a la colección privada para que veas las obras y descargues tu dossier en PDF. Si no lo recibes en unos minutos, revisa la carpeta de spam.'", "'Thank you. We have sent ' + payload.email + ' a personal link to the private collection, where you can see the works and download your dossier as a PDF (in Spanish). If it does not arrive within a few minutes, please check your spam folder.'"),
("'Te acabamos de enviar a '+em+' un enlace personal a la colección privada, con las fotos de las obras, para que prepares y descargues tu dossier.'", "'We have just sent '+em+' a personal link to the private collection, with photos of the works, so you can prepare and download your dossier (in Spanish).'"),
("`No hemos podido enviarlo automáticamente. Se ha abierto tu programa de correo con el mensaje preparado: pulsa «Enviar». Si no se abre, escríbenos a ${CONTACT_EMAIL}.`",
 "`We could not send it automatically. Your email program has opened with the message ready: press “Send”. If it does not open, write to us at ${CONTACT_EMAIL}.`"),
("name: 'Colección Eleve Art · Obras disponibles para alquiler'", "name: 'Eleve Art Collection · Works available to rent'"),
("url: 'https://eleve.art/#obra/' + c.id", "url: 'https://eleve.art/obra/' + c.id + '.html'"),
]
for es, en in T:
    raw(es, en)

# etiquetas de filtros y opciones cortas (solo como texto de botón)
for es, en in [('Todas', 'All'), ('Abstracto', 'Abstract'), ('Figurativo', 'Figurative'), ('Surrealismo', 'Surrealism'),
               ('Informalismo / Matérico', 'Art Informel / Matter painting'), ('Cubista', 'Cubist'), ('Pop / Figuración narrativa', 'Pop / Narrative figuration'),
               ('Contemporáneo', 'Contemporary'), ('Escultura', 'Sculpture'), ('Dau al Set / Catalán', 'Dau al Set / Catalan'), ('Disponibles ahora', 'Available now'),
               ('Hotel boutique', 'Boutique hotel'), ('Interiorismo residencial', 'Residential interiors'), ('Esencial', 'Essential')]:
    ui(es, en, required=False)

# búsqueda: añadir términos en inglés
raw("const CAT_SEARCH = {abstracto:'abstracto',figurativo:'figurativo',surrealismo:'surrealismo',informalismo:'informalismo matérico',cubista:'cubista',pop:'pop figuración narrativa',contemporaneo:'contemporáneo',dauaset:'dau al set catalán català',escultura:'escultura'};",
    "const CAT_SEARCH = {abstracto:'abstracto abstract',figurativo:'figurativo figurative',surrealismo:'surrealismo surrealism',informalismo:'informalismo matérico informel matter',cubista:'cubista cubist cubism',pop:'pop figuración narrativa narrative figuration',contemporaneo:'contemporáneo contemporary',dauaset:'dau al set catalán català catalan',escultura:'escultura sculpture'};")

# selector de idioma
raw('<span>ES</span> · <a href="en/" hreflang="en" lang="en">EN</a>', '<a href="../" hreflang="es" lang="es">ES</a> · <span>EN</span>', required=False)

# ---------- datos de las obras ----------
tr_path = os.path.join(ROOT, '_tools', 'i18n', 'en-collection.json')
if os.path.exists(tr_path):
    tr = json.load(open(tr_path, encoding='utf-8'))
    m = re.search(r'const COLLECTION = (\[[\s\S]*?\n\]);', s)
    col = json.loads(m.group(1))
    for o in col:
        t = tr.get(o['id'], {})
        for k in ('medium', 'dimensions', 'style', 'edition', 'description', 'blurb', 'ref_note'):
            if t.get(k) not in (None, ''):
                o[k] = t[k]
    s = s.replace(m.group(0), 'const COLLECTION = ' + json.dumps(col, ensure_ascii=False, indent=2) + ';')
else:
    print('AVISO: falta _tools/i18n/en-collection.json; las fichas quedan en español')

# etiquetas de enlaces de artista
m = re.search(r'const ARTIST_LINKS = (\{[\s\S]*?\n\});', s)
al = json.loads(m.group(1))
LBL = {'Web del artista': 'Artist’s website', 'Web de la artista': 'Artist’s website', 'Web oficial': 'Official website',
       'serie Pandasan en la web del artista': 'the Pandasan series on the artist’s website',
       'MACBA, Museo de Arte Contemporáneo de Barcelona': 'MACBA, Barcelona Museum of Contemporary Art', 'Museo Reina Sofía': 'Museo Reina Sofía, Madrid',
       'Museo Nacional Thyssen-Bornemisza': 'Thyssen-Bornemisza National Museum'}
for v in al.values():
    v['label'] = LBL.get(v['label'], v['label'])
    v['url'] = v['url'].replace('museoreinasofia.es/colecciones/artista/', 'museoreinasofia.es/en/collection/artist/') if False else v['url']
s = s.replace(m.group(0), 'const ARTIST_LINKS = ' + json.dumps(al, ensure_ascii=False, indent=1) + ';')
s = s.replace('"ref_label": "Setdart (subasta)"', '"ref_label": "Setdart (auction)"')

# el contenido pre-renderizado en español se vacía: lo vuelve a pintar el JS (y se pre-renderiza después)
s = re.sub(r'<div id="main">.*?<!-- /main -->', '<div id="main"></div><!-- /main -->', s, flags=re.S)
s = re.sub(r'(<script type="application/ld\+json" id="ld-collection">).*?(</script>)', r'\1\2', s, flags=re.S)

os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
open(os.path.join(ROOT, 'en', 'index.html'), 'w', encoding='utf-8').write(s)
print('en/index.html generado.', 'Sin coincidencia:' if missing else 'Todas las cadenas aplicadas.')
for x in missing: print('  -', x)
