import random
import string

PLATFORM = "tifeblue"
MODEL_PREFIX = "model"
DATASET_PREFIX = "dataset"
WORKFLOW_PREFIX = "workflow"
OP_PREDIX = "operator"
ENV = "CORP"


def info2urn_query(query: str = None,
                   namespace: str = None,
                   name: str = None,
                   version: str = None,
                   count: int = 10):
    query = ""
    if namespace is not None:
        query += namespace
    if name is not None:
        query += ".%s" % (name)
    if version is not None:
        query += ".%s" % (version)
    if query is not None:
        query = query
    urn_query = """query{
            searchAcrossEntities(
                input:{
                    query:"%s",
                    start:0,
                    count:%d
                }
            ){
                searchResults{
                    entity{
                        urn,
                    }
                }
            }
    }""" % (query, count)
    return {"query": urn_query.strip()}


def dataset_urn_query(urn: str):
    return {
        "query":
        """query{
        dataset(
            urn:"%s"
        ){
            properties{
            name,
            customProperties{
                key,
                value
            }
            }
        }
}
""" % (urn).strip()
    }


def get_auto_name(len: int = 4):
    return "".join(random.sample(string.ascii_letters, len))


def container_urn_query(urn: str):
    return {
        "query":
        """"query{
  container(urn:"%s"){
    entities(
      input:{
        query:"*",
      }){
      searchResults{
        entity{
          urn,
        }
      }
    }
  } 
}""" % (urn).strip()
    }



