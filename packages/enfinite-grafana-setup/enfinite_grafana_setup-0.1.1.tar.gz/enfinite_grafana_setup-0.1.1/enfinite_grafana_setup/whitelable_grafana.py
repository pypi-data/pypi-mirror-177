import bs4
import requests
import os

index_file = "/usr/share/grafana/public/views/index.html"


def change_title_icon_footer(app_title, fav_icon, app_icon):
    # load the file
    with open(index_file) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, features="html.parser")

    # Edit Title
    title = soup.select_one("title")
    if app_title:
        if not title:
            title = soup.new_tag("title")
        title.string = app_title

    # Edit main icon

    # download icon
    os.system(f"wget {app_icon}")

    # rename original icon
    os.system(
        "mv /usr/share/grafana/public/img/grafana_icon.svg /usr/share/grafana/public/img/grafana_icon_original.svg"
    )
    os.system("mv ./enfinite_icon.svg /usr/share/grafana/public/img/grafana_icon.svg")
    # Edit icon
    icon = soup.select_one('link[rel="icon"]')
    if fav_icon:
        if not icon:
            icon = soup.new_tag("link", rel="icon", type="image/png", href=fav_icon)
        else:
            icon["href"] = fav_icon

    # Hide Footer
    style = soup.select_one("style")
    if style:
        if ".footer" not in str(style.string):
            style.string = str(style.string) + "\n      .footer {visibility: hidden}"

    # save the file again
    with open(index_file, "w") as outf:
        outf.write(str(soup))


def changes_in_jsfiles(login_url, title):
    login_page = requests.get(login_url)
    soup = bs4.BeautifulSoup(login_page.content, features="html.parser")
    js_files = []
    for script in soup.select("script"):
        if "src" in script.attrs.keys() and str(script["src"]).startswith(
            "public/build/"
        ):
            print(script)
            js_files.append("/usr/share/grafana/" + str(script["src"]))

    for js_file_loc in js_files:
        with open(js_file_loc, "r") as js_file_in:
            print(js_file_loc)
            new_file = []
            for line_ in js_file_in:
                while '(d,"AppTitle","Grafana")' in line_:
                    print("--------------")
                    print(line_, "\n")
                    print("xxxxxxxxxxxxxxx")
                    line_ = line_.replace(
                        '(d,"AppTitle","Grafana")', f'(d,"AppTitle","{title}")'
                    )
                    print(line_, "\n")
                    print("--------------")

                while '(d,"LoginTitle","Welcome to Grafana")' in line_:
                    print("--------------")
                    print(line_, "\n")
                    print("xxxxxxxxxxxxxxx")
                    line_ = line_.replace(
                        '(d,"LoginTitle","Welcome to Grafana")',
                        f'(d,"LoginTitle","Welcome to {title}")',
                    )
                    print(line_, "\n")
                    print("--------------")

                new_file.append(line_)
            # print(new_file)
        with open(js_file_loc, "w") as js_file_out:
            print(f"writing to: {js_file_loc}")
            js_file_out.writelines(new_file)
