li=[
"Algeria",
"Argentina",
"Australia",
"Austria",
"Azerbaijan",
"Bahrain",
"Bangladesh",
"Belarus",
"Belgium",
"Bolivia",
"Bosnia and Herzegovina",
"Brazil",
"Bulgaria",
"Canada",
"Chile",
"China",
"Colombia",
"Croatia",
"Czechia",
"Denmark",
"Egypt",
"Estonia",
"Ethiopia",
"Finland",
"France",
"Georgia",
"Germany",
"Ghana",
"Greece",
"Hong Kong",
"Hungary",
"Iceland",
"India",
"Indonesia",
"Iraq",
"Ireland",
"Israel",
"Italy",
"Jamaica",
"Japan",
"Jordan",
"Kazakhstan",
"Kenya",
"Kuwait",
"Latvia",
"Lebanon",
"Libya",
"Lithuania",
"Luxembourg",
"Macedonia",
"Malawi",
"Malaysia",
"Mexico",
"Montenegro",
"Morocco",
"Mozambique",
"Nepal",
"Netherlands",
"New Zealand",
"Nigeria",
"Norway",
"Oman",
"Pakistan",
"Panama",
"Peru",
"Philippines",
"Poland",
"Portugal",
"Puerto Rico",
"Qatar",
"Romania",
"Russia",
"Saudi Arabia",
"Senegal",
"Serbia",
"Singapore",
"Slovakia",
"Slovenia",
"South Africa",
"South Korea",
"Spain",
"Sri Lanka",
"Sweden",
"Switzerland",
"Taiwan",
"Tanzania",
"Thailand",
"Togo",
"Tunisia",
"Turkey",
"Uganda",
"Ukraine",
"United Arab Emirates",
"United Kingdom",
"United States",
"Venezuela",
"Vietnam",
"Yemen",
"Zimbabwe"
]
li.sort()
print("[")
for i in li:
    print("{\n'model': 'blog.country',\n")
    print("'pk':"+str(li.index(i)+1)+",\n")
    print("'fields': {\n")
    print("'name': '"+i+"',\n")
    print("'slug': '"+i.lower().replace(" ","_")+"',\n")
    print("'created_date': '2022-09-30'\n")
    print("}\n")
    print("},\n")

print("]")