import json
from collections import OrderedDict

publications = OrderedDict()


class Publication:
    def __init__(self, pub_id, title, year, origin_path, path_to_pdf):
        self.id = pub_id
        self.title = title
        self.year = year
        self.origin_path = origin_path
        self.path_to_pdf = path_to_pdf

        self.add_to_publications()

    def add_to_publications(self):
        publications[self.id] = self


def save_backup():
    with open('publications_backup.json', 'w') as fp:
        for publication in publications.values():
            json.dump(publication.__dict__, fp)
            fp.write("\n")


def restore_backup():
    with open('publications_backup.json', 'r') as fp:
        lines = fp.read().splitlines()
        for line in lines:
            temp = json.loads(line)

            Publication(pub_id=temp['id'],
                        title=temp['title'],
                        year=temp['year'],
                        origin_path=temp['origin_path'],
                        path_to_pdf=temp['path_to_pdf'])


def sample():
    Publication('0001', 'title', '1993', 'origin_path_oh', 'path to some pdf')
    Publication('0005', 't2itle', '12993', 'or2igin_path_oh', 'pa2th to some pdf')


sample()
# save_backup()
restore_backup()

print(publications)
print(publications['0005'].title)
