import os, sys

PROJECT_DIR = '/var/www/ekyc_two_face_compare/'
sys.path.insert(0, PROJECT_DIR)


def execfile(filename):
    globals = dict( __file__ = filename )
    exec( open(filename).read(), globals )

activate_this = os.path.join( '/var/www/ekyc_two_face_compare/facematchvenv/bin', 'activate_this.py' )
execfile( activate_this )


from two_face_compare_api import create_app
application = create_app()
application.debug = True
