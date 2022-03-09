# This file creates a simple interface to use a db with the bot
import sqlite3
from PIL import Image

# Create connection and cursor to DB
con = sqlite3.connect("fontano.db")
cur = con.cursor()

# Transparency bound for pixels
transparency_bound = 204 # 80% (Alpha value)

# Create tables if they don't exist already
def createtables(tables):
    for table, schema in tables.items():
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema[0]}, CONSTRAINT {table}_pk PRIMARY KEY ({schema[1]}))")
    con.commit()

# Query and return result as a set of tuples
def query(querystring):
    cur.execute(querystring)
    return set(cur.fetchall())

def updatequery(query):
    cur.execute(query)
    con.commit()

# To convert rgb values to hex color values
def rgb_to_hex(rgb):
    r = f"0x0{hex(rgb[0])[-1]}" if rgb[0] < 16 else str(hex(rgb[0]))
    g = f"0x0{hex(rgb[1])[-1]}" if rgb[1] < 16 else str(hex(rgb[1]))
    b = f"0x0{hex(rgb[2])[-1]}" if rgb[2] < 16 else str(hex(rgb[2]))
    return f"#{r[-2:]}{g[-2:]}{b[-2:]}"

# Load picture into DB
def loadpicture(image: Image):
    cur.execute("DELETE FROM pixels;")
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            alpha = pixel[3]
            if alpha < transparency_bound:
                continue
            color = rgb_to_hex(pixel[:3])
            cur.execute(f"""INSERT INTO pixels (xpos, ypos, color, alpha, drawn) VALUES ({x}, {y}, "{color}", {alpha}, FALSE)""")
    con.commit()
