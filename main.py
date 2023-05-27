from flask import Flask, request, jsonify
import os
from uclchem.src import uclchem
from pathlib import Path as pt

app = Flask(__name__)
output_dir = pt('./outputs')

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
    
    results = {'status': status, 'results': {'abundaces': abundances}}
    
    if 'outputFile' in data:
        
        if not output_dir.exists():
            output_dir.mkdir()
            
        output_file = output_dir / data['outputFile']
        df = uclchem.analysis.read_output_file(output_file)
        results['results']['full_output'] = df.to_json()
        
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
