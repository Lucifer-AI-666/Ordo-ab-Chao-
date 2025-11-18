#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ordo ab Chao - Icon Generator
Genera tutte le icone PWA automaticamente
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Directory output
OUTPUT_DIR = "/Users/dib/Ordo-ab-Chao-/web"

# Dimensioni icone standard
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Icone speciali
SPECIAL_ICONS = [
    {"name": "icon-tauros.png", "size": 192, "emoji": "🐂", "color": "#ff4444"},
    {"name": "icon-lucy.png", "size": 192, "emoji": "🧠", "color": "#7b68ee"},
    {"name": "icon-dashboard.png", "size": 192, "emoji": "📊", "color": "#00d4ff"}
]

def create_gradient(draw, size, color1, color2):
    """Crea un gradient diagonale"""
    for i in range(size):
        # Calcola colore intermedio
        ratio = i / size
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)

        # Disegna linea diagonale
        draw.line([(0, i), (size, i)], fill=(r, g, b))

def hex_to_rgb(hex_color):
    """Converte colore hex in RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_main_icon(size):
    """Crea icona principale Ordo ab Chao"""
    # Crea immagine
    img = Image.new('RGB', (size, size), color='#1a1a2e')
    draw = ImageDraw.Draw(img)

    # Background gradient
    color1 = hex_to_rgb('#1a1a2e')
    color2 = hex_to_rgb('#00d4ff')

    for i in range(size):
        ratio = i / size
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, i), (size, i)], fill=(r, g, b))

    # Secondo gradient sovrapposto
    for i in range(size):
        ratio = i / size
        alpha = int(255 * ratio * 0.3)
        color3 = hex_to_rgb('#7b68ee')
        # Blend con il background

    # Border
    border_width = max(1, size // 50)
    draw.rectangle(
        [0, 0, size - 1, size - 1],
        outline=(255, 255, 255, 80),
        width=border_width
    )

    # Testo "⚡"
    try:
        # Prova a usare font system
        font_size = int(size * 0.6)
        font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", font_size)
    except:
        # Fallback su font default
        font = ImageFont.load_default()

    # Disegna emoji fulmine
    text = "⚡"

    # Calcola posizione centrata
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2 - int(size * 0.05)

    # Ombra
    shadow_offset = max(2, size // 100)
    draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 128), font=font)

    # Testo principale
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    # Testo "ORDO" in basso
    try:
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size * 0.12))
    except:
        font_small = ImageFont.load_default()

    ordo_text = "ORDO"
    bbox = draw.textbbox((0, 0), ordo_text, font=font_small)
    text_width = bbox[2] - bbox[0]

    x_ordo = (size - text_width) // 2
    y_ordo = int(size * 0.82)

    draw.text((x_ordo, y_ordo), ordo_text, fill=(228, 228, 228), font=font_small)

    return img

def create_special_icon(size, emoji, color):
    """Crea icona speciale per Tauros/Lucy/Dashboard"""
    # Crea immagine
    img = Image.new('RGB', (size, size), color='#1a1a2e')
    draw = ImageDraw.Draw(img)

    # Background gradient radiale simulato
    center = size // 2
    max_radius = size // 2

    color_rgb = hex_to_rgb(color)
    bg_rgb = hex_to_rgb('#1a1a2e')

    # Disegna cerchi concentrici per simulare gradient radiale
    for radius in range(max_radius, 0, -1):
        ratio = radius / max_radius
        r = int(bg_rgb[0] * (1 - ratio) + color_rgb[0] * ratio)
        g = int(bg_rgb[1] * (1 - ratio) + color_rgb[1] * ratio)
        b = int(bg_rgb[2] * (1 - ratio) + color_rgb[2] * ratio)

        draw.ellipse(
            [center - radius, center - radius, center + radius, center + radius],
            fill=(r, g, b)
        )

    # Border
    border_width = max(1, size // 50)
    draw.rectangle(
        [0, 0, size - 1, size - 1],
        outline=(255, 255, 255, 80),
        width=border_width
    )

    # Emoji
    try:
        font_size = int(size * 0.5)
        font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", font_size)
    except:
        font = ImageFont.load_default()

    # Calcola posizione centrata
    bbox = draw.textbbox((0, 0), emoji, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2

    draw.text((x, y), emoji, fill=(255, 255, 255), font=font)

    return img

def main():
    """Genera tutte le icone"""
    print("🎨 Ordo ab Chao - Generazione Icone PWA")
    print("=" * 60)
    print()

    # Crea directory se non esiste
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Genera icone standard
    print("📱 Generazione icone standard...")
    for size in ICON_SIZES:
        filename = f"icon-{size}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)

        print(f"  ⚡ Creando {filename} ({size}x{size})...")
        img = create_main_icon(size)
        img.save(filepath, 'PNG', quality=95)

        print(f"     ✅ Salvato: {filepath}")

    print()
    print("🎯 Generazione icone speciali...")

    # Genera icone speciali
    for icon_info in SPECIAL_ICONS:
        name = icon_info['name']
        size = icon_info['size']
        emoji = icon_info['emoji']
        color = icon_info['color']

        filepath = os.path.join(OUTPUT_DIR, name)

        print(f"  {emoji} Creando {name}...")
        img = create_special_icon(size, emoji, color)
        img.save(filepath, 'PNG', quality=95)

        print(f"     ✅ Salvato: {filepath}")

    print()
    print("=" * 60)
    print("✅ TUTTE LE ICONE GENERATE CON SUCCESSO!")
    print()
    print(f"📁 Directory: {OUTPUT_DIR}")
    print(f"📊 Totale icone: {len(ICON_SIZES) + len(SPECIAL_ICONS)}")
    print()
    print("🚀 Ora puoi avviare la PWA con: ./avvia-pwa.sh")
    print("=" * 60)

if __name__ == '__main__':
    main()
