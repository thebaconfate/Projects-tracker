"""Workhours project."""
__version__ = "0.1.0"
import os
from src.routes import bp
from dotenv import load_dotenv
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    return app
