from datetime import datetime
from flask import render_template
from flask import make_response
from flask import jsonify
from app import app
from ssis import monitor
import urllib

# Set app version 
version = "0.6.1 (beta)"

# Define routes
@app.route('/')
def all():
    return package()

@app.route('/folder/<folder_name>/project/<project_name>/status/<status>')
def folder_project_status(folder_name, project_name, status):
    return package(folder_name = folder_name, project_name = project_name, status = status)

@app.route('/folder/<folder_name>/project/<project_name>')
def folder_project(folder_name, project_name):
    return package(folder_name = folder_name, project_name = project_name)

@app.route('/folder/<folder_name>')
def folder(folder_name):
    return package(folder_name = folder_name)

@app.route('/<folder_name>/<project_name>/<status>/<int:execution_id>')
@app.route('/folder/<folder_name>/project/<project_name>/status/<status>/execution/<int:execution_id>')
def package(folder_name = monitor.all, project_name = monitor.all, status = monitor.all, execution_id = monitor.all):
    folder_name = urllib.unquote(folder_name) 
    project_name = urllib.unquote(project_name) 

    m = monitor()
    m.folder_name = folder_name
    m.project_name = project_name
    m.status = status
    m.execution_id = execution_id

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'execution_id': execution_id,
        'project_name': project_name,
        'folder_name': folder_name,
        'status': status
        }

    engine_folders = m.get_engine_folders()
    engine_projects = m.get_engine_projects()
    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_list = m.get_package_list()
    package_executables = m.get_package_executables()
    package_children = m.get_package_children()

    return render_template(
        'index.html',
        environment = environment,
        engine_folders = engine_folders,
        engine_projects = engine_projects,
        engine_info = engine_info,
        engine_kpi = engine_kpi,
        package_info = package_info,
        package_kpi = package_kpi,
        package_list = package_list,
        package_children = package_children,
        package_executables = package_executables
    )

@app.route('/execution/<int:execution_id>/details/<detail_type>')
def package_details(execution_id, detail_type):
    m = monitor()
    m.execution_id = execution_id

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'execution_id': execution_id,
        }

    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_details = m.get_package_details(detail_type)

    return render_template(
        'details.html',
        environment = environment,
        engine_info = engine_info,
        package_info = package_info,
        package_kpi = package_kpi,
        package_details = package_details
    )

@app.route('/folder/<folder_name>/project/<project_name>/status/<status>/package/<package_name>/country/<pckg_country>')
def package_history(folder_name, project_name, status, package_name, pckg_country):
    folder_name = urllib.unquote(folder_name) 
    project_name = urllib.unquote(project_name) 
    package_name = urllib.unquote(package_name)
    package_country = urllib.unquote(pckg_country) 

    m = monitor()
    m.project_name = project_name
    m.package_name = package_name
    m.folder_name = folder_name 
    m.package_country = package_country

    environment = {
        'version': version,
        'timestamp': datetime.now(),
        'folder_name': folder_name,
        'project_name': project_name,
        'package_name': package_name,
        'package_country':package_country,
        'status': status
        }

    engine_kpi = m.get_engine_kpi()
    engine_info = m.get_engine_info()
    package_info = m.get_package_info()
    package_kpi = m.get_package_kpi()
    package_history = m.get_package_history()

    return render_template(
        'history.html',
        environment = environment,
        engine_info = engine_info,
        package_info = package_info,
        package_kpi = package_kpi,
        package_history = package_history
    )

#@app.route('/tasks', methods = ['GET'])
#def get_tasks():
#    return services.get_tasks()

#@app.route('/tasks/<int:task_id>', methods = ['GET'])
#def get_task(task_id):
#    return services.get_task(task_id)

#@app.route('/ssis/execution-status', methods = ['GET'])
#def get_statuses():
#    execution_status = services.get_package_execution_status()
#    return jsonify ( { 'data': execution_status } )

#@app.route('/<int:execution_id>/execution-history', methods = ['GET'])
#def get_execution_history():
#    history = services.get_package_execution_history()
#    return jsonify ( { 'data': history } )

#@app.route('/ssis/execution-events/<int:execution_id>', methods = ['GET'])
#def get_package_execution_events(execution_id):
#    execution_events = services.get_package_execution_events(execution_id)
#    return jsonify ( { 'data': execution_events } )

#@app.route('/ssis/execution-kpi/<int:execution_id>', methods = ['GET'])
#def get_package_execution_kpi(execution_id):
#    kpi = services.get_package_execution_kpi(execution_id)
#    return jsonify( { 'data': kpi } )

#@app.route('/sample', methods = ['GET'])
#def get_sample():
#    return jsonify({'result': 123})

@app.errorhandler(404)
def not_found(error):
    environment = {
        'version': version,
        'timestamp': datetime.now()
        }

    return render_template(
        '404.html',
        environment = environment        
    )

