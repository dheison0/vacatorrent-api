from os import getenv
from flask import Flask

PORT = int(getenv("PORT", "5000"))

app = Flask(__name__)
