from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Institution(models.Model):
    # from hd2015

    OBEREG_CHOICES = (
        (0, 'US Service School'),
        (1, 'New England (CT, ME, MA, NH, RI, VT)'),
        (2, 'Mid East (DC, DE, MD, NH, NY, PA)'),
        (3, 'Great Lakes (IL, IN, MI, OH, WI'),
        (4, 'Plains (IA, KS, MN, MO, NE, ND, SD)'),
        (5, 'Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)'),
        (6, 'Southwest (AX NM, OK, TX)'),
        (7, 'Rocky Mountains (CO, ID, MT, UT, WY)'),
        (8, 'Far West (AK, CA, HI, NV, OR, WA)'),
        (9, 'Outlying Areas (AS, FM, GU, MH, MP, PR, PW, VI)'),
        (-3, 'Not Available')
    )

    SECTOR_CHOICES = (
        (0, 'Administrative Unit'),
        (1, 'Public, 4 Year or Above'),
        (2, 'Private Non Profit, 4 Year or Above'),
        (3, 'Private For Profit, 4 Year or Above'),
        (4, 'Public, 2 Year'),
        (5, 'Private Non Profit, 2 Year'),
        (6, 'Private For Profit, 2 Year'),
        (7, 'Public, Less Than 2 Year'),
        (8, 'Private Non Profit, Less Than 2 Year'),
        (9, 'Private For Profit, Less Than 2 Year'),
        (99, 'Sector Unknown')
    )

    LEVEL_CHOICES = (
        (1, 'Four or more years'),
        (2, 'At least 2 years and less than 4'),
        (3, 'Less than 2 years (Below Associate)'),
        (-3, 'Not Available'),
    )

    CONTROL_CHOICES = (
        (1, 'Public'),
        (2, 'Private Non Profit'),
        (3, 'Private For Profit'),
        (-3, 'Not Available')
    )

    DEGREE_CHOICES = (
        (0, 'Other'),
        (1, 'Postsecondary award, certificate or diploma of less than one academic year'),
        (2, 'Postsecondary award, certificate or diploma of at least one but less than two academic years'),
        (3, 'Associate\'s degree'),
        (4, 'Postsecondary award, certificate or diploma of at least two but less than four academic years'),
        (5, 'Bachelor\'s degree'),
        (6, 'Postbaccalaureate certificate'),
        (7, 'Master\'s degree'),
        (8, 'Post-Master\'s degree'),
        (9, 'Doctor\'s degree'),
        (-3, 'Not Available')
    )

    LOCALE_CHOICES = (
        (11, 'Large city with population > 250,000'),
        (12, 'Mid-sized city with population between 100,000 and 250,000'),
        (13, 'Small city with population < 100,000'),
        (21, 'Large suburb with population > 250,000'),
        (22, 'Mid-sized surburb with population between 100,000 and 250,000'),
        (23, 'Small suburb with population less than 100,000'),
        (31, 'Fringe town <= 10 miles from nearest urbanized area'),
        (32, 'Distant town between 10 and 35 miles from nearest urbanized area'),
        (33, 'Remote town that is > 35 miles from nearest urbanized area'),
        (41, 'Rural, Fringe'),
        (42, 'Rural, Distant'),
        (43, 'Rural, Remote'),
        (-3, 'Not Available')
    )

    SYSTEM_TYPE_CHOICES = (
        (1, 'Multi-institution or multi-campus'),
        (2, 'Not multi-institution or multi-campus'),
        (-1, 'Not Reported'),
        (-2, 'Not Applicable')
    )

    unitid = models.IntegerField(help_text = 'Institution unit ID', unique = True)
    name = models.CharField(max_length = 100, default = '', db_index = True, help_text = 'Institution name')
    address = models.CharField(max_length = 100, default = '', help_text = 'Address of institution')
    city = models.CharField(max_length = 50, default = '', help_text = 'City of institution')
    state = models.CharField(max_length = 3, default = '', help_text = 'State')
    ein = models.CharField(max_length = 20, default = '', help_text = 'IRS EIN number')
    location_region = models.IntegerField(default = -3, choices = OBEREG_CHOICES,
                                          help_text = 'Bureau of Economic Analysis Region')
    web_address = models.URLField(max_length = 255, default = '', help_text = 'Institution web address')
    admission_url = models.URLField(max_length = 255, default = '', help_text = 'Admission URL')
    financial_aid_url = models.URLField(max_length = 255, default = '', help_text = 'Financial Aid URL')
    application_url = models.URLField(max_length = 255, default = '', help_text = 'Application URL')
    net_price_url = models.URLField(max_length = 255, default = '', help_text = 'Net Price Calculator URL')
    sector = models.IntegerField(default = 99, choices = SECTOR_CHOICES,
                                 help_text = 'Institution category joining level and control')
    level = models.IntegerField(default = -3, choices = LEVEL_CHOICES,
                                help_text = 'Classification of institution programs by year length')
    control = models.IntegerField(default = -3, choices = CONTROL_CHOICES,
                                  help_text = 'Institution operated publicly or private')
    highest_award = models.IntegerField(default = -3, choices = DEGREE_CHOICES,
                                        help_text = 'Highest offering award')
    locale = models.IntegerField(default = -3, choices = LOCALE_CHOICES,
                                 help_text = 'Geographic status of a school based on surrounding '
                                             'population and distance')
    enrollment = models.IntegerField(default = -1, help_text = 'Total student enrollment')
    system_type = models.IntegerField(default = -2, choices = SYSTEM_TYPE_CHOICES,
                                      help_text = 'Multi-institution or multi-campus organization')
    system_name = models.CharField(max_length = 255, default = '',
                                   help_text = 'Name of multi-instition or multi-campus organization')
    location = models.PointField(default = Point(0, 0), spatial_index = True)

    def __str__(self):
        return 'Name: [{}] State: [{}]'.format(self.name, self.state)


class BaseTuition(models.Model):
    institution = models.ForeignKey(Institution, related_name = 'tuitions', related_query_name = 'tuition')
    academic_year_2013_books = models.IntegerField(default = -1, help_text = '2013 academic year books and supplies')
    academic_year_2014_books = models.IntegerField(default = -1, help_text = '2014 academic year books and supplies')
    academic_year_2015_books = models.IntegerField(default = -1, help_text = '2015 academic year books and supplies')
    academic_year_2013_board = models.IntegerField(default = -1,
                                                   help_text = '2013 academic year on-campus room and board')
    academic_year_2014_board = models.IntegerField(default = -1,
                                                   help_text = '2014 academic year on-campus room and board')
    academic_year_2015_board = models.IntegerField(default = -1,
                                                   help_text = '2015 academic year on-campus room and board')

    class Meta:
        abstract = True


class Tuition(BaseTuition):
    # from ic2015_ay

    TUITION_CLASSES = (
        (0, 'In District'),
        (1, 'In State'),
        (2, 'Out of State'),
        (-1, 'Not Applicable')
    )

    tuition_class = models.IntegerField(default = -1, choices = TUITION_CLASSES,
                                        help_text = 'Tuition rates of student origin')
    cost = models.IntegerField(default = -1, help_text = 'List price for annual tuition')
    fees = models.IntegerField(default = -1, help_text = 'List price for annual fees - full time enrollment')
    credit_hour = models.IntegerField(default = -1, help_text = 'List price of credit hour cost')
    academic_year_2013_cost = models.IntegerField(default = -1, help_text = '2013 academic year cost and fees')
    academic_year_2014_cost = models.IntegerField(default = -1, help_text = '2014 academic year cost and fees')
    academic_year_2015_cost = models.IntegerField(default = -1, help_text = '2015 academic year cost and fees')

    def __str__(self):
        return '{} [class: [{}]] [list cost: [{}]]'.format(self.institution.name, self.tuition_class, self.cost)


class Admission(models.Model):
    # From adm2015
    institution = models.OneToOneField(Institution)
    total_applicants = models.IntegerField(default = -1, help_text = 'Total number of applicants')
    male_applicants = models.IntegerField(default = -1, help_text = 'Total number of male applicants')
    female_applicants = models.IntegerField(default = -1, help_text = 'Total number of female applicants')

    total_admissions = models.IntegerField(default = -1, help_text = 'Total number of admissions')
    male_admissions = models.IntegerField(default = -1, help_text = 'Total number of male admissions')
    female_admissions = models.IntegerField(default = -1, help_text = 'Total number of female admissions')

    total_enrollment = models.IntegerField(default = -1, help_text = 'Total enrollment')
    male_enrollment = models.IntegerField(default = -1, help_text = 'Male enrollment')
    female_enrollment = models.IntegerField(default = -1, help_text = 'Female enrollment')

    ft_enrollment = models.IntegerField(default = -1, help_text = 'Total full-time enrollment')
    ft_male_enrollment = models.IntegerField(default = -1, help_text = 'Total male full-time enrollment')
    ft_female_enrollment = models.IntegerField(default = -1, help_text = 'Total female full-time enrollment')

    pt_enrollment = models.IntegerField(default = -1, help_text = 'Total part-time enrollment')
    pt_male_enrollment = models.IntegerField(default = -1, help_text = 'Total male part-time enrollment')
    pt_female_enrollment = models.IntegerField(default = -1, help_text = 'Total female part-time enrollment')

    sat_reading_25 = models.IntegerField(default = -1, help_text = 'SAT critical reading 25th percentile')
    sat_reading_75 = models.IntegerField(default = -1, help_text = 'SAT critical reading 75th percentile')
    sat_math_25 = models.IntegerField(default = -1, help_text = 'SAT math 25th percentile')
    sat_math_75 = models.IntegerField(default = -1, help_text = 'SAT math 75th percentile')
    sat_writing_25 = models.IntegerField(default = -1, help_text = 'SAT writing 25th percentile')
    sat_writing_75 = models.IntegerField(default = -1, help_text = 'SAT writing 75th percentile')

    act_composite_25 = models.IntegerField(default = -1, help_text = 'ACT composite 25th percentile')
    act_composite_75 = models.IntegerField(default = -1, help_text = 'ACT composite 75th percentile')
    act_english_25 = models.IntegerField(default = -1, help_text = 'ACT english 25th percentile')
    act_english_75 = models.IntegerField(default = -1, help_text = 'ACT english 75th percentile')
    act_math_25 = models.IntegerField(default = -1, help_text = 'ACT math 25th percentile')
    act_math_75 = models.IntegerField(default = -1, help_text = 'ACT math 75th percentile')
    act_writing_25 = models.IntegerField(default = -1, help_text = 'ACT writing 25th percentile')
    act_writing_75 = models.IntegerField(default = -1, help_text = 'ACT writing 75th percentile')

    def __str__(self):
        return '{} [applicants: [{}]]'.format(self.institution.name, self.total_applicants)


class Crosswalk(models.Model):
    """
    A crosswalk between IPEDS, Bureau of Labor and Office of Management and Budget classification
    codes and occupation titles
    """
    census_code = models.IntegerField(default = -1, help_text = 'Census 2000 occupation code')
    census_occupation_title = models.CharField(default = 'No Title', db_index = True, max_length = 200,
                                               help_text = 'Census Occupation Title')
    bls_code = models.CharField(default = 'No Code', db_index = True, max_length = 100,
                                help_text = 'Bureau of Labor Code')
    bls_occupation_title = models.CharField(default = 'No Title', db_index = True, max_length = 200,
                                            help_text = 'Bureau of Labor occupation title')
    ombsoc_code = models.CharField(default = 'No Code', db_index = True, max_length = 100,
                                   help_text = 'OMB Standard Occupation Classification code')
    ombsoc_occupation_title = models.CharField(default = 'No Title', db_index = True, max_length = 200,
                                               help_text = 'OMB Standard Occupation Classification title')
    cip_code = models.CharField(default = 'No Code', db_index = True, max_length = 100, help_text = 'CIP code')
    cip_occupation_title = models.CharField(default = 'No Title', db_index = True, max_length = 200,
                                            help_text = 'CIP occupation')

    def __str__(self):
        return '[Census code: [{}]] [BLS code: [{}]] [CIP code: [{}]'.format(self.census_code,
                                                                             self.bls_code,
                                                                             self.cip_code)


class AliasTitle(models.Model):
    """
    Some Crosswalk codes have duplicate occupation titles for a CIP code.  Store the alias title here
    """
    BUREAU_TYPES = (
        (0, 'Census'),
        (1, 'Bureau of Labor'),
        (2, 'Office of Management'),
        (3, 'Education')
    )

    crosswalk = models.ForeignKey(Crosswalk, related_name = 'aliases', related_query_name = 'alias')
    bureau_type = models.IntegerField(choices = BUREAU_TYPES, default = 3)
    alias_title = models.CharField(default = '', db_index = True, max_length = 200,
                                   help_text = 'Alias CIP occupation title')


class Completion(models.Model):
    institution = models.ForeignKey(Institution, related_name = 'completions', related_query_name = 'completion')
    crosswalk = models.ForeignKey(Crosswalk, related_name = 'cips', related_query_name = 'cip')
    award_level = models.IntegerField(default = -1, help_text = 'Institution award level')
    total_awards = models.IntegerField(default = -1, help_text = 'Total awards for this program')
    total_awards_male = models.IntegerField(default = -1, help_text = 'Total awards of this program to men')
    total_awards_female = models.IntegerField(default = -1, help_text = 'Total awards of this program to women')
