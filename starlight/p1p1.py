import time
from PIL import Image
from starlight import p_getter
import io
import requests
import re

im_width = 146
im_height = 204


def make_p1p1(setcode):
    """Creates a composite image of a pack from the set.

    Returns a BytesIO object."""
    # Grab from get_p1p1_v3
    pack, foils = p_getter.get_p1p1_v3(setcode)
    width = min(len(pack), 5) * im_width
    height = (len(pack) // 5) if len(pack) % 5 == 0 else (len(pack) // 5 + 1)
    height = height * im_height
    image_composite = Image.new("RGBA", (width, height))
    row = 0
    column = 0
    resp = requests.get("https://i.imgur.com/1zBWUSU.png", stream=True)
    foil_image = Image.open(io.BytesIO(resp.content))
    # for each card in the pack,
    #  if column == 5:
    #   column = 0
    #   row += 1
    #  paste the image at (column*im_width, row*im_height)
    #  column += 1
    for i, card in enumerate(pack):
        if column == 5:
            column = 0
            row += 1
        uri = re.sub(
            "\?\d+$",
            "",
            card["card_faces"][0]["image_uris"]["small"] if "card_faces" in card.keys() and "adventure" != card["layout"] and "split" != card["layout"] else card["image_uris"]["small"],
        )
        resp = requests.get(uri, stream=True)
        new_im = Image.open(io.BytesIO(resp.content))
        if i in foils:
            new_im.paste(foil_image, (0, 0), foil_image)
        image_composite.paste(new_im, (column * im_width, row * im_height))
        new_im.close()
        column += 1
    f = io.BytesIO()
    image_composite.save(f, "png")
    f.seek(0)
    return f
