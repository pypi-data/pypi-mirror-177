import os
from .settings import config
from .common import get_uuid_by_given_name, download_obj_from_server
def main(db, by='uuid'):
    md5 = None
    if by == 'given_name':
        md5 = get_uuid_by_given_name(db)
    elif by == 'uuid':
        md5 = db
    else:
        print('by type not found:', by)
    local_folder = os.path.join(config['axiom_cache'], md5, 'obj')
    if not os.path.isdir(local_folder):
        download_obj_from_server(md5)
    return local_folder
