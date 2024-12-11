from flask import jsonify , Response , request
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from db import mongo  
from bson.objectid import ObjectId
from config import Config
s3 = boto3.client('s3',
                  aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=Config.AWS_SECRET_KEY,
                  )

BUCKET_NAME = 'indica-ai'

class file_contollers:
    def fetch_files_and_add_to_db():
        try:
            response = s3.list_objects_v2(Bucket=BUCKET_NAME )
            
            if 'Contents' not in response:
                return jsonify({'error': 'No files'}), 404

            files = []
            for obj in response['Contents']:
                video_url = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']},
                                                    ExpiresIn=8600)
                files_meta = {
                    'file_name': obj['Key'],
                    
                    'file_size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'link': video_url,
                    "metadata": response["ResponseMetadata"]
                }
                
                file_info = {
    'file_name': files_meta['file_name'],
    'file_size': files_meta['file_size'],
    'last_modified': files_meta['last_modified'],
    'link': files_meta['link'],
     }

                files.append(file_info)


            
                existing_file = mongo.db.metadata.find_one({'file_name': obj['Key']})
                if not existing_file:
                
                    result = mongo.db.metadata.insert_one(files_meta)
                    files_meta['_id'] = str(result.inserted_id)
                    file_info['_id'] = str(existing_file['_id'])
                else:
                    files_meta['_id'] = str(existing_file['_id'])
                    file_info['_id'] = str(existing_file['_id'])
                
            
            
            return jsonify(files), 200

        except (NoCredentialsError, PartialCredentialsError):
            return jsonify({'error': 'Credentials not found or incomplete'}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 500


        
    def fetch_file_by_id():
        try:
           
            file_id = request.args.get('id') 
            
            if not file_id:
                return jsonify({'error': 'File ID is required'}), 400

           
            if not ObjectId.is_valid(file_id):
                return jsonify({'error': 'Invalid file ID'}), 400

           
            file = mongo.db.metadata.find_one({'_id': ObjectId(file_id)})
            
            if not file:
                return jsonify({'error': 'File not found'}), 404

           
            return jsonify({
                'file_name': file['file_name'],
                'file_size': file['file_size'],
                'last_modified': file['last_modified'],
                'link': file['link'],
                'metadata': file['metadata']
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

    def search_files_by_name():
            try:
                search_query = request.args.get('query')

                if not search_query:
                    return jsonify({'error': 'queru missing'}), 400

                files = mongo.db.metadata.find({
                    'file_name': {'$regex': search_query, '$options': 'i'}  
                })

                result = []
                for file in files:
                    result.append({
                        '_id': str(file['_id']),
                        'file_name': file['file_name'],
                        'file_size': file['file_size'],
                        'last_modified': file['last_modified'],
                        'link': file['link'],
                        'metadata': file['metadata']
                    })

                if not result:
                    return jsonify({'error': 'No files '}), 404

                return jsonify(result), 200

            except Exception as e:
                return jsonify({'error': str(e)}), 500
