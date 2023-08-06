# The Latest News Indonesia
This package will display various news in Indenesia
## HOW IT WORK?
This package will scrape data from [detikcom](https://www.detik.com) and [bmkg.go.id](https://www.bmkg.go.id/) to display the latest various news in Indonesia. This package use BeautifulSoup4 and request to  produce output in the form of JSON which is ready to be used in web and mobile applications

## HOW TO USE
```
from berita_indonesia import NewsTrending

if __name__ == "__main__":
    berita_populer = NewsTrending()
    berita_populer.run()
```

## Author
Fauzi Kurniawan