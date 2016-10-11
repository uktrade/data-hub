# Models and specs for Data Hub Backend

Document containing specification for models in Korben and Leeloo, with caveats and required fields.

## Company

| CDMS | Required | Leeloo | Display | Comments |
|:---:|:---:|:---:|:---:|---|
| `Name` | `← * →` | `name` | Registered name | _Companies House_ XOR _CDMS name_ |
| `optevia_Alias` | | `alias` | Trading name | |
| `optevia_ukorganisation` | `← *` |  | UK based | Inferred property |
| `optevia_BusinessType_Id` | `* →` | `business_type_id` | Type of business | |
| `optevia_Sector_Id` | `← * →` | `sector_id` | Sector | |
| `optevia_Address1` | `← * →` | `registered_address_1` | Address line 1 | |
| `optevia_Address2` | | `registered_address_2` | Address line 2 | |
| `optevia_Address3` | | `registered_address_3` | Address line 3 | |
| `optevia_Address4` | | `registered_address_4` | Address line 4 | |
| `optevia_TownCity` | `← *` | `registered_address_towncity` | Address town/city | Korben sends `N/A` |
| `optevia_StateCounty` | | `registered_address_county` | Address county | |
| `optevia_Country_Id` | `← * →` | `registered_address_country_id` | Address country | |
