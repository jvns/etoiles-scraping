from bs4 import BeautifulSoup
import glob
from datetime import datetime, timezone, timedelta
from ics import Calendar, Event


def scrape(filename):
    with open(filename) as file:
        soup = BeautifulSoup(file, "html.parser")
    # projection_grille_dateheure
    date_time = soup.find("p", class_="projection_grille_dateheure")
    assert date_time, "Could not find date and time"
    # convert date to number -- 19 July 2024 at 19h30
    date_time = datetime.strptime(date_time.text, "%d %B %Y at %Hh%M")
    date_time = date_time.replace(tzinfo=timezone.utc)
    date_time = date_time + timedelta(hours=4)

    location = soup.find("p", class_="projection_grille_lieu")
    location = location.text

    title = soup.find("h2", class_="film-title").text

    # <link rel="alternate" href="https://cinemasouslesetoiles.org/en/film/farming-the-revolution_en/" hreflang="en" />

    link = soup.find("link", rel="alternate", hreflang="en")
    link = link["href"]
    return date_time, location, title, link


def main():
    cal = Calendar()
    for filename in glob.glob("html/*"):
        date, location, name, link = scrape(filename)
        e = Event(
            begin=date,
            end=date + timedelta(hours=2),
            location=location,
            name=name,
            description=link,
        )
        cal.events.add(e)
    with open("etoiles.ics", "w") as my_file:
        my_file.writelines(cal.serialize_iter())


if __name__ == "__main__":
    main()
