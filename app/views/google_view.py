from flask_restful import Resource

import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

class GoogleView(Resource):
  def get(self):
    return {"message": "Hi google"}


class CallbackView(Resource):
  pass


class Logout(Resource):
  pass


class ProtectedArea(Resource):
  pass
