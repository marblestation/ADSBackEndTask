
def init_db(db):
    from ReferenceResolver.Models import ResolveModel

    db.drop_all()
    db.create_all()

    #resolve = ResolveModel(refstring="Test", bibcode="...................", status="Test", ip = "127.0.0.1")
    #db.session.add(resolve)
    #db.session.commit()
