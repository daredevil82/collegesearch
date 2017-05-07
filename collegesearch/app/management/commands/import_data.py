import csv
import os
import zipfile

from io import TextIOWrapper

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from app.models import AliasTitle, Institution, Admissions, Tuition, CIP, Completions


class Command(BaseCommand):
    help = 'Imports the data into db'

    def __init__(self):
        super().__init__(self)
        self.datasets = {
            'education': ('HD2015', 'ADM2015', 'IC2015_AY', 'C2015_A')
        }

    def handle_characteristics(self, reader):
        print('Importing institution data')

        header = next(reader)

        required_columns = ('UNITID', 'INSTNM', 'ADDR', 'CITY', 'STABBR', 'OBEREG', 'EIN', 'WEBADDR',
                            'ADMINURL', 'FAIDURL', 'APPLURL', 'NPRICURL', 'SECTOR', 'ICLEVEL', 'CONTROL',
                            'HLOFFER', 'LOCALE','F1SYSTYP', 'F1SYSNAM', 'LONGITUD', 'LATITUDE')
        header_indices = []

        for idx, val in enumerate(header):
            if val in required_columns:
                header_indices.append(idx)

        try:
            for idx, row in enumerate(reader):
                try:
                    location = Point(float(row[header_indices[19]]), float(row[header_indices[20]]))
                except ValueError:
                    print('[{}] institution has an error converting latitude or longitude'.format(row[0]))
                    location = Point(-180, 0)

                institution = Institution.objects.create(unitid = self.safe_cast(row[header_indices[0]]),
                                                         name = row[header_indices[1]],
                                                         address = row[header_indices[2]],
                                                         city = row[header_indices[3]],
                                                         state = row[header_indices[4]],
                                                         location_region = self.safe_cast(row[header_indices[5]]),
                                                         ein = row[header_indices[6]],
                                                         web_address = row[header_indices[7]],
                                                         admission_url = row[header_indices[8]],
                                                         financial_aid_url = row[header_indices[9]],
                                                         application_url = row[header_indices[10]],
                                                         net_price_url = row[header_indices[11]],
                                                         sector = self.safe_cast(row[header_indices[12]]),
                                                         level = self.safe_cast(row[header_indices[13]]),
                                                         control = self.safe_cast(row[header_indices[14]]),
                                                         highest_award = self.safe_cast(self.safe_cast(row[header_indices[15]])),
                                                         locale = self.safe_cast(row[header_indices[16]]),
                                                         system_type = self.safe_cast(row[header_indices[17]]),
                                                         system_name = row[header_indices[18]],
                                                         location = location)

                if (idx + 1) % 100 == 0:
                    print('[{}] institutions inserted'.format(idx + 1))

        except UnicodeDecodeError as e:
            print(e)

    def handle_tuition(self, reader):
        print('Importing tuition data')
        header = next(reader)

        shared_columns      = ('CHG4AY1', 'CHG4AY2', 'CHG4AY3', 'CHG5AY1', 'CHG5AY2', 'CHG5AY3')
        district_columns    = ('TUITION1', 'FEE1', 'HRCHG1', 'CHG1AY1', 'CHG1AY2', 'CHG1AY3')
        in_state_columns    = ('TUITION2', 'FEE2', 'HRCHG2', 'CHG2AY1', 'CHG2AY2', 'CHG2AY3')
        out_state_columns   = ('TUITION3', 'FEE3', 'HRCHG3', 'CHG3AY1', 'CHG3AY2', 'CHG3AY3')

        shared_indices = []
        district_indices = []
        in_state_indices = []
        out_state_indices = []


        for idx, val in enumerate(header):
            if val in district_columns:
                district_indices.append(idx)
            if val in in_state_columns:
                in_state_indices.append(idx)
            if val in out_state_columns:
                out_state_indices.append(idx)
            if val in shared_columns:
                shared_indices.append(idx)

        try:
            for idx, row in enumerate(reader):
                institution = Institution.objects.get(unitid = row[0])

                district_tuition = Tuition.objects.create(institution = institution,
                                                          tuition_class = 0,
                                                          cost = self.safe_cast(row[district_indices[0]]),
                                                          fees = self.safe_cast(row[district_indices[1]]),
                                                          credit_hour = self.safe_cast(row[district_indices[2]]),
                                                          academic_year_2013_cost = self.safe_cast(row[district_indices[3]]),
                                                          academic_year_2014_cost = self.safe_cast(row[district_indices[4]]),
                                                          academic_year_2015_cost = self.safe_cast(row[district_indices[5]]),
                                                          academic_year_2013_books = self.safe_cast(row[shared_indices[0]]),
                                                          academic_year_2014_books = self.safe_cast(row[shared_indices[1]]),
                                                          academic_year_2015_books = self.safe_cast(row[shared_indices[2]]),
                                                          academic_year_2013_board = self.safe_cast(row[shared_indices[3]]),
                                                          academic_year_2014_board = self.safe_cast(row[shared_indices[4]]),
                                                          academic_year_2015_board = self.safe_cast(row[shared_indices[5]]))

                in_state_tuition = Tuition.objects.create(institution = institution,
                                                          tuition_class = 1,
                                                          cost = self.safe_cast(row[in_state_indices[0]]),
                                                          fees = self.safe_cast(row[in_state_indices[1]]),
                                                          credit_hour = self.safe_cast(row[in_state_indices[2]]),
                                                          academic_year_2013_cost = self.safe_cast(row[in_state_indices[3]]),
                                                          academic_year_2014_cost = self.safe_cast(row[in_state_indices[4]]),
                                                          academic_year_2015_cost = self.safe_cast(row[in_state_indices[5]]),
                                                          academic_year_2013_books = self.safe_cast(row[shared_indices[0]]),
                                                          academic_year_2014_books = self.safe_cast(row[shared_indices[1]]),
                                                          academic_year_2015_books = self.safe_cast(row[shared_indices[2]]),
                                                          academic_year_2013_board = self.safe_cast(row[shared_indices[3]]),
                                                          academic_year_2014_board = self.safe_cast(row[shared_indices[4]]),
                                                          academic_year_2015_board = self.safe_cast(row[shared_indices[5]]))

                out_state_tuition = Tuition.objects.create(institution = institution,
                                                           tuition_class = 2,
                                                           cost = self.safe_cast(row[out_state_indices[0]]),
                                                           fees = self.safe_cast(row[out_state_indices[1]]),
                                                           credit_hour = self.safe_cast(row[out_state_indices[2]]),
                                                           academic_year_2013_cost = self.safe_cast(row[out_state_indices[3]]),
                                                           academic_year_2014_cost = self.safe_cast(row[out_state_indices[4]]),
                                                           academic_year_2015_cost = self.safe_cast(row[out_state_indices[5]]),
                                                           academic_year_2013_books = self.safe_cast(row[shared_indices[0]]),
                                                           academic_year_2014_books = self.safe_cast(row[shared_indices[1]]),
                                                           academic_year_2015_books = self.safe_cast(row[shared_indices[2]]),
                                                           academic_year_2013_board = self.safe_cast(row[shared_indices[3]]),
                                                           academic_year_2014_board = self.safe_cast(row[shared_indices[4]]),
                                                           academic_year_2015_board = self.safe_cast(row[shared_indices[5]]))

                if (idx + 1) % 100 == 0:
                    print('[{}] tuition rows processed'.format(idx + 1))

        except UnicodeDecodeError as e:
            print('Unicode Error')
            print(e)


    def handle_admissions(self, reader):
        print('Importing admissions data')

        header = next(reader)

        required_columns = ('APPLCN', 'APPLCNM', 'APPLCNW',
                            'ADMSSN', 'ADMSSNM', 'ADMSSNW',
                            'ENRLT', 'ENRLM', 'ENRLW',
                            'ENRLFT', 'ENRLFTM', 'ENRLFTW',
                            'ENRLPT', 'ENRLPTM', 'ENRLPTW',
                            'SATVR25', 'SATVR75', 'SATMT25', 'SATMT75', 'SATWR25', 'SATWR75',
                            'ACTCM25', 'ACTCM75', 'ACTEN25', 'ACTEN75', 'ACTMT25', 'ACTMT75', 'ACTWR25', 'ACTWR75 ')

        column_indices = []

        for idx, val in enumerate(header):
            if val in required_columns:
                column_indices.append(idx)

        try:
            for idx, row in enumerate(reader):
                institution = Institution.objects.get(unitid = self.safe_cast(row[0]))
                admissions = Admissions.objects.create(institution = institution,
                                                       total_applicants = self.safe_cast(row[column_indices[0]]),
                                                       male_applicants = self.safe_cast(row[column_indices[1]]),
                                                       female_applicants = self.safe_cast(row[column_indices[2]]),
                                                       total_admissions = self.safe_cast(row[column_indices[3]]),
                                                       male_admissions = self.safe_cast(row[column_indices[4]]),
                                                       female_admissions = self.safe_cast(row[column_indices[5]]),
                                                       total_enrollment = self.safe_cast(row[column_indices[6]]),
                                                       male_enrollment = self.safe_cast(row[column_indices[7]]),
                                                       female_enrollment = self.safe_cast(row[column_indices[8]]),
                                                       ft_enrollment = self.safe_cast(row[column_indices[9]]),
                                                       ft_male_enrollment = self.safe_cast(row[column_indices[10]]),
                                                       ft_female_enrollment = self.safe_cast(row[column_indices[11]]),
                                                       pt_enrollment = self.safe_cast(row[column_indices[12]]),
                                                       pt_male_enrollment = self.safe_cast(row[column_indices[13]]),
                                                       pt_female_enrollment = self.safe_cast(row[column_indices[14]]),
                                                       sat_reading_25 = self.safe_cast(row[column_indices[15]]),
                                                       sat_reading_75 = self.safe_cast(row[column_indices[16]]),
                                                       sat_math_25 = self.safe_cast(row[column_indices[17]]),
                                                       sat_math_75 = self.safe_cast(row[column_indices[18]]),
                                                       sat_writing_25 = self.safe_cast(row[column_indices[19]]),
                                                       sat_writing_75 = self.safe_cast(row[column_indices[20]]),
                                                       act_composite_25 = self.safe_cast(row[column_indices[21]]),
                                                       act_composite_75 = self.safe_cast(row[column_indices[22]]),
                                                       act_english_25 = self.safe_cast(row[column_indices[23]]),
                                                       act_english_75 = self.safe_cast(row[column_indices[24]]),
                                                       act_math_25 = self.safe_cast(row[column_indices[25]]),
                                                       act_math_75 = self.safe_cast(row[column_indices[26]]),
                                                       act_writing_25 = self.safe_cast(row[column_indices[27]]),
                                                       act_writing_75 = self.safe_cast(row[column_indices[28]]))

                if (idx + 1) % 100 == 0:
                    print('[{}] admission rows processed'.format(idx + 1))

        except UnicodeDecodeError as e:
            print('Unicode error')
            print(e)

    def handle_completions(self, reader):
        print('Importing completions data')
        next(reader)

        try:
            for idx, row in enumerate(reader):

                try:
                    institution = Institution.objects.get(unitid = self.safe_cast(row[0]))
                    cip = CIP.objects.get(cip_code = row[1])

                    completion = Completions.objects.create(institution = institution,
                                                            cip = cip,
                                                            award_level = self.safe_cast(row[3]),
                                                            total_awards = self.safe_cast(row[5]),
                                                            total_awards_male = self.safe_cast(row[7]),
                                                            total_awards_female = self.safe_cast(row[9])
                                                            )

                except (Institution.DoesNotExist, CIP.DoesNotExist) as e:
                    print('DoesNotExist row [{}]'.format(idx))
                    print(e)
                except CIP.MultipleObjectsReturned as e:
                    print('CIP Multiple Objects Returned row [{}]'.format(idx))
                    print(e)

                if (idx + 1) % 100 == 0:
                    print('[{}] completions processed'.format(idx + 1))

        except UnicodeDecodeError as e:
            print('Unicode error')
            print(e)

    def safe_cast(self, val):
        # TODO is there a way to pass type in to be cased, to make this very generic?
        try:
            return int(val)
        except:
            return 0

    def import_cip(self):
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_file = os.path.join(current_path, '../../../data/cip_occupational_crosswalk.csv')
        with open(dataset_file, mode = 'r', encoding = 'latin-1') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader)

            for idx, row in enumerate(reader):
                cip, created = CIP.objects.get_or_create(cip_code = row[8])

                if created:
                    cip.census_code = self.safe_cast(row[0])
                    cip.census_occupation_title = row[1]
                    cip.bls_code = row[2]
                    cip.bls_occupation_title = row[3]
                    cip.cip_occupation_title = row[9]

                else:
                    if not AliasTitle.objects.filter(alias_title = row[9]).exists():
                        print('Creating Alias for CIP [{}]: [{}]'.format(row[8], row[9]))
                        AliasTitle.objects.create(cip = cip, alias_title = row[9])

                if (idx + 1) % 100 == 0:
                    print('[{}] CIP records processed'.format(idx + 1))

    def import_data(self):

        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(current_path, '../../../data')
        for k, v in self.datasets.items():
            for dataset in v:
                path = os.path.join(dataset_path, k, '2015/{}.zip'.format(dataset))
                with zipfile.ZipFile(path) as z:
                    reader = csv.reader(TextIOWrapper(z.open('{}.csv'.format(dataset.lower()), mode = 'r'), encoding = 'latin-1'))
                    dataset = dataset.lower()

                    if dataset == 'hd2015':
                        self.handle_characteristics(reader)
                    elif dataset == 'ic2015_ay':
                        self.handle_tuition(reader)
                    elif dataset == 'adm2015':
                        self.handle_admissions(reader)
                    elif dataset == 'c2015_a':
                        self.handle_completions(reader)

        print('Completed import')
        print('Institution record count: [{}]'.format(Institution.objects.all().count()))
        print('Admissions record count: [{}]'.format(Admissions.objects.all().count()))
        print('Tuition record count: [{}]'.format(Tuition.objects.all().count()))
        print('Completions record count: [{}]'.format(Completions.objects.all().count()))


    def handle(self, *args, **options):
        print('Clearing database')
        Institution.objects.all().delete()
        CIP.objects.all().delete()
        self.import_cip()
        self.import_data()


