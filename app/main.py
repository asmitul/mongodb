import logging
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

LOGS_LOCATE = os.getenv("LOGS_LOCATE","LOCAL")

if LOGS_LOCATE == "LOCAL":
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    logging.basicConfig(
        filename=f"./app/logs/{current_date}.log",
        format="%(asctime)s %(levelname)s %(message)s",
        level=os.getenv("LOGGING_LEVEL")
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

if LOGS_LOCATE == "REMOTE":
    client = MongoClient(f'mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/?authMechanism=DEFAULT')
    db_logs = client[os.getenv("APP_NAME")+os.getenv("MONGODB_LOGS_DATABASE_NAME")]
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    collection_logs = db_logs["log_"+current_date]

    logger = logging.getLogger(__name__)
    logger.setLevel(os.getenv("LOGGING_LEVEL"))

    class MongoDBhandler(logging.Handler):
        def emit(self, record):
            from datetime import datetime
            record.created = datetime.now().isoformat()
            collection_logs.insert_one(record.__dict__)

    logger.addHandler(MongoDBhandler())

client = MongoClient(f'mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/?authMechanism=DEFAULT')
db = client[os.getenv("APP_NAME")+os.getenv("MONGODB_DATABASE_NAME")]

def insert_one(collection, document):
    try:
        result = db[collection].insert_one(document)
        logger.debug("Inserted document ID: %s" % result.inserted_id)
        return result
    except Exception as e:
        logger.error("Error inserting document: %s" % str(e))
        raise

def insert_many(collection, documents):
    try:
        result = db[collection].insert_many(documents)
        logger.debug(f"Inserted documents ID: {result.inserted_ids}")
        return result
    except Exception as e:
        logger.error(f"Error inserting documents: {e}")
        raise

def replace_one(collection, filter, replacement):
    try:
        result = db[collection].replace_one(filter=filter, replacement=replacement)
        logger.debug("Matched Count: {}".format(result.matched_count))
        logger.debug("Modified Count: {}".format(result.modified_count))
        logger.debug("upserted_id: {}".format(result.upserted_id))
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def update_one(collection, filter, update):
    try:
        result = db[collection].update_one(filter=filter, update=update)
        logger.debug("Matched Count: {}".format(result.matched_count))
        logger.debug("Modified Count: {}".format(result.modified_count))
        logger.debug("upserted_id: {}".format(result.upserted_id))
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def update_many(collection, filter, update):
    # example 
    # filter = {"age":{"$gt":20}}
    # update = {"$set":{"status":"active"}}
    try:
        result = db[collection].update_many(filter=filter, update=update)
        logger.debug("Matched Count: {}".format(result.matched_count))
        logger.debug("Modified Count: {}".format(result.modified_count))
        logger.debug("upserted_id: {}".format(result.upserted_id))
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def delete_one(collection, filter):
    try:
        result = db[collection].delete_one(filter=filter)
        logger.debug("Deleted Count: {}".format(result.deleted_count))
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def delete_many(collection, filter):
    try:
        result = db[collection].delete_many(filter=filter)
        logger.debug("Deleted Count: {}".format(result.deleted_count))
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def find(collection):
    try:
        result = db[collection].find()
        for document in result:
            logger.debug(document)
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def find_one(collection, filter):
    try:
        result = db[collection].find_one(filter=filter)
        logger.debug(result)
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def find_one_and_delete(collection, filter):
    try:
        result = db[collection].find_one_and_delete(filter=filter)
        logger.debug(result) # not find return None , find return document and delete
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def find_one_and_replace(collection, filter, replacement):
    try:
        result = db[collection].find_one_and_replace(filter=filter, replacement=replacement)
        logger.debug(result)
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise

def find_one_and_update(collection, filter, update):
    try:
        result = db[collection].find_one_and_update(filter=filter, update=update)
        logger.debug(result)
        return result
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        raise
    
if __name__ == "__main__":
    find_one({"_id": ObjectId("60a6f3f3a5b4e3b0b4e3b0b4e")})
    
    # filter = {"age":{"$gt":35}}
    # update = {"$set":{"status":"active"}}
    # document = {
    #     "name": "Test20",
    #     "age": 35
    # }
    # delete_one(filter=document)