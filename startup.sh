#!/bin/sh
gunicorn --bind 0.0.0.0:80 propalyzer_site.wsgi