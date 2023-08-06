import requests
from bs4 import BeautifulSoup


class Berita:  # class
    def __init__(self, description):  # Methode
        self.description = description
        self.result = None

    def tampilkan_keterangan(self):
        print('News:', self.description)

    def scraping_data(self):
        print('Not yet implemented')

    def tampilkan_data(self):
        print('Not yet implemented')

    def run(self):
        self.tampilkan_keterangan()
        self.scraping_data()
        self.tampilkan_data()


class NewsEarhquake(Berita):
    def __init__(self):
        super(NewsEarhquake, self).__init__('Latest earthquake in Indonesia - BMGK.go.id')

    def scraping_data(self):
        try:
            content = requests.get('https://www.bmkg.go.id/')
        except Exception:
            return None
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'html.parser')
            page = soup.find('span', {'class': 'waktu'})
            page = page.text.split(', ')
            tanggal = page[0]
            waktu = page[1]

            page = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            page = page.findChildren('li')

            i = 0
            magnitudo = None
            kedalaman = None
            ls = None
            bt = None
            lokasi = None
            dirasakan = None

            for res in page:
                if i == 1:
                    magnitudo = res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    dirasakan = res.text
                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitudo'] = magnitudo
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print('Tidak menemukan data gempa terkini')
            return
        print("Gempa terakhir berdasarkan BMKG")
        print(f"Tanggal {self.result['tanggal']}")
        print(f"waktu {self.result['waktu']}")
        print(f"Magnitudo {self.result['magnitudo']}")
        print(f"Kedalaman {self.result['kedalaman']}")
        print(f"koordinat: ls= {self.result['koordinat']['ls']} bt= {self.result['koordinat']['bt']}")
        print(f"Lokasi {self.result['lokasi']}")
        print(f"{self.result['dirasakan']}")


class NewsTrending(Berita):
    def __init__(self):
        super(NewsTrending, self).__init__('Latest popular news in Indonesia - Detik.com')

    def scraping_data(self):
        try:
            page = requests.get('http://detik.com')
        except Exception:
            return None
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')

            times = soup.find('div', {'class': 'box cb-mostpop'})
            time = times.findChildren('div', {'class': 'media__date'})

            i = 0
            time_one = None
            time_two = None
            time_three = None
            time_four = None
            time_five = None

            for upload in time:
                if i == 0:
                    time = upload.text.split(' | ')
                    time_one = time[1]
                if i == 1:
                    time = upload.text.split(' | ')
                    time_two = time[1]
                if i == 2:
                    time = upload.text.split(' | ')
                    time_three = time[1]
                if i == 3:
                    time = upload.text.split(' | ')
                    time_four = time[1]
                if i == 4:
                    time = upload.text.split(' | ')
                    time_five = time[1]
                i += 1

            first_news = soup.find('a', {'dtr-evt': 'box artikel terpopuler', 'dtr-idx': '1'})
            first_news = first_news.text.strip()

            second_news = soup.find('a', {'dtr-evt': 'box artikel terpopuler', 'dtr-idx': '2'})
            second_news = second_news.text.strip()

            third_news = soup.find('a', {'dtr-evt': 'box artikel terpopuler', 'dtr-idx': '3'})
            third_news = third_news.text.strip()

            fourth_news = soup.find('a', {'dtr-evt': 'box artikel terpopuler', 'dtr-idx': '4'})
            fourth_news = fourth_news.text.strip()

            fifth_news = soup.find('a', {'dtr-evt': 'box artikel terpopuler', 'dtr-idx': '5'})
            fifth_news = fifth_news.text.strip()

            hasil = dict()
            hasil['pertama'] = {
                'first_news': first_news,
                'time_one': time_one
            }
            hasil['kedua'] = {
                'second_news': second_news,
                'time_two': time_two
            }
            hasil['ketiga'] = {
                'third_news': third_news,
                'time_three': time_three
            }
            hasil['keempat'] = {
                'fourth_news': fourth_news,
                'time_four': time_four
            }
            hasil['kelima'] = {
                'fifth_news': fifth_news,
                'time_five': time_five
            }
            self.result = hasil
        else:
            return None

    def tampilkan_data(self):
        if self.result is None:
            print('Tidak dapat menemukan data berita terkini')
            return None
        print(f"#1. {self.result['pertama']['first_news']}.\ndiupload : {self.result['pertama']['time_one']}")
        print(f"#2. {self.result['kedua']['second_news']}.\ndiupload : {self.result['kedua']['time_two']}")
        print(f"#3. {self.result['ketiga']['third_news']}.\ndiupload : {self.result['ketiga']['time_three']}")
        print(f"#4. {self.result['keempat']['fourth_news']}.\ndiupload : {self.result['keempat']['time_four']}")
        print(f"#5. {self.result['kelima']['fifth_news']}.\ndiupload : {self.result['kelima']['time_five']}")


if __name__ == "__main__":
    news = NewsEarhquake()
    news.run()
