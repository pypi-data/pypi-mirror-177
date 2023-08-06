# Indonesia Latest Quake Report
This package will get the latest earthquake report from BMKG

## HOW IT WORK
This package will scrape from (BMKG)(https://bmkg.go.id)

This package will use BeautifulSoup4 and Requests

## HOW TO USE

    import gempa_terkini

    if __name__ == '__main__':
        result = gempa_terkini.ekstraksi_data()
        gempa_terkini.tampilkan_data(result)

Dont forget to install BeautifulSoup4 and Requests to make sure this package working 