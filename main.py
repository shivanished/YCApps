from scraper import create_dataframe

yc_company_directory_url = "https://www.ycombinator.com/companies?batch=W24&batch=S23&batch=W23&batch=S22&batch=W22&batch=S21&batch=W21&regions=United%20States%20of%20America&tags=Artificial%20Intelligence&tags=SaaS&team_size=%5B%225%22%2C%2225%22%5D"

def main(url):
    df = create_dataframe(url)
    print(df["Company Website"].head()) 

main(yc_company_directory_url)