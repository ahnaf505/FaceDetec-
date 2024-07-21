from tinydb import TinyDB, Query

db = TinyDB('db.json')

def filever_add(ver_id):
    db.insert({'veriv_id': str(ver_id)})

def filever_verif(ver_id):
    User = Query()
    result = db.search(User.veriv_id == str(ver_id))
    if not result:
        return False
    else:
        return True

def expire_verif(ver_id):
    User = Query()
    db.remove(User.veriv_id == str(ver_id))
