import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        title = soup.find('title')
        print(title.string)
        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        x = 0
        tanggal = None
        waktu = None
        magnitudo = None
        ls = None
        bt = None
        kedalaman = None
        lokasi = None
        dirasakan = None

        for res in result:
            if x == 0:
                waktu = res.text.split(',')
                tanggal = waktu[0]
                waktu = waktu[1]
            elif x == 1:
                magnitudo = res.text
            elif x == 2:
                kedalaman = res.text
            elif x == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif x == 4:
                lokasi = res.text
            elif x == 5:
                dirasakan = res.text
            x = x + 1
        hasil = dict()
        hasil['Tanggal'] = tanggal
        hasil['Waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Tidak Bisa Menampilkan Data")
        return
    print('Gempa terakhir berdasarkan BMKG')
    print(f"Tanggal {result['Tanggal']}")
    print(f"Waktu {result['Waktu']}")
    print(f"Magnitudo {result['magnitudo']}")
    print(f"Kedalaman {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi {result['lokasi']}")
    print(f"Dirasakan {result['dirasakan']}")

if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)
