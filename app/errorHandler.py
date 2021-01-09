from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

def handle_404(e):
    return render_template('404.html')