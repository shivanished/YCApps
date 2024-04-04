for index, row in df.iterrows():
    url = row['Link']
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page = soup.find('div', class_="mx-auto max-w-ycdc-page")

        company_name = page.find('h1', class_="font-extralight")
        df.at[index, 'Company'] = company_name.text.strip()

        content_section = page.find('section', class_="relative isolate z-0 border-retro-sectionBorder sm:pr-[13px] ycdcPlus:pr-0 pt-2 sm:pt-4 lg:pt-6 pb-2 sm:pb-4 lg:pb-6")
        content_paragraphs = content_section.find('section', class_="relative isolate z-0 border-retro-sectionBorder sm:pr-[13px] ycdcPlus:pr-0 pt-1 sm:pt-2 lg:pt-3 pb-1 sm:pb-2 lg:pb-3")
        full_content = content_paragraphs.find('p', class_="whitespace-pre-line")
        df.at[index, 'Explanation'] = full_content.text.strip()

        founders_paragraphs = page.find('div', class_="space-y-5")
        if founders_paragraphs:
            founders_names = founders_paragraphs.find_all('h3', class_="text-lg font-bold")
            founders_names_text = [tag.text.strip() for tag in founders_names]
            df.at[index, 'Founders_Names'] = founders_names_text

        website = page.find('div', cless_='group flex flex-row items-center px-3 leading-none text-linkColor ')
        website_url = website.find('a').get('href')
        print(website_url)
        break