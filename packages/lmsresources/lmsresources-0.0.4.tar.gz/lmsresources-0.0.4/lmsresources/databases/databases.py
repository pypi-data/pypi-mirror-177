"""
This handles all the work regardint the mongo database.
"""
from django.conf import settings
from pymongo import MongoClient


def get_mongo_client():
    """
    Creates and return database client for the MongoDB.
    """
    return MongoClient(settings.MONGO_URI)[settings.MONGO_DATABASE]


def get_database_client(database):
    """
    Creates and return database client for the MongoDB.
    """
    return MongoClient(settings.MONGO_URI)[database]


def get_modules_collection():
    """
    Get modules collection of mongo database.
    """
    client = get_database_client()
    return client[settings.MODULES_COLLECTION]


def get_trainings_collection():
    """
    Get modules collection of mongo database.
    """
    client = get_database_client()
    return client[settings.TRAININGS_COLLECTION]


def get_trainings_data_collection():
    """
    Get modules collection of mongo database.
    """
    client = get_database_client()
    return client[settings.TRAININGS_DATA_COLLECTION]


def get_modules(query={}):
    """
    Get all training Modules.
    """
    col = get_modules_collection()
    cur = col.find(query, {'_id': 0})
    return list(cur)


def get_module(query):
    """
    Get single module
    """
    col = get_modules_collection()
    module = col.find_one(query, {'_id': 0})
    return module


def get_trainings(module):
    """
    Get Trainings for a module.
    """
    col = get_trainings_collection()
    cur = col.find({"module": module}, {'_id': 0})
    return list(cur)


def get_training(query):
    """
    Get training for a module
    """
    col = get_trainings_collection()
    training = col.find_one(query, {'_id': 0})
    return training


def get_training_data(training):
    """
    Get module Traning data for a training.
    """
    col = get_trainings_data_collection()
    cur = col.find({"training": training}, {'_id': 0})
    return list(cur)


def get_trainings_count():
    """
    Get trainings count.
    """
    col = get_trainings_data_collection()
    return col.count_documents({})


def get_training_questions_count(question_type):
    col = get_trainings_data_collection()
    trainings_data = col.find({}, {'_id': 0})
    question_type_count = 0
    for training_data in list(trainings_data):
        for question in training_data["questions"]:
            if question["type"] == question_type:
                question_type_count += 1
    return question_type_count


def get_collection(name: str, database: str):
    """
    Return the collection with the param name.
    """
    client = get_database_client(database=database)
    return client[name]


def get_data(col, query: dict):
    """
    Filter and return the related data.
    """
    cur = col.find(query, {"_id": 0})
    return list(cur)


def get_data_aggregate(col, query: list):
    """
    Filter and return the related data.
    """
    cur = col.aggregate(query)
    data = list(cur)
    for i in range(len(data)):
        del data[i]['_id']
    return data


def get_clean_data(col, query: dict):
    """
    Filter and return the related data.
    """
    cur = col.find(
        query,
        {
            "_id": 0,
            "created_on": 0,
            "created_by": 0,
            "updated_on": 0,
            "updated_by": 0,
            "deleted_on": 0,
            "deleted_by": 0,
        },
    )
    return list(cur)


def get_video_data(col, query: dict):
    """
    Filter and return the related data.
    """
    cur = col.find(query, {"_id": 0, "steps": 0, "classroom-setup": 0,
                   "Resources Needed": 0, "SLOs Covered - SNC": 0, "External Links": 0, "type": 0})
    return list(cur)