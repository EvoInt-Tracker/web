from Publication import publications, Publication, get_keywords_from_csv
from Vikus_writer import create_data_csv, read_data_csv
from Year import years, Year
from urllib.request import urlopen
import urllib.parse
from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup
from pathlib import Path

from pdf2image import convert_from_path
from urllib.error import HTTPError




def parse_title(title):
    title = title.replace('\n', ' ')
    title = title.replace('\t', ' ')
    title = title.replace('  ', ' ')
    title = title.strip()
    return title


def next_pub_id():
    ids = [int(pub_id) for pub_id in publications.keys()]
    ids.sort()
    result = str(ids[-1] + 1) if len(ids) > 0 else '0'
    return result.zfill(4)


def download(pub):
    # check if file already downloaded
    if Path(pub.path_to_pdf).is_file():
        return
    try:
        print(f'Downloading Publication "{pub.title}" \n\tfrom {pub.origin_path}\n')
        response = urlopen(pub.origin_path)
        # TODO: path_to_pdf has to start at data/..., so add vikus-viewer/ here
        file = open(pub.path_to_pdf, 'wb')
        file.write(response.read())
        file.close()
    except HTTPError:
        print("error writing file: " + pub.origin_path)
        pass

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
        desired_year = str(desired_year)
        os.makedirs(base_pdf_path + desired_year, exist_ok=True)
        year = years[desired_year] if desired_year in years.keys() else Year(desired_year)

        file_links = []
        year_url = urllib.parse.urljoin(base_url, str(year.year))
        response = urlopen(year_url)  # opens the URL
        page_source = response.read()
        soup = BeautifulSoup(page_source, 'html.parser')
        for link in soup.find_all('a'):
            current_link = link.get('href')
            if "www.ijcai.org" not in current_link:
                current_link = urllib.parse.urljoin("https://www.ijcai.org", current_link)
            if current_link.endswith('.pdf') and current_link not in file_links:
                file_links.append(urllib.parse.urljoin(year_url, current_link))

                if not urlparse(current_link).scheme:
                    current_link = 'https://' + current_link

                pub_id = next_pub_id()
                title = parse_title(link.text)
                path_to_pdf = base_pdf_path + str(year.year) + '/' + str(pub_id) + '.pdf'
                print(f'{year.year}:')
                print(f'Creating Publication_Object "{title}"')
                publication = Publication(pub_id=pub_id,
                                          title=title,
                                          year=year.year,
                                          origin_path=current_link,
                                          path_to_pdf=path_to_pdf)

                download(publication)

                # TODO: new Method 'add_to_data_csv(publication)'
                create_data_csv(publications)


def pdf_to_thumbnail(dct):
    for publication in dct.values():
        path = Path(publication.path_to_pdf)
        output_path = Path('data/thumbnails/' + str(publication.id) + '.png')
        if path.is_file() and not output_path.is_file():
            print(f'Creating Thumbnail for Publication "{publication.title}"')
            page = convert_from_path(path, 200, first_page=1, last_page=1)
            page[0].save('data/thumbnails/' + str(publication.id) + '.png', 'PNG')


def create_vikus_textures_and_sprites():
    os.system("node ../vikus-viewer-script/bin/textures 'data/thumbnails/*.png' --output '../vikus-viewer/data/images'")


# download_from_single_volume_years()

read_data_csv()
# create_data_csv(publications)
# pdf_to_thumbnail(publications)
# create_vikus_textures_and_sprites()

# get_keywords_from_csv()
for publication in publications.values():
    print(publication.id)
    fulltext = publication.fulltext()
    publication.set_keywords(fulltext)
create_data_csv(publications)
