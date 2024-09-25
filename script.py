import datetime
from bs4 import BeautifulSoup
import requests

page = 0
form = "js"
halls = ["Southside", "Ike's", "The Globe", "The Spot"]
menu_string = "menuid-23-day"
pages = [requests.get("https://menus.sodexomyway.com/BiteMenu/Menu?menuId=16652&locationId=27747003&whereami=http://masondining.sodexomyway.com/dining-near-me/southside"), requests.get("https://menus.sodexomyway.com/BiteMenu/Menu?menuId=35763&locationId=27747017&whereami=http://masondining.sodexomyway.com/dining-near-me/ikes"), requests.get("https://menus.sodexomyway.com/BiteMenu/Menu?menuId=36397&locationId=27747052&whereami=http://masondining.sodexomyway.com/dining-near-me/the-globe"), requests.get("https://menus.sodexomyway.com/BiteMenu/Menu?menuId=32761&locationId=27747049&whereami=http://masondining.sodexomyway.com/dining-near-me/the-spot")]
soups = [BeautifulSoup(pages[0].text, "html.parser"), BeautifulSoup(pages[1].text, "html.parser"), BeautifulSoup(pages[2].text, "html.parser"), BeautifulSoup(pages[3].text, "html.parser")]

def init():
    generate_menu_string()
    for p in range(len(pages)):
        print(str(p) + ": " + halls[p])
        get_meals(p)


meals = []

def get_meals(p):
    # Use a breakpoint in the code line below to debug your script.
    print(pages[p].status_code)
    meals.append(halls[p])

    try:
        elems = soups[p].find(id=menu_string).find_all(class_="col-xs-9")

        for x in elems:
            meal = x.find_next(class_="get-nutritioncalculator")
            if meal.text != "Have A Nice Day":
                meals.append(meal.text)
                # print(meal.text)

    except:
        meals.append("No known meals for this dining hall.")

    for meal in meals:
        print(meal)

    print(form)
    if form == "html" or form == "both":
        format_html(meals)
    if form == "js" or form == "both":
        format_js(meals)


def format_html(meals):
    html = "<html><head><title>GMU Menu</title></head><body><p>(c) Zachary Henry, 2024<p><hr><p>"
    for meal in meals:
        if meal == "Southside" or meal == "Ike's" or meal == "The Globe" or meal == "The Spot":
            html = html + ("<br><b>" + meal + "</b><br>")
        else:
            if meal != "No known meals for this dining hall.":
                html = html + (meal + "<br>")
            else:
                html = html + ("<i>" + meal + "</i><br>")

    html = html + "</p><br><small>Last updated " + str(datetime.datetime.now()) + "</small></body></html>"

    # Edit File
    f = open("C:/Users/15713/Desktop/Personal/Server/gmumenu.html", "w")
    f.write(html)
    f.close()

    print("HTML Generated!")


def generate_menu_string():
    day = datetime.datetime.today().day
    print(str(day))
    menu_string = ("menuid-" + str(day) + "-day")
    print(menu_string)


def format_js(meals):
    js = "/* GMU Menu. (c) Zachary Henry, 2024 */ var menu = { southside: ["
    for meal in meals:
        if meal == "Ike's" or meal == "The Globe" or meal == "The Spot":
            if meal == "Ike's": js = js + "], ikes: ["
            if meal == "The Globe": js = js + "], globe: ["
            if meal == "The Spot": js = js + "], spot: ["
        else:
            js = js + ('"' + meal + '", ')

    js = js + '], lu: "' + str(datetime.datetime.now()) + '"};'

    # File Handling
    f = open("C:/Users/15713/Desktop/Personal/Server/gmumenu.js", "w")
    f.write(js)
    f.close()

    print("JS Generated!")


init()