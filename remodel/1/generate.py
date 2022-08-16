#!/usr/bin/python3

import glob
import os

html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>Remodel</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
"""

html_footer = """
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>
    <script src="js/gallery.js"></script>

</body>
</html>
"""

sections_html = []
for path in sorted(os.listdir("./photos"), reverse=True):
    if path == ".DS_Store":
        continue

    section_title = path

    items_html = ["""
                            <div class="gallery-item item-3x4">
                                <img class="thumb placeholder" src="{}" data-src="{}">
                            </div>
""".format(image, image) for image in glob.glob("./photos/" + path + "/" + "*.png")]

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
    sections_html.append(section_html)

file_handler = open("index.html", "w")
file_handler.write(html_header)
file_handler.write("\n".join(sections_html))
file_handler.write(html_footer)
file_handler.close()
