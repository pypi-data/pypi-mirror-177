import os

app_login = os.getenv("LOGIN")
app_title = os.getenv("TITLE")
fav_icon = os.getenv("FAVICON")
app_icon = os.getenv("APPICON")

if __name__ == "__main__":
    print(
        f"App Title:{app_title}\nLogin page:{app_login}\nFav Icon:{fav_icon}\nApp Icon:{app_icon}"
    )
