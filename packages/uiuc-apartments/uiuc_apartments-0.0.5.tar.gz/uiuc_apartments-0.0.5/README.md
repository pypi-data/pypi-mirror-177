# UIUC Apartment Kit

A wrapper around a webscraper for popular rental agencies on UIUC campus

Installation:
```
pip install uiuc-apartments
```

Usage:
```py
from uiuc_apartments import AllAgencies

for agency in AllAgencies:
    print(agency.get_all())
```

```py
from uiuc_apartments import Smith
agency = Smith()
print(agency.name) # Smith Apartments
apartments = agency.get_all()
# [<Apartment $1020.0/month 2.0 beds/1.0 baths 8/2/2024 Smith Apartments>, ...
print(apartments[0].link)
# https://smithapartments-cu.com/property-details/?pid=27
```

Development:

+ Add a new agency to the folder
+ Add it to the imports of `agencies/__init__.py` and to `AllAgencies`
