from flask import Blueprint
from contollers.file_controller import file_contollers

file_routes = Blueprint('file_routes', __name__)

file_routes.route('/fetch_files', methods=['GET'])( file_contollers.fetch_files_and_add_to_db)
file_routes.route('/fetch_file_by_id', methods=['GET'])(file_contollers.fetch_file_by_id)
file_routes.route('/fetch_file_by_name', methods=['GET'])(file_contollers.search_files_by_name)