
import os
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3 import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
import urllib.parse
import requests

from typing import Optional, List

from pydantic import BaseModel, ValidationError, validator,   Field
from array import array
from pydantic import condecimal
import json
from time import time, sleep
import enum
import hnswlib

JIGGY_HOST    = os.environ.get("JIGGY_HOST", "https://api.jiggy.ai")
JIGGY_VERSION = os.environ.get("JIGGY_VERSION", "jiggy-v0")


class ClientError(Exception):
    """
    API returned 4xx client error
    """

class ServerError(Exception):
    """
    API returned 5xx Server error
    """

class IndexError(Exception):
    """
    Index creation failed
    """
    


class JiggySession(requests.Session):
    def __init__(self, prefix_url, *args, **kwargs):
        super(JiggySession, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url
        self.bearer_token = None
        super(JiggySession, self).mount('https://',
                                        HTTPAdapter(max_retries=Retry(connect=5,
                                                                      read=5,
                                                                      status=5,
                                                                      redirect=2,
                                                                      backoff_factor=.001,
                                                                      status_forcelist=(500, 502, 503, 504))))

    def _set_bearer(self, jwt):
        self.bearer_token = jwt
        self.headers['Authorization'] = f"Bearer {jwt}"

    def _getjwt(self, key):
        resp = requests.post(self.prefix_url+"/auth", json={'key': key})
        if resp.status_code == 200:
            self._set_bearer(resp.json()['jwt'])
        elif resp.status_code == 401:
            raise ClientError("Invalid API Key")
        else:
            raise ServerError(resp.content)
        
    def _auth(self):
        if 'JIGGY_API_KEY' in os.environ:
            self._getjwt(os.environ['JIGGY_API_KEY'])
            return
        print("JIGGY_API_KEY environment variable is not set")
        print("Enter an existing API Key, or your email address to create an account:")
        while True:
            key_or_email = input("API Key or Email: ")
            if key_or_email[:4] == "jgy-":
                # try using the key to see if it is valid
                try:
                    self._getjwt(key_or_email)
                    break
                except:
                    print("Invalid API Key")
                    continue
            elif '@' in key_or_email:
                # create a key in exchange for what what might be the user's email address
                username = key_or_email.split('@')[0]
                resp = requests.post(self.prefix_url+"/apiuser", json={'email': key_or_email, 'username': username})
                if resp.status_code != 200:
                    raise ServerError(resp.content)
                key = resp.json()['key']
                os.environ['JIGGY_API_KEY'] = key
                print("\nA new API key has been created for you.")
                print(f"JIGGY_API_KEY:  {key}")
                print("Please store it in a safe place.")
                print("Set JIGGY_API_KEY environment variable to use it, e.g.:")
                print(f"\nexport JIGGY_API_KEY={key}\n")
                input("Hit enter to continue: ")
                self._getjwt(key)


                                         
    def request(self, method, url, *args, **kwargs):
        if not self.bearer_token:
            self._auth()
        url = self.prefix_url + url
        #print("~~~~~~~~~~~~~~~~~~~~~~~~\n", method, url)
        resp =  super(JiggySession, self).request(method, url, *args, **kwargs)
        if resp.status_code == 401:
            self.bearer_token = None
            del self.headers['Authorization']
            self._auth()
            resp =  super(JiggySession, self).request(method, url, *args, **kwargs)
        if resp.status_code in [500, 502, 503, 504]:
            pass # TODO: retry these cases        
        if resp.status_code >= 500:
            raise ServerError(resp.content)
        if resp.status_code >= 400:
            raise ClientError(resp.content)
        return resp


session = JiggySession(prefix_url = JIGGY_HOST + '/' + JIGGY_VERSION)
    


class IndexLibraries(str, enum.Enum):
    """
    The library used to create the index.
    Currently only 'hnswlib' is supported.
    """
    hnswlib = 'hnswlib'


class DistanceMetric(str, enum.Enum):
    """
    The distance metric to use for the nearest neighbor index.
    """
    cosine = 'cosine'
    ip     = 'ip'
    l2     = 'l2'

class IndexBuildState(str, enum.Enum):
    prep = "preparing data"
    indexing = "indexing vectors"
    saving = "saving index"
    complete = "index complete"
    failed = "indexing failure"

    
class Collection(BaseModel):
    
    id:    int = Field(description='Unique identifier for a particular collection.')
    name:  str = Field(description="The Collection's unique name within the team context.")

    dimension: int         = Field(default= 0, description="The dimension of the vectors in this collection.")
    team_id:   int         = Field(None, index=True, description="The team that this collection is associated with.")
    count: int             = Field(default=0, description="The number of vectors in the collection")
    created_at: float = Field(description='The epoch timestamp when the collection was created.')
    updated_at: float = Field(description='The epoch timestamp when the collection was updated.')
       
    def add(self, vector_data:[float], vector_id:int):
        """
        Add the specified vector_data to the collection and associate it with the specified vector_id.
        A collection may not have more than one vector with a given vector_id.
        Re-using a vector_id will over-write any existing  vector_id +  vector pair.
        All vectors in a collection must share the same dimension.
        """
        vector_data = [float(x) for x in vector_data]
        session.post(f"/collections/{self.id}/vectors/{vector_id}", json={'vector': vector_data})
        if not self.dimension:
            self.dimension = len(vector_data)  # record dimension

    def get(self, vector_id : int):
        """
        Return the vector with the specified vector_id from the collection
        """
        resp = session.get(f"/collections/{self.id}/vectors/{vector_id}")
        return resp.json()['vector']
        
    def delete(self, vector_id : int):
        """
        Delete the vector with the specified vector_id from the collection
        """        
        session.delete(f"/collections/{self.id}/vectors/{vector_id}")
        
    def create_index(self,
                     tag='latest',
                     target_library=IndexLibraries.hnswlib,
                     metric=DistanceMetric.cosine,
                     target_recall=None,
                     M=None,
                     ef=None):
        body = {'tag': tag,
                'target_library': target_library,
                'metric': metric,
                'target_recall': target_recall,
                'hnswlib_M':  M,
                'hnswlib_ef': ef}
        resp = session.post("/collections/%d/index" % self.id, json=body)
        return Index(**resp.json(), collection=self)
                                                            
    def delete_collection(self):
        """
        Delete the collection.
        """
        resp = session.delete("/collections/%s" % self.id)
        self.id=None
        self.name= None
        self.created_at=None
        self.updated_at=None
        self.team_id=None
        self.dimension=None


    def get_index(self, tag:str="latest"):
        data = {'tag': tag}
        resp = session.get(f"/collections/{self.id}/index?{urllib.parse.urlencode(data)}")
        items = resp.json()['items']
        if tag and items:
            return Index(**items[0], collection=self)
        return [Index(**i, collection=self) for i in items]

    def get_all_index(self):
        return self.get_index(None)

    def _update(self):
        resp = session.get(f"/collections/{self.id}")
        self.__dict__.update(resp.json())
        
    def __getattribute__(self, attr):
        if attr in ['count', 'updated_at']:
            self._update()
        return object.__getattribute__(self, attr)        

        
def create_collection(name:str, team_name=None):
    """
    Create a collection of the specified name
    Returns a Collection object.
    Raises ClientError if the specified name already exists

    'team_obj_or_name' is optional and can be either a team name or team object.
    if team is unspecified the user's default team will be used.
    """
    data = {'name': name}
    if team_name:
        data['team_id'] = team(team_name).id
    resp = session.post("/collections", json=data)
    return Collection(**resp.json())


def collection(name:str):
    """
    Get a collection by name.
    Returns a Collection Object, or None if collection name is not found
    """
    data = {'name': name}
    resp = session.get(f"/collections?{urllib.parse.urlencode(data)}")
    items = resp.json()['items']
    if len(items):
        return Collection(**items[0])
    raise Exception(f"Collection {name} not found")


def all_collections():
    resp = session.get("/collections")
    return [Collection(**i) for i in resp.json()['items']]


class Index(BaseModel):
    id: int            = Field(description='Unique identifier for a given index.')
    collection: Collection = Field(description="The containing collection")
    tag:  str = Field(description="User tag for this Index.  Uniquely identifies an index in the context of a collection.")
    name: str = Field(description="The full name for this index in the form of TEAM_NAME/COLLECTION_NAME:TAG")
    target_library:    IndexLibraries = Field(default=IndexLibraries.hnswlib, description="The library use to create the index")
    metric:        str = Field(description='The distance metric ("space" in hnswlib): "cosine", "ip", or "l2"')
    hnswlib_M:  Optional[int] = Field(default=None, description="The M value passed to hnswlib when creating the index.")
    hnswlib_ef: Optional[int]  = Field(default=None, description="The ef_construction value passed to hnswlib when creating the index.")
    hnswlib_ef_search: Optional[int] = Field(default=None, ge=10, description="The recommended ef value to use at search time.")
    target_recall: Optional[float] = Field(default=None, ge=0.5, le=1, description="The desired recall value to target for index parameter optimization.")        
    count: int = Field(description="The number of vectors included in the index.  The number of vectors in the collection at the time of index build.")
    created_at: float = Field(description='The epoch timestamp when the index was requested to be created.')
    state: IndexBuildState = Field(description = "The current build status.")
    completed_at: float = Field(description='The epoch timestamp when the index build was completed.')
    build_status: str     = Field(description='Informational status message for the index build.')
    url: Optional[str] = Field(default=None, description='The url the index can be downloaded from.  The url is valid for a limited time.')

    
    def _wait_complete(self):
        while self.state not in [IndexBuildState.failed, IndexBuildState.complete]:
            print(f"Index Status: {self.build_status}")  # XXX provide percentage completion
            data = {'tag': self.tag}
            resp = session.get (f"/collections/{self.collection.id}/index?{urllib.parse.urlencode(data)}")
            items = resp.json()['items'][0]
            self.__dict__.update(items)
            sleep(2)  # XXX update sleep time based on something like halfway toward the estimated remaining completed_at estimate
        if self.state == IndexBuildState.failed:
            raise IndexError(self.build_status)
        
            
    def hnswlib_index(self, max_elements:int = None):
        self._wait_complete()
        if not max_elements:
            max_elements = self.count
        resp = requests.get(self.url)
        assert(resp.status_code == 200)
        assert(int(len(resp.content)) == int(resp.headers['Content-Length']))
        fname = self.name.replace('/','-')
        fname += f".{self.target_library}"
        open(fname, 'wb').write(resp.content)
        ix = hnswlib.Index(space=self.metric, dim=self.collection.dimension)
        ix.load_index(fname, max_elements=max_elements)
        ef = self.hnswlib_ef_search if self.hnswlib_ef_search else self.hnswlib_ef
        ix.set_ef(ef)
        return ix


###
##  Teams
###
class Team(BaseModel):
    id: int = Field(description="Internal team id")
    name: str = Field(min_length=3, max_length=39, description='Unique name for this team.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')
    created_at: float = Field(description='The epoch timestamp when the team was created.')
    updated_at: float = Field(description='The epoch timestamp when the team was updated.')


def all_teams():
    """
    return all Teams that the user is a member of
    """
    resp = session.get("/teams")
    return [Team(**i) for i in resp.json()['items']]

def team(name):
    """
    get team by name
    raises Exception if an exact match for name is not found
    """
    team = [t for t in session.get("/teams").json()['items'] if t['name'] == name]
    if len(team):
        return Team(**team[0])
    raise Exception(f"Team '{name}' not found")


def init(host    = os.environ.get("JIGGY_HOST",    "https://api.jiggy.ai"),
         version = os.environ.get("JIGGY_VERSION", "jiggy-v0")):
    global session
    session = JiggySession(prefix_url = host + '/' + version)




