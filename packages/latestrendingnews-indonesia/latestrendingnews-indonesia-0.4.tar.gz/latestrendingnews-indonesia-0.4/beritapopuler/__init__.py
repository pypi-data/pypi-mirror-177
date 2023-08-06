import requests
from bs4 import BeautifulSoup


class NewsTrending:
    def __init__(self):
        self.description = 'Latest Popular News - Detik.com'
        self.result = None

    def ekstraksi_data(self):
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

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()


if __name__ == "__main__":
    berita_populer = NewsTrending()
    print(f'News : ', berita_populer.description)
    berita_populer.run()
