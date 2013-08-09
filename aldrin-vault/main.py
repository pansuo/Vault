#!/usr/bin/env python

import webapp2, jinja2, os, hashlib, hmac, string, sys, logging, urllib

from google.appengine.api import files
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                              autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(render_str(template, **kw))

class FrontPageHandler(BaseHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.render('vault.html', upload_url=upload_url)

    def post(self):
        user_passphrase = self.request.get('passphrase')
        self.write(self.request)






class Passphrase(db.Model):
    passphrase = db.StringProperty(required=True)
    blob_key = blobstore.BlobReferenceProperty()

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads()
        blob_info = upload_files[0]
        logging.error(blob_info)
        self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)






app = webapp2.WSGIApplication([('/', FrontPageHandler), 
                               ('/serve/([^/]+)?', ServeHandler), 
                               ('/upload', UploadHandler)
                              ], debug=True)
