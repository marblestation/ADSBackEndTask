from __future__ import division
import re
from adsutils import get_pub_abbreviation
import ads

class ResolveHelper(object):

    def __init__(self):
        # NOTE: Test regex in http://pythex.org/
        name_pattern = "([A-Z]\.(?: [A-Z]\.)?)"
        surname_pattern = "([A-Z]{1}[a-z]+(?:(?:-| )[A-Z]{1}[a-z]+)?)"

        self.authors_pattern = []
        #refstring = "Accomazzi, A., Eichhorn, G., Kurtz, M. J., Grant, C. S., & Murray, S. S. 2000, A&AS, 143, 85"
        self.authors_pattern.append(re.compile("^(?:"+surname_pattern+", "+name_pattern+")(?:, et. al. |, et. al.|, and |, & |, |. |.)"))
        #refstring = "J. B. Gupta, K. Kumar, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977)."
        self.authors_pattern.append(re.compile("^(?:"+name_pattern+" "+surname_pattern+")(?:, et. al. |, et. al.|, and |, & |, |. |.)"))
        #refstring = "Adainson M, Kerr Th, Whittet DCB, Duley WW. 1994. MNRAS 268:705-8"
        self.authors_pattern.append(re.compile("^(?:"+surname_pattern+" ([A-Z]+[a-zA-Z]*))+(?:, |. |.)"))

    def _match_authors(self, refstring, authors_pattern):
        """
        Find author names on a reference string based on a pattern, which should
        match author name+surname at the beginning of the refstring.

        Return list of authors and the remaining unmatched reference string
        """
        authors = []
        remaining_refstring = refstring
        match = authors_pattern.match(remaining_refstring)
        while match is not None:
            authors.append(match.groups())
            remaining_refstring = authors_pattern.sub('', remaining_refstring)
            match = authors_pattern.match(remaining_refstring)
        return authors, remaining_refstring

    def extract_authors(self, refstring):
        authors, remaining_refstring = self._match_authors(refstring, self.authors_pattern[0])

        if len(authors) == 0:
            # Alternative author pattern
            authors, remaining_refstring = self._match_authors(refstring, self.authors_pattern[1])
            authors = [ (x[1], x[0]) for x in authors ] # Reverse to have surnames in first position (to match the rest of compatible formats)

        if len(authors) == 0:
            # Alternative author pattern
            authors, remaining_refstring = self._match_authors(refstring, self.authors_pattern[2])

        if len(authors) == 0:
            first_author = None
        else:
            first_author = ", ".join(authors[0])
            if first_author[-1] != ".":
                first_author += "."
        return first_author, authors, remaining_refstring

    def extract_year(self, refstring):
        # WARNING: Year pattern valid for years between 1800 and 2016 only:
        year_pattern = re.compile("(?:\(| )*(18\d\d|19\d\d|200\d|201[0-6])(?:, |. |,|.|\).|\))")
        years = year_pattern.findall(refstring)
        remaining_refstring = year_pattern.sub('', refstring)

        if len(years) == 0:
            year = None
        else:
            # TODO: Consider multiple years if more than one is found
            # Just use the first year found
            year = years[0]
        return year, remaining_refstring

    def extract_numbers(self, refstring):
        # Find remaining number which may correspond to volume, page or other value
        number_pattern = re.compile("\\d+")
        numbers = number_pattern.findall(refstring)
        remaining_refstring = number_pattern.sub('', refstring)
        return numbers, remaining_refstring

    def extract_potential_bibstems(self, refstring):
        # Identify PhD Thesis
        phd_pattern = re.compile("(Ph(?:\.)?D(?:\.)|(?:T|t)hesis|(?:D|d)issertation)")
        if phd_pattern.search(refstring) is not None:
            potential_bibstems = {'PhDT': 1}
        else:
            # Try to infer a publication
            # TODO: Implement a smarter way to isolate potential publication name
            potential_bibstems = get_pub_abbreviation(refstring)
            potential_bibstems = {x[1].replace(".", ""): x[0] for x in potential_bibstems}
        return potential_bibstems

    def _get_score(self, first_author, authors, year, numbers, potential_bibstems, article_bibcode, article_authors, article_volume, article_page, article_bibstem):
        score = 0
        # Year should coincide with 4 first bibcode characthers
        if article_bibcode[:4] == year:
            score += 1

        # First letter of first author surname should be at the end of bibcode
        if article_bibcode[-1] == first_author[0]:
            score += 1

        if len(article_authors) == len(authors):
            # Check if authors' surnames coincidences in the expected order
            authors_score = 0
            for i, (surname, name) in enumerate(authors):
                if surname in article_authors[i]:
                    authors_score += 1
            # Normalize authors' score to keep scores comparable independently of the number of authors
            score += authors_score / len(authors)

        # Is volume number present in the refstring as a number?
        if article_volume in numbers:
            score += 1

        # Is page number present in the refstring as a number?
        if article_page is not None and len(article_page) > 0 and article_page[0] in numbers:
            score += 1

        # Abbreviated publication name (journal) matches any predicted ones?
        if article_bibstem in potential_bibstems.keys():
            score += potential_bibstems[article_bibstem]
        return score

    def search_bibcode_in_ads(self, first_author, authors, year, numbers, potential_bibstems):
        try:
            ## TODO: I do not manage to build a query forcing all the authors to be present
            ## TODO: ADS Search API is not looking for author's synonyms and I do not manage to activate that option
            ##       (while ADS web has this feature on by default as it is also explained in ADS Help)
            articles = ads.SearchQuery(q="", year=year, max_pages=1, first_author=first_author, sort="citation_count", fl=["bibcode", "author", "volume", "page"])

            score = {}
            for article in articles:
                # Key values for current article
                article_bibcode = article.bibcode
                article_bibstem = article_bibcode[4:].split(".")[0]
                score[article_bibcode] = self._get_score(first_author, authors, year, numbers, potential_bibstems, article_bibcode, article.author, article.volume, article.page, article_bibstem)
        except ads.exceptions.APIResponseError:
            bibcode = None
            status = "ADS API call failed with an error"
        else:
            if len(score) > 0:
                bibcode = max(score, key=score.get)
                status = "Success (score = {0})".format(max(score.values()))
            else:
                bibcode = None
                status = "ADS API call returned no article candidates"
        return bibcode, status
