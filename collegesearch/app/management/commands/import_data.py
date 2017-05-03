import csv
import os
import pandas as pd
import zipfile

from io import TextIOWrapper

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from app.models import Institution, Scores, Tuition


class Command(BaseCommand):
    help = 'Imports the data into db'

    def __init__(self):
        super().__init__(self)
        self.datasets = {
            'education': ('HD2015', 'ADM2015', 'IC2015_AY')
        }

    def handle_characteristics(self, reader):
        try:
            for row in reader:
                try:
                    location = Point(float(row[66]), float(row[67]))
                except ValueError:
                    location = Point(-180, 0)

                institution = Institution.objects.create(unitid = row[0],
                                                         name = row[1],
                                                         address = row[2],
                                                         city = row[3],
                                                         state = row[4],
                                                         location_region = int(row[7]),
                                                         ein = row[12],
                                                         web_address = row[14],
                                                         admission_url = row[15],
                                                         financial_aid_url = row[16],
                                                         application_url = row[17],
                                                         net_price_url = row[18],
                                                         sector = row[22],
                                                         level = row[23],
                                                         control = row[24],
                                                         highest_award = int(row[25]),
                                                         locale = int(row[33]),
                                                         enrollment = row[55],
                                                         system_type = int(row[60]),
                                                         system_name = row[61],
                                                         location = location)
        except UnicodeDecodeError as e:
            print(e)

    def handle_tuition(self, reader):
        pass

    def handle_scores(self, reader):
        pass

    def handle(self, *args, **options):
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(current_path, '../../../data')
        for k, v in self.datasets.items():
            for dataset in v:
                path = os.path.join(dataset_path, k, '2015/{}.zip'.format(dataset))
                with zipfile.ZipFile(path) as z:
                    reader = csv.reader(TextIOWrapper(z.open('{}.csv'.format(dataset.lower()), mode = 'r'), encoding = 'latin-1'))
                    next(reader, None)

                    dataset = dataset.lower()

                    if dataset == 'hd2015':
                        self.handle_characteristics(reader)
                    # elif dataset == 'ic2015_ay':
                    #     self.handle_scores(reader)
                    # elif dataset == 'adm2015':
                    #     self.handle_tuition(reader)
