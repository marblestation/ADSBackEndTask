from flask import request
from flask import g # Request context reserved for custom data
from flask_restful import Resource, marshal_with
from ReferenceResolver import db
from ReferenceResolver.Models import ResolveModel

class Resolve(Resource):

    #@marshal_with(ResolveModel.resolve_marshaller)
    def get(self, refstring):
        import re
        #refstring = "Accomazzi, A., Eichhorn, G., Kurtz, M. J., Grant, C. S., & Murray, S. S. 2000, A&AS, 143, 85"
        # NOTE: Test regex in http://pythex.org/
        authors_pattern = re.compile("(?:([A-Z]{1}[a-z]+), ([A-Z]\.(?: [A-Z]\.)?)+)(?:, et. al. |, et. al.|, & |, |. |.)")
        authors = authors_pattern.findall(refstring)

        if len(authors) == 0:
            # Alternative author pattern
            #refstring = "Adainson M, Kerr Th, Whittet DCB, Duley WW. 1994. MNRAS 268:705-8"
            authors_pattern = re.compile("(?:([A-Z]{1}[a-z]+) ([A-Z]+[a-zA-Z]*))+(?:, |. |.)")
            authors = authors_pattern.findall(refstring)

        if len(authors) == 0:
            # TODO: Problem
            first_author = None
        else:
            remaining_refstring = authors_pattern.sub('', refstring)
            first_author = ", ".join(authors[0])
            if first_author[-1] != ".":
                first_author += "."

        # WARNING: Year pattern valid for years between 1800 and 2016 only:
        year_pattern = re.compile("(?:\(| )*(18\d\d|19\d\d|200\d|201[0-6])(?:, |. |,|.|\).|\))")
        years = year_pattern.findall(remaining_refstring)
        remaining_refstring = year_pattern.sub('', remaining_refstring)

        if len(years) == 0:
            # TODO: We don't have a year!
            year = None
        else:
            # TODO: Consider multiple years if more than one is found
            # Just use the first year found
            year = years[0]

        #from adsutils import get_pub_abbreviation
        #pubstring = 'American Astronautical Society Meeting'
        #result = get_pub_abbreviation(pubstring)

        ## How to get an API token:
        # 1. Create an account and log in to the latest version of the ADS.
        # 2. Push the "Generate a new key" button under Account - Customize settings - API Token
        import ads
        ads.config.token = "K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK"

        ## TODO: I do not manage to build a query forcing all the authors to be present
        #articles = list(ads.SearchQuery(q="", year=2014, max_pages=1, first_author="Blanco-Cuaresma, S.", author=["Blanco-Cuaresma, S.", "Soubiran, C.", "+Jofre, P."], sort="citation_count"))
        #articles = ads.SearchQuery(q="", year=2014, max_pages=1, first_author="Blanco-Cuaresma, S.", sort="citation_count", fl=["bibcode", "author", "bibstem", "alternate_bibcode", "citation_count", "identifier", "volume", "page", "year"])
        articles = ads.SearchQuery(q="", year=year, max_pages=1, first_author=first_author, sort="citation_count", fl=["id", "bibcode", "author", "bibstem", "volume", "page", "year"])

        score = {}
        for article in articles:
            # TODO: Compare author names
            # TODO: Compare publication (use get_pub_abbreviation)
            current_bibcode = article.bibcode
            score[current_bibcode] = 0
            if len(article.author) == len(authors):
                score[current_bibcode] += 1
            if article.volume in remaining_refstring:
                score[current_bibcode] += 1
            current_page = article.page
            if len(current_page) > 0 and current_page[0] in remaining_refstring:
                score[current_bibcode] += 1
        if len(score) > 0:
            bibcode = max(score, key=score.get)
        else:
            bibcode = None

        #from adsutils import resolve_references
        #refdata = 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541'
        #ads_resolved_bibcode = resolve_references(refstring)

        return {'refstring': refstring, 'bibcode': bibcode}
