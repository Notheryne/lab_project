import os


# print(os.listdir("../frontend/pages"))

menu_path = "../frontend/menu/"
with open(menu_path + "menu.html", 'r') as html_file:
    menu_html = html_file.read()

with open(menu_path + "menu.css", 'r') as css_file:
    menu_css = css_file.read()

pages_path = "../frontend/pages/"
styles_path = "../frontend/pages/styles/"

pages = [page for page in os.listdir(pages_path) if page.endswith('.html')]
pages = [page.replace('.html', '') for page in pages]
ignore_pages = []
pages = [page for page in pages if page not in ignore_pages]


print(pages)
for page in pages:
    css_path = styles_path + page + '.css'
    rel_css_path = 'styles/' + page + '.css'
    html_path = pages_path + page + '.html'

    with open(html_path, 'r') as html_file:
        html = html_file.read()

    with open(css_path, 'r') as css_file:
        css = css_file.read()

