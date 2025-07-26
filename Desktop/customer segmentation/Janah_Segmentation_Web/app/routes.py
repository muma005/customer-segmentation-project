from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/segmentation')
def segmentation():
    return render_template('segmentation.html')

@main.route('/results')
def results():
    return render_template('results.html')
