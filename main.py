from flask import Flask, request, jsonify
import os
from uclchem.src import uclchem
app = Flask(__name__)

@app.route("/")
def main():
    return "<h1>UCLCHEM API - Working</h1>"

@app.route("/api/simple_model", methods=['POST'])
def api():
    data: dict = request.get_json()
    out_species = data.pop('out_species') if 'out_species' in data else None
    status, *abundances = uclchem.model.cloud(param_dict=data, out_species=out_species)
    
    if status < 0:
        return jsonify({'status': status, 'results': uclchem.utils.check_error(status)})
        
    return jsonify({'status': status, 'results': {'abundaces': abundances}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
