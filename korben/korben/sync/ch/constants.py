DOWNLOAD_URL = 'http://download.companieshouse.gov.uk/en_output.html'
CACHE_PATH = '/cache'  # TODO: find out where this type of thing should live
SUPPORTED_CSV_FIELDNAMES = (  # ask @ztolley
    'name',
    'company_number',
    'address_care_of',
    'address_po_box',
    'address_address_1',
    'address_address_2',
    'address_town',
    'address_county',
    'address_country',
    'address_postcode',
    'company_category',
    'company_status',
    'country_of_origin',
    'dissolution_date',
    'incorporation_date',
    'accounts_accounting_ref_day',
    'accounts_accounting_ref_month',
    'accounts_next_due_date',
    'accounts_last_made_up_date',
    'accounts_category',
    'returns_next_due_date',
    'returns_last_made_up_date',
    'mortgages_num_mort_charges',
    'mortgages_num_mort_outstanding',
    'mortgages_num_mort_part_satisfied',
    'mortgages_num_mort_satisfied',
    'sic_code_1',
    'sic_code_2',
    'sic_code_3',
    'sic_code_4',
    'limited_partnerships_num_gen_partners',
    'limited_partnerships_num_lim_partners',
    'uri',
    'previous_name_1_change_of_name_date',
    'previous_name_1_company_name',
    'previous_name_2_change_of_name_date',
    'previous_name_2_company_name',
    'previous_name_3_change_of_name_date',
    'previous_name_3_company_name',
    'previous_name_4_change_of_name_date',
    'previous_name_4_company_name',
    'previous_name_5_change_of_name_date',
    'previous_name_5_company_name',
    'previous_name_6_change_of_name_date',
    'previous_name_6_company_name',
    'previous_name_7_change_of_name_date',
    'previous_name_7_company_name',
    'previous_name_8_change_of_name_date',
    'previous_name_8_company_name',
    'previous_name_9_change_of_name_date',
    'previous_name_9_company_name',
    'previous_name_10_change_of_name_date',
    'previous_name_10_company_name'
)
