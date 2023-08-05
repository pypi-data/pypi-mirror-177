from flask import Flask, jsonify


app = Flask("test-ms")



from .test import start_testing
start_testing()