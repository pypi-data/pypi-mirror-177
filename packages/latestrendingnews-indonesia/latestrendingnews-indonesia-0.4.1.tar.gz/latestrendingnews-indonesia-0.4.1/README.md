# latest trending news
This package will display the latest trending news data taken from detik.com
## HOW IT WORK?
This package will scrape data from [detikcom](https://www.detik.com) to display the latest most popular news in Indonesia. This package use BeautifulSoup4 and request to  produce output in the form of JSON which is ready to be used in web and mobile applications

## HOW TO USE
```
from beritapopuler import NewsTrending

if __name__ == "__main__":
    berita_populer = NewsTrending()
    berita_populer.run()
```

## Author
Fauzi Kurniawan
