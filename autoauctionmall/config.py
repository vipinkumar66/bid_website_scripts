from urllib.parse import quote, unquote_plus
import datetime

csv_folder_name = f"AutoAuctionMallCSV_{datetime.datetime.now().strftime('%H_%M_%S')}"

variables = {
    "website": "https://www.autoauctionmall.com",
    "api-url": "https://9vmz5hxzr0-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla"
               "%20JavaScript%20(lite)%203.30.0%3Breact-instantsearch%205.3.1%3BJS%20Helper%202.26.1&x-algolia"
               "-application-id=9VMZ5HXZR0&x-algolia-api-key=a690ed2c1bfe7a3d4d4c2dfc124fb075",
    "headers": {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.autoauctionmall.com',
        'Referer': 'https://www.autoauctionmall.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    },
    "params": "query=&hitsPerPage=60&maxValuesPerFacet=100&page={page}&attributesToRetrieve=%5B%22buyNow%22%2C"
              "%22condition%22%2C%22current_bid%22%2C%22price%22%2C%22image%22%2C%22location_city_state"
              "%22%2C%22make%22%2C%22model%22%2C%22name%22%2C%22normalizedTitle%22%2C%22objectID%22%2C"
              "%22odometer%22%2C%22slug%22%2C%22start_date%22%2C%22start_date_timestamp%22%2C%22title%22"
              "%2C%22titleNotAllowedIn%22%2C%22vehicleStatus%22%2C%22year%22%2C%22enhancements%22%5D"
              "&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight"
              "-0000000000%3E&facets=%5B%22vehicleStatus%22%2C%22vehicleCategories.name%22%2C"
              "%22locationSlug%22%2C%22bodyStyle%22%2C%22year%22%2C%22make.name%22%2C%22model.name%22%2C"
              "%22odometer%22%2C%22extFilters%22%2C%22buyNow%22%2C%22current_bid%22%2C%22normalizedTitle"
              "%22%2C%22damage%22%2C%22vehicleType%22%5D&tagFilters=&facetFilters=%5B%5B%22vehicleStatus"
              "%3Aactive%22%2C%22vehicleStatus%3Aactive_no_date%22%2C%22vehicleStatus%3Alive%22%2C"
              "%22vehicleStatus%3Apre-live%22%2C%22vehicleStatus%3Aprivate%22%5D%5D&numericFilters=%5B"
              "%22year%3E%3D{from_year}%22%2C%22year%3C%3D{to_year}%22%5D ",
    "data": {
        "requests": [
            {
                "indexName": "prod_aam_auctions",
                "params": ""
            }
        ]
    }
}

if __name__ == "__main__":
    print(unquote_plus(variables['params']))
