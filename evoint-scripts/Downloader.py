from Publication import publications, Publication
from Year import years, Year
from urllib.request import urlopen
import urllib.parse
import os
from bs4 import BeautifulSoup


def next_pub_id():
    ids = [pub_id for pub_id in publications.keys()]
    ids.sort()
    result = str(ids[-1] + 1)
    return result.zfill(4)


def download(publication):
    # try:
    response = urlopen(publication.origin_path)
    file = open(str(publication.year) + "_IJCAI_" + str(publication.id) + ".pdf", 'wb')
    file.write(response.read())
    file.close()
    # except :
    #     print("error writing file: " + url)
    #     pass

    # folder_name = str(year) + "_IJCAI"
    # os.makedirs(folder_name)
    # os.chdir(os.getcwd() + "/" + folder_name)
    #
    #
    # os.chdir("..")


# Single Volume: 1969 - 1975 & 2003 - ...
def download_from_single_volume_years(desired_years=None):
    if desired_years is None:
        desired_years = list(range(1969, 1977, 2)) + list(range(2003, 2017, 2)) + list(range(2016, 2021))

    base_pdf_path = '../vikus-viewer/data/fulltext/pdf/'
    base_url = "https://www.ijcai.org/Proceedings/"

    for desired_year in desired_years:
        os.makedirs(base_pdf_path + desired_year, exist_ok=True)
        year = years[desired_year] if desired_year in years else Year(desired_year)

        file_links = []
        year_url = base_url + str(year) + "/"
        response = urlopen(year_url)  # opens the URL
        page_source = response.read()
        soup = BeautifulSoup(page_source, 'html.parser')
        for link in soup.find_all('a'):
            current_link = link.get('href')
            if current_link.endswith('.pdf') and current_link not in file_links:
                file_links.append(urllib.parse.urljoin(year_url, current_link))

                pub_id = next_pub_id()
                title = link.text
                path_to_pdf = base_pdf_path + '/' + str(year.year) + '/' + str(pub_id) + '.pdf'

                publication = Publication(pub_id=pub_id,
                                          title=title,
                                          year=year,
                                          origin_path=current_link,
                                          path_to_pdf=path_to_pdf)

                download(publication)

