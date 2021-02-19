from flask import Flask, render_template, request, flash, redirect, session, g
from models import Follows, User, Lesson, Resource

app = Flask(__name__)

