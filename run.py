import re
import pyEX
from flask import Flask, request, render_template, jsonify

# The results will be cached in memory until reload.
# In case we need uncached version, results and tickers should be moved in the request.

iexCloud = pyEX.Client(
    api_token='Tpk_1e8fef17ee254009a45873d2c1b76828',
    version='sandbox'
)

results = iexCloud.symbols()

tickers = [
    dict(
        symbol=r['symbol'],
        name=r['name'],
    ) for r in results
]

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/tickers')
def tickers_search():
    search = request.args.get('s')
    search_results = []
    for t in tickers:
        if re.match(search, t['symbol'], re.I):
            search_results.append(t)
        if len(search_results) == 10:
            break
    return jsonify(search_results)


if __name__ == '__main__':
    app.run()
