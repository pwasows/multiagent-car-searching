import collections

"""This module defines AdData data type

AdData objects spawning:

AdData(<description string>,
       <a list of tags - (tag_name, tag_value) tuples>,
       <a hyperlink to the ad>)

Examples:
desc = 'Best VW Passat in SF Bay!''
tag_list = ['odometer': '150 000 km', 'year': '2000', 'engine': '1.9 TDi']
link = "https://sfbay.craigslist.org/eby/cto/d/00-vw-sports-wagon-1-owner/6607249314.html"

ad1 = AdData(desc, tag_list, link)
# or:
ad2 = AdData(description=desc, tags=tag_list, hyperlink=link)
"""

AdData = collections.namedtuple('AdData', ['description', 'tags', 'hyperlink'])
