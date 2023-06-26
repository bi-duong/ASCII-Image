from PIL import Image, ImageDraw, ImageFont
import numpy as np


# The function converts an image to ASCII art
def asciiart(in_f, SC, GCF, out_f, color1='black', color2='blue', bgcolor='white'):
    # The array of ASCII symbols from white to black
    chars = np.asarray(list(' .,:irs?@9B&#'))

    # Load the fonts and then get the height and width of a typical symbol
    # You can use different fonts here
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]

    WCF = letter_height / letter_width

    # Open the input file
    img = Image.open(in_f)

    # Calculate the number of ASCII letters needed on the width and height based on the desired output image size
    widthByLetter = round(img.size[0] * SC * WCF)
    heightByLetter = round(img.size[1] * SC)
    S = (widthByLetter, heightByLetter)

    # Resize the image based on the symbol width and height
    img = img.resize(S)

    # Convert the RGB color values of each sampled pixel point to grayscale using the average method
    img = np.sum(np.asarray(img), axis=2)

    # Normalize the results, enhance, and reduce the brightness contrast
    # Map grayscale values to bins of symbols
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    # Generate the ASCII art symbols
    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")

    # Create gradient color bins
    nbins = len(lines)
    colorRange = [color1, color2]

    # Create an image object and set its width and height
    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)

    # Print symbols to the image
    leftpadding = 0
    y = 0
    lineIdx = 0
    for line in lines:
        color = colorRange[lineIdx % 2]
        lineIdx += 1

        draw.text((leftpadding, y), line, color, font=font)
        y += letter_height

    # Save the image file
    newImg.save(out_f)


# main()
if __name__ == '__main__':
    inputf = "test10.jpg"  # Input image file name

    SC = 0.1  # Pixel sampling rate in width
    GCF = 2  # Contrast adjustment

    # ASCII art with default colors (black to blue)
    asciiart(inputf, SC, GCF, "result1.png")

    # ASCII art with custom colors (black to magenta)
    
