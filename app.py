from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import flask 
from subprocess import Popen, PIPE
from flask import send_from_directory
from socket import gethostname
from pipes import quote

app = flask.Flask(__name__)

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route('/')
def main():
  return flask.redirect('/index')

@app.route('/index')
def index():
    # handle user args
    args = flask.request.args
    query = getitem(args, 'searchbox', '')
    cs = getitem(args, 'caseSensitive', '')
    hostname = gethostname()
    if query == '':
        resultslist = ''
    else:
        if cs != 'on':
            cs = "-i "
        else:
            cs = ""
        command = 'mlocate ' + cs + quote(query)
        with Popen(command, shell=True, stdout=PIPE) as proc:
            outs = proc.stdout.read()
        results = outs.splitlines()
        resultslist = ""
        for entry in results:
            resultslist = resultslist + "<li>" + entry.decode('utf-8') + "</li>"

    html = flask.render_template(
        'index.html',
        resultslist=resultslist,
        hostname=hostname)
    return html

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

if __name__ == '__main__':
    port = 5000
    app.run(debug=False,host='0.0.0.0',port=port)   