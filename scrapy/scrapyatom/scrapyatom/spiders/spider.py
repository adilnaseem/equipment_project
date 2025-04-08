import scrapy
from bs4 import BeautifulSoup as bs4

class WsbaSpider(scrapy.Spider):
    name = "wsba_spider"  # Name of the spider
    start_urls = [
        "https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&LicenseType=Lawyer&EligibleToPractice=Y&Status=Active&Page=0"
    ]

    def parse(self, response):
        # Parse the initial page with BeautifulSoup
        soup0 = bs4(response.body, 'html.parser')

        # Extract rows from the search results table
        trs0 = soup0.find('table', {'class': "search-results"}).find_all('tr', {'class': "grid-row"})

        # Process only the first row for demonstration (you can loop through all rows if needed)
        for tr0 in trs0[0:1]:
            # Extract the onclick attribute to get the detail page URL
            qw = tr0['onclick']
            detail_url = 'https://www.mywsba.org/PersonifyEbusiness/' + qw.split("'")[1]

            # Follow the detail page URL
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # Parse the detail page with BeautifulSoup
        soup = bs4(response.body, 'html.parser')

        # Initialize a dictionary to store the data
        data = {}

        # Extract the name
        name = soup.find('span', {'class': "name"}).get_text(separator="", strip=True)
        data['Name'] = name

        # Extract data from the table rows
        trs = soup.find('div', class_='center mobile-way').find_all('tr')
        for tr in trs:
            aa = tr.get_text(strip=True)
            key = aa.split(':')[0]
            value = ', '.join(aa.split(':')[1:])
            data[key] = value

        # Extract "Member of the following groups" information
        asd = soup.select(':-soup-contains("Member of the following groups")')[-3].get_text(
            separator="", strip=True).split(':')[1:]
        member = 'Member of the following groups:' + ', '.join(asd)
        data[member.split(':')[0]] = ', '.join(member.split(':')[1:])

        # Extract "Disciplinary History" information
        Disciplinary_History = 'Disciplinary History:' + soup.select(':-soup-contains("Disciplinary History")')[
            -2].find('p').get_text(separator="", strip=True)
        data[Disciplinary_History.split(':')[0]] = ', '.join(Disciplinary_History.split(':')[1:])

        # Yield the extracted data
        yield data