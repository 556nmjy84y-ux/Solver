#!/usr/bin/env python3
"""Deriva la version publicable de fieltro.html.

El visor de artefactos envuelve el contenido en su propio <!doctype html>,
<head> y <body>, asi que aqui solo se entrega el <title>, el <style> y el
cuerpo con sus scripts. Se genera, no se edita a mano: la fuente unica sigue
siendo fieltro.html.
"""
import re, sys, pathlib

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "fieltro.html").read_text(encoding="utf-8")
dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "fieltro-artefacto.html")

estilo = re.search(r'<style>[\s\S]*?</style>', src).group(0)
cuerpo = re.search(r'<body>([\s\S]*)</body>', src).group(1)

# los <link rel=icon> viven en el head y ahi no llegan; el icono lo pone el
# parametro favicon al publicar, asi que se van con sus 18 KB de base64
cuerpo = re.sub(r'\s*<link rel="(?:apple-touch-)?icon"[^>]*>', "", cuerpo)

# El aviso de "pagina sin arrancar" habla de abrir un .html suelto en el movil.
# Publicada, la pagina se sirve por http y ese consejo no aplica.
cuerpo = re.sub(
    r'<div id="arranque">[\s\S]*?</div>\n',
    '<div id="arranque">\n'
    '  <b>Esta página no ha arrancado.</b> Todo lo que ves es el armazón: el board, la rejilla\n'
    '  y los botones los construye el JavaScript, que aquí no se ha ejecutado. Prueba a\n'
    '  recargar; si sigue igual, tu navegador lo tiene desactivado.\n'
    '</div>\n',
    cuerpo, count=1)

dst.write_text("<title>Fieltro solver</title>\n" + estilo + "\n" + cuerpo.strip() + "\n",
               encoding="utf-8")
print(f"{dst} · {dst.stat().st_size/1024:.0f} KB")
