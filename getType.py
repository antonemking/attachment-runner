#########################################
# Antone M King                         #
# Output content-type for POST request  #
#########################################

from mimetypes import MimeTypes

def getContentType(file):
    mime = MimeTypes()
    x = mime.guess_type(file)[0]
    return x
