'''Panintelligence 2021 - EFS lambda copy utility'''

import os
import logging
import shutil

import boto3


logger = logging.getLogger() # pylint: disable=C0103
logger.setLevel(logging.INFO)

def get_bucket_name(record):
    '''retrieve bucket name from s3 triggered event'''
    try:
        return record['s3']['bucket']['name']
    except KeyError as key_error:
        logger.error('Unable to find "name" key in record bucket')
        raise Exception from key_error

def get_object_key(record):
    '''retrieve object key from s3 triggered event'''
    try:
        return record['s3']['object']['key']
    except KeyError as key_error:
        logger.error('Unable to find "key" key in record object')
        raise Exception from key_error
    return record['s3']['object']['key']

def get_object_type(record):
    '''The part before the first / forms the object type and will decide
    where it loads to (if it can be loaded)'''
    allowed_types = os.environ.get('allowed_types', '').split(',')
    try:
        key = record['s3']['object']['key']
        if '/' in key:
            file_type = key[0:key.find('/')]
            if file_type in allowed_types:
                return file_type
            error = 'file_type not found in allowed types'
            logger.error(error)
            raise Exception(error)
        logger.error('unable to find separator')
        raise Exception('could not determine what the record file_type is')
    except KeyError as key_error:
        logger.error('Unable to find "key" for record file_type')
        raise Exception from key_error

def get_file_name_from_object_key(object_key, separator='/'):
    '''retrieves the file name from the object'''
    logger.info("Grabbing object key")
    logger.info("object key data: %s", object_key)
    #return object_key
    if separator in object_key:
        path = object_key.split(separator)
        logger.info(path)
        file_name = path.pop()
        full_path = os.path.join(file_name)
        logger.info("object full path dir : %s", full_path)
        return full_path
    logger.error('Could not find separator in %s', object_key)
    raise Exception(f'could not find separator {separator} in {object_key}')

def get_dir_from_object_key(object_key, separator='/'):
    '''retrieves the file name from the object'''
    logger.info("Grabbing object key dir")
    logger.debug("object key data: %s", object_key)
    if separator in object_key:
        path = object_key.split(separator)
        logger.info(path)
        file_name = path.pop()
        file_type = path.pop(0)
        logger.info(path)
        try:
            full_path = os.path.join(file_type, *path, file_name)
            logger.debug("full path for dir object: %s", full_path)
            return full_path
        except TypeError as type_error:
            logger.warning("warning, issue with getting directory from object %s", type_error)
            full_path = os.path.join(file_type, file_name)
            return full_path
    logger.error('Could not find separator in %s', object_key)
    raise Exception(f'could not find separator {separator} in {object_key}')

def copy_file(source_file, target_file_name):
    '''copy the file from local system to efs volume'''
    logger.info('copying file from tmp to ')
    try:
        logger.info('copy_file target_file_name: %s', target_file_name)
        logger.info('copy_file source_file: %s', source_file)
        logger.info('efs local mount directory: %s', os.listdir("/mnt/efs"))
        target_file = os.path.join(os.path.sep, 'mnt/efs', target_file_name)
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            logger.info("Now copying files from %s to %s", source_file, target_file)
            logger.info('efs local mount directory: %s', os.listdir("/mnt/efs"))
            shutil.copyfile(source_file, target_file)
        except OSError as file_error:
            logger.info('efs local mount directory: %s', os.listdir("/mnt/efs"))
            logger.error("Error when copying file into efs")
            logger.error(file_error)
    except OSError as error:
        logger.error(error)
    except TypeError as type_error:
        logger.error("Error when copying file into efs there is an empty directory")
        logger.error(type_error)

class EfsTrigger:
    '''EFS lambda trigger code'''
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def download_from_s3(self, bucket_name, object_name, target_file_name):
        '''download object from s3 to store on /tmp'''
        logger.info('downloading from s3')
        try:
            target_name = os.path.join(os.path.sep, 'tmp', target_file_name)
            logger.info('download from s3 target name: %s', target_name)
            logger.info('download from s3 object name: %s', object_name)
            logger.info('download from s3 bucket name: %s', bucket_name)
            self.s3_client.download_file(bucket_name, object_name, target_name)
            return target_name
        except OSError as error:
            logger.error(error)
            raise Exception(f'could not find object_name {object_name} in {bucket_name}')

    def run_migrations(self, event):
        '''entry point for the program'''
        logger.info("Output of records: %s", event['Records'])
        for record in event['Records']:
            source_bucket = get_bucket_name(record)
            logger.info('this is the source_bucket %s ', source_bucket)
            file_type = get_object_type(record)
            logger.info('this is the file_type %s ', file_type)
            source_object_key = get_object_key(record)
            target_file_name = get_file_name_from_object_key(source_object_key)
            target_dir = get_dir_from_object_key(source_object_key)
            source_file = self.download_from_s3(source_bucket, source_object_key, target_file_name)
            copy_file(source_file, target_dir)

def main():
    ''' initialising lambda function'''
    return EfsTrigger()

def lambda_handler(event, context):
    '''call this from AWS'''
    del context
    efs_trigger = main()
    efs_trigger.run_migrations(event)

if __name__ == '__main__':
    lambda_handler(event={}, context={})
