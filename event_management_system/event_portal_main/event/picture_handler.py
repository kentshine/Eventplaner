import os
from PIL import Image
from flask import url_for,current_app


def add_event_banner(banner,event_name,height,width):
    filename = banner.filename
    ext_type = filename.split(".")[-1]
    storage_filename = str(event_name) + "." + ext_type

    filepath = os.path.join(current_app.root_path , "static\\event_banner" , storage_filename)

    output_size =(height,width)

    pic = Image.open(banner)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename