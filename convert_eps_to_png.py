#run this file from current directory 
from PIL import Image
import glob

#this is the very first thing to do
# import os, subprocess, shutil
# #see is gs is avaible
# if shutil.which("gs") is None:
#    print("GhostScrip is not avaible, search for it")
#    try:
#       gs = subprocess.Popen(["which","gs"],stdout=subprocess.PIPE)
#       gs_path = gs.stdout.read()
#       gs_path = gs_path.decode() if isinstance(gs_path,bytes) else gs_path
#       print("GhostScrip found in",gs_path)
#       os.environ["PATH"] += ":"+ os.path.dirname(gs_path)
#    except Exception as e:
#       raise Warning("GhostScrip not found, this program may fail")

# del subprocess
# del shutil

import os
print("## Addind gs to environ ##", os.environ["PATH"] )
os.environ["PATH"] += ":/usr/local/bin" 
print("## Addind gs to environ ##", os.environ["PATH"] )
os.environ["PATH"] += "Library/usr/local/bin" 
os.environ["PATH"] = "/usr/local/bin:" + os.environ["PATH"]
os.environ["PATH"] = "Library/usr/local/bin:" + os.environ["PATH"]
# import os
# All files and directories ending with .txt and that don't begin with a dot:
# cwd = os.getcwd()
# print(cwd)




epsFiles = glob.glob(f"fractals/*.eps")

TARGET_BOUNDS = (1024, 1024)

# Load the EPS at 10 times whatever size Pillow thinks it should be
# (Experimentaton suggests that scale=1 means 72 DPI but that would
#  make 600 DPI scale=8⅓ and Pillow requires an integer)

for file in epsFiles:
    # 
    print(file)
    # image_eps = file
    # im = Image.open(file)
    # print(im)
    # fig = im.convert('RGBA')
    image_png= file.replace("eps", "png")
    # print(image_png)
    # fig.save(image_png, lossless = True)
    pic = Image.open(file)
    pic.load(scale=10)

    # Ensure scaling can anti-alias by converting 1-bit or paletted images
    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")

    # Calculate the new size, preserving the aspect ratio
    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                TARGET_BOUNDS[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

    # Resize to fit the target size
    pic = pic.resize(new_size, Image.ANTIALIAS)

    # Save to PNG
    image_png= file.replace("eps", "png")
# print()
    pic.save(file.split('/')[-1])
