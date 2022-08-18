#!/usr/bin/python3

import glob
import os

def html_header(relative_adjustment = ""):
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Remodel</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
    <link rel="stylesheet" href="{}css/style.css">
</head>
<body>
""".format(relative_adjustment)

def html_footer(relative_adjustment = ""):
    return """
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>
    <script src="{}js/gallery.js"></script>

</body>
</html>
""".format(relative_adjustment)

def section_html(section_title, image_paths):
    items_html = ["""
                            <div class="gallery-item item-3x4">
                                <img class="thumb placeholder" src="{}" data-src="{}">
                            </div>
""".format(path, path) for path in image_paths]

    section_html = """
    <section>
        <b>{}</b>
        <div class="rt-container">
            <div class="col-rt-12">
                <div class="Scriptcontent">
                    <section>
                        <div class="gallery">
{}
                        </div>
                    </section>
                </div>
            </div>
        </div>
    </section>
""".format(section_title, "\n".join(items_html))
    return section_html

def grouped_photos():
    photo_groups = {}
    for path in sorted(os.listdir("./photos"), reverse=True):
        if path == ".DS_Store":
            continue

        photo_groups[path] = sorted([image for image in glob.glob("./photos/" + path + "/" + "*.png")])
    return photo_groups

def write_html(path, html_list):
    file_handler = open(path, "w")
    file_handler.write("\n".join(html_list))
    file_handler.close()

###############################################################################
# Generate groups of photos
###############################################################################

photo_groups = grouped_photos()

###############################################################################
# Write main `index.html`
###############################################################################

write_html(
    path = "index.html",
    html_list = [html_header()] + [section_html(date, images) for date, images in photo_groups.items()] + [html_footer()]
)

###############################################################################
# Write each section's separate `index.html`
###############################################################################

for date, images in photo_groups.items():
    html_dir = os.path.dirname(images[0])

    html = section_html(date, [os.path.basename(file_path) for file_path in images])

    write_html(
        path = "{}/index.html".format(html_dir),
        html_list = [
            html_header(relative_adjustment = "../../"),
            html,
            html_footer(relative_adjustment = "../../"),
        ]
    )
