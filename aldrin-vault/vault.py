#!/usr/bin/env python

import webapp2, jinja2, os, hashlib, hmac, string, sys, logging, urllib, VaultHash, time

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
        passphrase_hash = VaultHash.hash(user_passphrase)
        self.response.headers.add_header('Set-Cookie', 'passphrase=%s; Path=/' % passphrase_hash)
        self.redirect('/stash')

class StashHandler(BaseHandler):
    def get(self):
        passphrase_cookie = self.request.cookies.get('passphrase')
        passphrases = db.GqlQuery("SELECT * FROM Passphrase WHERE passphrase = :1", passphrase_cookie)
        #self.response.headers.add_header('Set-Cookie', 'passphrase=; Path=/')
        passphrases = list(passphrases)
        files = [entity.blob.key() for entity in passphrases]
        infos = blobstore.BlobInfo.get(files)
        self.render('stash.html', files=infos)

    def post(self):
        file_id = self.request.get('file_id')
        blob_info = blobstore.BlobInfo.get(file_id)
        passphrase = db.GqlQuery("SELECT * FROM Passphrase WHERE blob = :1", blob_info.key()).get()
        blob_info.delete()
        passphrase.delete()
        self.redirect('/')



class Passphrase(db.Model):
    passphrase = db.StringProperty(required=True)
    blob = blobstore.BlobReferenceProperty()

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, BaseHandler):
    def post(self):
        upload_files = self.get_uploads()
        user_passphrase = self.request.get('passphrase')
        user_passphrase = VaultHash.hash(user_passphrase)
        if not user_passphrase or not upload_files:
            self.redirect('/')
            return
        blob_info = upload_files[0]
        logging.error(blob_info)
        passphrase = Passphrase(blob=blob_info.key(), passphrase=user_passphrase)
        passphrase.put()
        self.redirect('/success')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info, save_as=True)

class SuccessHandler(BaseHandler):
    def get(self):
        self.render('success.html')

app = webapp2.WSGIApplication([('/', FrontPageHandler), 
                               ('/serve/([^/]+)?', ServeHandler), 
                               ('/upload', UploadHandler), 
                               ('/success', SuccessHandler), 
                               ('/stash', StashHandler)
                              ], debug=True)
