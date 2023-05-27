from flask import Flask, request, jsonify
import os
from uclchem.src import uclchem
app = Flask(__name__)

@app.route("/api/simple_model", methods=['POST'])
def api():
    data: dict = request.get_json()
    out_species = data.pop('out_species') if 'out_species' in data else None
    status, *abundances = uclchem.model.cloud(param_dict=data, out_species=out_species)
    return jsonify({'result': status, 'abundances': abundances})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
