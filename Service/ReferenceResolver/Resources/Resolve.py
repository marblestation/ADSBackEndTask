from __future__ import division
from flask import request
from flask import g # Request context reserved for custom data
from flask_restful import Resource, marshal_with
from ReferenceResolver import db
from ReferenceResolver.Models import ResolveModel
from ResolveHelper import ResolveHelper


class Resolve(Resource):

    def __init__(self):
        # TODO: For every request, this method is called. Optimize to make ResolveHelper created only once.
        self.resolve_helper = ResolveHelper()


    @marshal_with(ResolveModel.resolve_marshaller)
    def get(self, refstring):
        bibcode = None
        status = None # None until a fatal error occurs or the processing has finished

        first_author, authors, remaining_refstring = self.resolve_helper.extract_authors(refstring)
        if first_author is None:
            status = "No first author found in refstring"

        if status is None:
            year, remaining_refstring = self.resolve_helper.extract_year(remaining_refstring)
            if year is None:
                status = "No year found in refstring"
            else:
                numbers, remaining_refstring = self.resolve_helper.extract_numbers(remaining_refstring)
                potential_bibstems = self.resolve_helper.extract_potential_bibstems(remaining_refstring)
                bibcode, status = self.resolve_helper.search_bibcode_in_ads(first_author, authors, year, numbers, potential_bibstems)

        resolve = ResolveModel(refstring=refstring, bibcode=bibcode, status=status, ip=request.remote_addr)
        db.session.add(resolve)
        db.session.commit()
        return resolve
        #return {'refstring': refstring, 'bibcode': bibcode, 'status': status}
