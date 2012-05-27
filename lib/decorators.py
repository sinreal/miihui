#coding:utf-8

from lib.kit import Auth
import web

def authenticate(handler):
  def _check_auth(*args,**kwargs):
      if Auth.is_login():
        return handler(*args,**kwargs)
      else:
        web.seeother("/login")
  return _check_auth
