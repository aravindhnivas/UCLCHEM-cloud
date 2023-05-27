from flask import Flask, request, jsonify
from uclchem.src import uclchem
from pathlib import Path as pt
import os
from time import perf_counter

app = Flask(__name__)
output_dir = pt('./outputs')

@app.route("/")
def main():
    return "<h1>UCLCHEM API - Working!!</h1>"

@app.route("/api/simple_model", methods=['POST'])
def api():
    
    if not output_dir.exists():
        output_dir.mkdir()
        
    parameters: dict = request.get_json()
    out_species = parameters.pop('out_species') if 'out_species' in parameters else None
    
    for key in ['outputFile', 'abundSaveFile']:
        if key in parameters:
            parameters[key] = str(output_dir / parameters[key])
        else:
            parameters[key] = str(output_dir / f'{key}.dat')
    
    if 'out_species' in parameters:
        if not 'columnFile' in parameters:
            parameters['columnFile'] = str(output_dir / 'columnFile.dat')
    
    time_start = perf_counter()
    status, *abundances = uclchem.model.cloud(param_dict=parameters, out_species=out_species)
    final_time = perf_counter() - time_start
    
    if status < 0:
        return jsonify({'status': status, 'results': uclchem.utils.check_error(status)})
    
    results = {'status': status, 'results': {'abundaces': abundances}, 'time': final_time}
    
    df = uclchem.analysis.read_output_file(parameters['outputFile'])
    results['results']['full_output'] = df.to_json()
    
    if not 'element_list' in parameters:
        parameters['element_list'] = ['H', 'N', 'C', 'O', 'S']
    
    conservation=uclchem.analysis.check_element_conservation(df, element_list=parameters['element_list'])
    results['results']['conservation'] = conservation
        
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
