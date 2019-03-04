from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import flask
from subprocess import Popen, PIPE
from flask import send_from_directory
from socket import gethostname
from pipes import quote

MAX_RESULT_BYTES = 1000000  # set to -1 to disable limit

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
        results_truncated = False
    else:
        if cs != 'on':
            cs = "-i "
        else:
            cs = ""
        command = 'mlocate ' + cs + quote(query)
        command = command.encode('utf-8')
        with Popen(command, shell=True, stdout=PIPE) as proc:
            outs = proc.stdout.read(MAX_RESULT_BYTES)
        results = outs.splitlines()
        results_truncated = len(outs) == MAX_RESULT_BYTES
        if results_truncated:
            results = results[:-1]
        resultslist = ""
        for entry in results:
            resultslist = resultslist + "<li>" + entry.decode('utf-8') + "</li>"

    html = flask.render_template(
        'index.html',
        results_truncated=results_truncated,
        resultslist=resultslist,
        hostname=hostname)
    return html

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

if __name__ == '__main__':
    port = 5000
    app.run(debug=False,host='0.0.0.0',port=port)
