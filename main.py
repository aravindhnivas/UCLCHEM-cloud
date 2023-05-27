from flask import Flask, request, jsonify
from uclchem.src import uclchem
from pathlib import Path as pt
import os


app = Flask(__name__)
output_dir = pt('./outputs')

@app.route("/")
def main():
    return "<h1>UCLCHEM API - Working!!</h1>"

@app.route("/api/simple_model", methods=['POST'])
def api():
    parameters: dict = request.get_json()
    out_species = parameters.pop('out_species') if 'out_species' in parameters else None
    
    for key in ['outputFile', 'abundSaveFile']:
        if key in parameters:
            if not output_dir.exists():
                output_dir.mkdir()
            parameters[key] = str(output_dir / parameters[key])
            
    status, *abundances = uclchem.model.cloud(param_dict=parameters, out_species=out_species)
    
    if status < 0:
        return jsonify({'status': status, 'results': uclchem.utils.check_error(status)})
    
    results = {'status': status, 'results': {'abundaces': abundances}}
    
    if 'outputFile' in parameters:
        df = uclchem.analysis.read_output_file(parameters['outputFile'])
        results['results']['full_output'] = df.to_json()
        
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
