import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np


def convert_to_ascii():
    input_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".png")

    SC = float(sc_entry.get())
    GCF = float(gcf_entry.get())

    asciiart(input_file, SC, GCF, output_file)

    # Display the converted image on the GUI
    display_image(output_file)


def asciiart(in_f, SC, GCF, out_f, color1='black', color2='blue', bgcolor='white'):
    chars = np.asarray(list(' .,:irs?@9B&#'))
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height / letter_width

    img = Image.open(in_f)
    widthByLetter = round(img.size[0] * SC * WCF)
    heightByLetter = round(img.size[1] * SC)
    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)
    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")
    nbins = len(lines)
    colorRange = [color1, color2]
    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)
    leftpadding = 0
    y = 0
    lineIdx = 0
    for line in lines:
        color = colorRange[lineIdx % 2]
        lineIdx += 1
        draw.text((leftpadding, y), line, color, font=font)
        y += letter_height
    newImg.save(out_f)
    return out_f


def display_image(image_file):
    # Display the converted image on the GUI
    image = Image.open(image_file)
    image.thumbnail((400, 400))  # Resize the image to fit in the GUI
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo


# Create the main window
window = tk.Tk()
window.title("ASCII Art Converter")

# Create the input file label and button
input_file_label = tk.Label(window, text="Input File:")
input_file_label.pack()
input_file_button = tk.Button(window, text="Choose File", command=convert_to_ascii)
input_file_button.pack()

# Create the pixel sampling rate entry
sc_label = tk.Label(window, text="Pixel Sampling Rate:")
sc_label.pack()
sc_entry = tk.Entry(window)
sc_entry.insert(tk.END, "0.1")
sc_entry.pack()

# Create the contrast adjustment entry
gcf_label = tk.Label(window, text="Contrast Adjustment:")
gcf_label.pack()
gcf_entry = tk.Entry(window)
gcf_entry.insert(tk.END, "2")
gcf_entry.pack()

# Create the image label to display the converted image
image_label = tk.Label(window)
image_label.pack()

# Start the tkinter event loop
window.mainloop()
