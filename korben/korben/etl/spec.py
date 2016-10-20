import csv
import os
from korben import services

MAPPINGS = {}

CONSTANT_MAPPINGS = (
    ('optevia_businesstypeId', 'optevia_businesstypeSet', 'optevia_name', 'company_businesstype'),
    ('optevia_sectorId', 'optevia_sectorSet', 'optevia_name', 'company_sector'),
    ('optevia_employeerangeId', 'optevia_employeerangeSet', 'optevia_name', 'company_employeerange'),
    ('optevia_turnoverrangeId', 'optevia_turnoverrangeSet', 'optevia_name', 'company_turnoverrange'),
    ('optevia_ukregionId', 'optevia_ukregionSet', 'optevia_name', 'company_ukregion'),
    ('optevia_countryId', 'optevia_countrySet', 'optevia_Country', 'company_country'),
    ('optevia_titleId', 'optevia_titleSet', 'optevia_name', 'company_title'),
    ('optevia_contactroleId', 'optevia_contactroleSet', 'optevia_name', 'company_role'),
    ('optevia_interactioncommunicationchannelId', 'optevia_interactioncommunicationchannelSet', 'optevia_name', 'company_interactiontype'),
    ('BusinessUnitId', 'BusinessUnitSet', 'Name', 'company_team'),
    ('optevia_serviceId', 'optevia_serviceSet', 'optevia_name', 'company_service'),
)

# Used to avoid having to make Django fields nullable, this is loaded into all
# "enum" style tables in the Django database
CONSTANT_UNDEFINED_ID = '0167b456-0ddd-49bd-8184-e3227a0b6396'

# ~8% of contacts in CDMS don’t have an email, we use the following placeholder
FAKE_EMAIL = 'fake@no-email-address-supplied.com'

for source_pkey, source_table, source_name, target_table in CONSTANT_MAPPINGS:
    MAPPINGS.update({
        source_table: {
            'to': target_table,
            'local': (
                (source_pkey, 'id'),
                (source_name, 'name'),
            ),
        },
    })

MAPPINGS.update({
    'AccountSet': {
        'to': 'company_company',
        'local': (
            ('AccountId', 'id'),
            ('Name', 'name'),
            ('optevia_Alias', 'alias'),
            ('optevia_CompaniesHouseNumber', 'company_number'),
            ('optevia_ukorganisation', 'uk_based'),
            ('optevia_Address1', 'registered_address_1'),
            ('optevia_Address2', 'registered_address_2'),
            ('optevia_Address3', 'registered_address_3'),
            ('optevia_Address4', 'registered_address_4'),
            ('optevia_TownCity', 'registered_address_town'),
            ('optevia_StateCounty', 'registered_address_county'),
            ('optevia_PostCode', 'registered_address_postcode'),
            ('Description', 'description'),
        ),
        'nonflat': (
            ('optevia_Country', (('Id', 'registered_address_country_id'),),),
            ('optevia_UKRegion', (('Id', 'uk_region_id'),),),
            ('optevia_BusinessType', (('Id', 'business_type_id'),),),
            ('optevia_Sector', (('Id', 'sector_id'),),),
            ('optevia_EmployeeRange', (('Id', 'employee_range_id'),),),
            ('optevia_TurnoverRange', (('Id', 'turnover_range_id'),),),
        ),
        'defaults': (
            ('archived', lambda: False),
        ),
        'empty_strings': (
            'alias',
            'description',
            'registered_address_1',
            'registered_address_2',
            'registered_address_3',
            'registered_address_4',
            'registered_address_town',
            'registered_address_county',
            'registered_address_postcode',
            'trading_address_1',
            'trading_address_2',
            'trading_address_3',
            'trading_address_4',
            'trading_address_town',
            'trading_address_county',
            'trading_address_postcode',
            'archived_reason',
        ),
        'use_undefined': (
            'registered_address_country_id',
            'business_type_id',
            'sector_id',
            'uk_region_id',
        ),
    },
    'SystemUserSet': {
        'to': 'company_advisor',
        'local': (
            ('SystemUserId', 'id'),
            ('FirstName', 'first_name'),
            ('LastName', 'last_name'),
        ),
        'concat': (
            (('FirstName', 'MiddleName'), 'first_name', 'FirstName'),
        ),
    },
    'ContactSet': {
        'to': 'company_contact',
        'local': (
            ('ContactId', 'id'),
            ('Title', 'title_id'),
            ('LastName', 'last_name'),
            # ('FirstName', 'first_name'),
            # ('MiddleName', None),  data migration to move these
            # ('optevia_LastVerified', None)  korben magic to add current on write
            ('optevia_PrimaryContact', 'primary'),
            ('optevia_CountryCode', 'telephone_countrycode'),
            ('EMailAddress1', 'email'),
            ('optevia_Address1', 'address_1'),
            ('optevia_Address2', 'address_2'),
            ('optevia_Address3', 'address_3'),
            ('optevia_Address4', 'address_4'),
            ('optevia_TownCity', 'address_town'),
            ('optevia_StateCounty', 'address_county'),
            ('optevia_PostCode', 'address_postcode'),

            # moved to `nonflat`
            # ('ParentCustomerId_Id', 'company_id'),
            # ('optevia_Country_Id', 'address_country_id'),
            # ('optevia_UKRegion_Id', 'uk_region_id'),
            # ('optevia_ContactRole_Id', 'role_id'),

            # ('ModifiedOn', 'modified_on'),  not wanted in leeloo?
            # ('CreatedOn', 'created_on'),
        ),
        'concat': (
            (('optevia_AreaCode', 'optevia_TelephoneNumber'), 'telephone_number', 'optevia_TelephoneNumber'),
            (('FirstName', 'MiddleName'), 'first_name', 'FirstName'),
        ),
        'nonflat': (
            ('ParentCustomerId', (('Id', 'company_id'),),),
            ('optevia_Country', (('Id', 'address_country_id'),),),
            ('optevia_UKRegion', (('Id', 'uk_region_id'),),),
            ('optevia_ContactRole', (('Id', 'role_id'),),),
        ),
        'nonflat_defaults': (
            ('ParentCustomerId', {'LogicalName': 'account'}),
        ),
        'use_undefined': (
            'title_id',
            'role_id',
            'company_id',
            'uk_region_id',
        ),
        'empty_strings': (
            'archived_reason',
            'telephone_countrycode',
            'address_1',
            'address_2',
            'address_3',
            'address_4',
            'address_town',
            'address_county',
            'address_postcode',
            'telephone_number',
        ),
        'defaults': (
            ('primary', lambda: True),
            ('archived', lambda: False),
            ('address_same_as_company', lambda: False),
            ('email', lambda: FAKE_EMAIL),
        ),
    },

    # check commit history for more information
    'detica_interactionSet': {
        'to': 'company_interaction',
        'local': (
            ('ActivityId', 'id'),
            ('Subject', 'subject'),
            ('ActualStart', 'date_of_interaction'),
            ('optevia_Notes', 'notes'),

            # ('ModifiedOn', 'modified_on'),  not wanted in leeloo?
            # ('CreatedOn', 'created_on'),
        ),
        'nonflat': (
            ('optevia_InteractionCommunicationChannel', (('Id', 'interaction_type_id'),),),
            ('optevia_Advisor', (('Id', 'advisor_id'),),),
            ('optevia_Contact', (('Id', 'contact_id'),),),
            ('optevia_Organisation', (('Id', 'company_id'),),),
            ('optevia_ServiceProvider', (('Id', 'service_provider_id'),),),
            ('optevia_Service', (('Id', 'service_id'),),),
        ),
        'nonflat_defaults': (
            ('optevia_Organisation', {'LogicalName': 'account'}),
        ),
        'empty_strings': (
            'archived_reason',
        ),
        'defaults': (
            ('archived', lambda: False),
        ),
    },
})

DJANGO_LOOKUP = {mapping['to']: name for name, mapping in MAPPINGS.items()}


ES_STRING_ANALYZED = {'type': 'string', 'index': 'analyzed'}
ES_STRING_NOT_ANALYZED = {'type': 'string', 'index': 'not_analyzed'}
ES_STRING_NO = {'type': 'string', 'index': 'no'}


def update(original_dict, update_dict):
    'Copy original_dict and update with update_dict'
    updated_dict = dict(original_dict)
    updated_dict.update(update_dict)
    return updated_dict

ES_INDEX = 'datahub'
_ES_TYPES = None


def get_es_types():
    'since this introspects the db to get table information, it must be called'
    global _ES_TYPES
    if _ES_TYPES is not None:
        return _ES_TYPES
    _ES_TYPES = {}
    tables = services.db.get_django_metadata().tables.values()
    for table in tables:  # NOQA
        if table.name not in DJANGO_LOOKUP:
            continue
        properties = {}
        for column in table.columns:
            # TODO: do a little type introspection for bools
            if not column.foreign_keys:
                properties[column.name] = ES_STRING_ANALYZED
            else:
                column_name = column.name[:-3]  # strip `_id` suffix
                properties[column_name] = ES_STRING_ANALYZED
        _ES_TYPES[table.name] = {'properties': properties}
    return _ES_TYPES


COLNAME_LONGSHORT = {}
COLNAME_SHORTLONG = {}
_COLNAME_MAPPING_PATH = os.path.join(
    os.path.dirname(__file__), 'cdms-psql-column-mapping.csv'
)
with open(_COLNAME_MAPPING_PATH) as fh:
    for table_name, long_col, short_col in csv.reader(fh):
        COLNAME_LONGSHORT[(table_name, long_col)] = short_col
        COLNAME_SHORTLONG[(table_name, short_col)] = long_col
