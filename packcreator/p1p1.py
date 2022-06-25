from PIL import Image
from .p_caller import get_p1p1_v3

# stringio file object from requests from image uri
# image.open() it
# push it to array
# go 5 wide
# make a large image canvas
# width = min(length of pack, 5) * im_width
# height = length of pack // 5 * im_height
#  if length of pack % 5 == 0
# else length of pack // 5 + 1 * im_height

# im_c = Image.new(im.mode, (im.width + im2.width, max(im.height, im2.height)))
# im_c.paste(im, (0, 0))
# im_c.paste(im2, (im.width, 0))
# im_c.save('new_image.png', quality=50)
# im_c.show()