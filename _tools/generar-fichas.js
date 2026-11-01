// Genera una página estática por obra en /obra/<id>.html y actualiza sitemap.xml.
// Fuente de datos: COLLECTION, SECTIONS y ARTIST_LINKS de index.html.
// Uso: node _tools/generar-fichas.js   (ejecutar tras cualquier cambio de obras)
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SITE = 'https://eleve-art.com';
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const grab = re => { const m = html.match(re); if (!m) throw new Error('No encontrado: ' + re); return (0, eval)('(' + m[1] + ')'); };
const COLLECTION = grab(/const COLLECTION = (\[[\s\S]*?\n\]);/);
const ARTIST_LINKS = grab(/const ARTIST_LINKS = (\{[\s\S]*?\n\});/);
const SECTIONS = grab(/const SECTIONS = (\{[\s\S]*?\n\});/);

const esc = v => String(v ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const shortMedium = m => (m || '').split(/[·,(]/)[0].trim();
const metaLine = it => [it.year, shortMedium(it.medium)].filter(v => v && v !== '—').join(' · ');
const num = it => 'Nº ' + String(COLLECTION.indexOf(it) + 1).padStart(2, '0');
const cut = (t, n) => { t = String(t || '').replace(/\s+/g, ' ').trim(); return t.length <= n ? t : t.slice(0, t.lastIndexOf(' ', n)) + '…'; };

const OUT = path.join(ROOT, 'obra');
fs.mkdirSync(OUT, { recursive: true });
for (const f of fs.readdirSync(OUT)) if (f.endsWith('.html')) fs.unlinkSync(path.join(OUT, f));

COLLECTION.forEach((it, i) => {
  const url = `${SITE}/obra/${it.id}.html`;
  const sec = SECTIONS[it.section] || { title: 'Colección' };
  const title = `${it.artist} — ${it.title}`;
  const desc = cut(`Alquiler de obra original: ${it.title} de ${it.artist}${it.year && it.year !== '—' ? ` (${it.year})` : ''}. ${it.blurb || it.description}`, 158);
  const fields = [['Año', it.year], ['Técnica', it.medium], ['Dimensiones', it.dimensions], ['Estilo', it.style], ['Edición', it.edition]]
    .filter(([, v]) => v && v !== '—');
  const al = ARTIST_LINKS[it.artist];
  const same = COLLECTION.filter(c => c.artist === it.artist && c.id !== it.id).slice(0, 6);
  const prev = COLLECTION[(i - 1 + COLLECTION.length) % COLLECTION.length], next = COLLECTION[(i + 1) % COLLECTION.length];
  const ld = {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'VisualArtwork', name: it.title, url, creator: { '@type': 'Person', name: it.artist },
        artMedium: it.medium || undefined, dateCreated: it.year && it.year !== '—' ? it.year : undefined, description: it.blurb || it.description,
        isPartOf: { '@type': 'Collection', name: 'Colección Eleve Art', url: SITE + '/' } },
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Eleve Art', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: sec.title, item: SITE + '/#coleccion' },
        { '@type': 'ListItem', position: 3, name: title, item: url }] }
    ]
  };
  const page = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)} | Alquiler de arte · Eleve Art</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${url}">
<meta property="og:title" content="${esc(title)} | Eleve Art">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${url}">
<meta property="og:type" content="website">
<meta property="og:image" content="${SITE}/img/og-eleve-art.jpg">
<meta property="og:locale" content="es_ES">
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../fonts/fonts.css">
<link rel="stylesheet" href="ficha.css">
<script type="application/ld+json">${JSON.stringify(ld)}</script>
</head>
<body>
<header class="hd"><a class="logo" href="../">Eleve <span>Art</span></a><a class="back" href="../#coleccion">← La colección</a></header>
<main class="wrap">
  <nav class="crumbs" aria-label="Ruta"><a href="../">Eleve Art</a> › <a href="../#coleccion">${esc(sec.title)}</a> › ${num(it)}</nav>
  <div class="grid">
    <article>
      <div class="artist">${esc(it.artist)}</div>
      <h1>${esc(it.title)}</h1>
      <p class="meta">${esc(metaLine(it))}</p>
      <p class="blurb">${esc(it.blurb || '')}</p>
      <p class="nophoto">Fotografía no publicada por respeto a los derechos de reproducción del artista. Disponible en el dossier privado, a solicitud.</p>
      ${it.ref_url ? `<a class="ref" href="${esc(it.ref_url)}" target="_blank" rel="noopener nofollow">Ver la obra en ${esc(it.ref_label || 'otra web')} ↗${it.ref_note ? `<small>${esc(it.ref_note)}</small>` : ''}</a>` : ''}
      ${al ? `<a class="artist-link" href="${esc(al.url)}" target="_blank" rel="noopener">Sobre ${esc(it.artist)}: ${esc(al.label)} ↗</a>` : ''}
      <dl class="fields">${fields.map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>
      ${it.description ? `<section class="cat"><h2>Catalogación y procedencia</h2><p>${esc(it.description)}</p></section>` : ''}
    </article>
    <aside class="side">
      <div class="box">
        <div class="box-label">Disponible para alquiler</div>
        <p>Recibe el dossier con fotografías, ficha completa y condiciones de esta obra, y una propuesta para tu espacio.</p>
        <a class="cta" href="../?obra=${encodeURIComponent(it.id)}#contacto">Solicitar dossier de esta obra</a>
        <p class="small">Respuesta en menos de 24 horas · Barcelona, Madrid y toda España</p>
      </div>
      ${same.length ? `<div class="more"><div class="box-label">Más de ${esc(it.artist)} en la colección</div><ul>${same.map(c => `<li><a href="${c.id}.html">${esc(c.title)}</a></li>`).join('')}</ul></div>` : ''}
    </aside>
  </div>
  <nav class="pager"><a href="${prev.id}.html">← ${esc(prev.artist)} · ${esc(cut(prev.title, 40))}</a><a href="${next.id}.html">${esc(next.artist)} · ${esc(cut(next.title, 40))} →</a></nav>
</main>
<footer class="ft">Eleve Art · Alquiler de arte original · <a href="../">eleve-art.com</a> · <a href="../terminos-legales.html">Términos legales</a> · <a href="../privacidad.html">Privacidad</a><br>Los derechos de reproducción de las obras pertenecen a sus autores y herederos. Eleve Art no está vinculada a las webs enlazadas.</footer>
</body>
</html>
`;
  fs.writeFileSync(path.join(OUT, it.id + '.html'), page);
});

fs.writeFileSync(path.join(OUT, 'ficha.css'), `:root{--ivory:#f7f4ef;--cream:#faf8f5;--parchment:#ede8df;--linen:#d9d0c1;--ash:#9e9890;--charcoal:#2c2a27;--ink:#1a1917;--gold:#b89a5e;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Jost',sans-serif;font-weight:300;background:var(--cream);color:var(--charcoal);}
a{color:inherit;}
.hd{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;padding:0 48px;height:64px;background:rgba(247,244,239,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--parchment);}
.logo{font-family:'Cormorant Garamond',serif;font-size:22px;letter-spacing:4px;text-transform:uppercase;color:var(--ink);text-decoration:none;}
.logo span{color:var(--gold);font-weight:600;}
.back{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;color:var(--ash);}
.back:hover{color:var(--ink);}
.wrap{max-width:1120px;margin:0 auto;padding:48px 48px 72px;}
.crumbs{font-size:11px;letter-spacing:1px;color:var(--ash);margin-bottom:36px;}
.crumbs a{text-decoration:none;}
.crumbs a:hover{color:var(--gold);}
.grid{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:64px;align-items:start;}
.artist{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:10px;}
h1{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:300;font-size:clamp(34px,4.5vw,56px);line-height:1.1;color:var(--ink);margin-bottom:10px;}
.meta{font-size:13px;color:var(--ash);margin-bottom:28px;}
.blurb{font-family:'Cormorant Garamond',serif;font-size:clamp(20px,2vw,24px);line-height:1.55;color:var(--ink);margin-bottom:18px;}
.nophoto{font-size:12px;font-style:italic;color:var(--ash);margin-bottom:22px;}
.ref{display:block;padding:14px 18px;border:1px solid var(--gold);color:var(--gold);text-decoration:none;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;}
.ref small{display:block;text-transform:none;letter-spacing:.3px;color:var(--ash);margin-top:4px;font-size:11px;}
.artist-link{display:inline-block;font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--charcoal);text-decoration:none;border-bottom:1px solid var(--linen);padding-bottom:2px;margin-bottom:28px;}
.artist-link:hover,.ref:hover{color:var(--ink);}
.fields{display:grid;grid-template-columns:1fr 1fr;gap:16px 28px;border-top:1px solid var(--parchment);padding-top:24px;margin-bottom:28px;}
.fields dt{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:var(--ash);margin-bottom:3px;}
.fields dd{font-size:14px;line-height:1.5;}
.cat h2{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--ash);font-weight:400;margin-bottom:8px;}
.cat p{font-size:14px;line-height:1.85;}
.side{position:sticky;top:96px;}
.box{border:1px solid var(--parchment);background:var(--ivory);padding:28px;}
.box-label{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:12px;}
.box p{font-size:13.5px;line-height:1.75;margin-bottom:18px;}
.cta{display:block;text-align:center;background:var(--ink);color:var(--cream);text-decoration:none;font-size:11px;letter-spacing:2.5px;text-transform:uppercase;padding:15px 18px;}
.cta:hover{background:var(--charcoal);}
.small{font-size:11px !important;color:var(--ash);margin:14px 0 0 !important;}
.more{margin-top:28px;}
.more ul{list-style:none;}
.more li{border-bottom:1px solid var(--parchment);}
.more a{display:block;padding:9px 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:17px;text-decoration:none;color:var(--ink);}
.more a:hover{color:var(--gold);}
.pager{display:flex;justify-content:space-between;gap:20px;margin-top:64px;padding-top:24px;border-top:1px solid var(--parchment);font-size:12px;}
.pager a{text-decoration:none;color:var(--ash);}
.pager a:hover{color:var(--gold);}
.ft{padding:36px 24px;text-align:center;border-top:1px solid var(--parchment);background:var(--ivory);font-size:11px;line-height:1.9;color:var(--ash);}
.ft a{color:var(--gold);text-decoration:none;}
@media(max-width:860px){.hd{padding:0 16px;}.wrap{padding:28px 20px 56px;}.grid{grid-template-columns:1fr;gap:36px;}.side{position:static;}.pager{flex-direction:column;}}
`);

// sitemap
const today = new Date().toISOString().slice(0, 10);
const base = ['/', '/en-la-ciudad.html'];
const extra = fs.existsSync(path.join(ROOT, 'en', 'index.html')) ? ['/en/'] : [];
const urls = [...base, ...extra].map(u => `  <url><loc>${SITE}${u}</loc><lastmod>${today}</lastmod></url>`)
  .concat(COLLECTION.map(it => `  <url><loc>${SITE}/obra/${it.id}.html</loc><lastmod>${today}</lastmod></url>`));
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`);
console.log(`${COLLECTION.length} fichas generadas en /obra y sitemap actualizado (${urls.length} URLs).`);
