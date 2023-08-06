"""Interaction with the API of PhotoPrism"""

from photoprism import Session
import requests, json

class Photo():
    def __init__(self, session):
        """Initialize based upon a session"""
        if type(session) != Session.Session:
            raise TypeError(f"session variable is not of type photoprism.Session.Session, but {type(session)}")

        self.session = session
        self.header = {
            "X-Session-ID": self.session.session_id}


    def search(self, query, count=100):
        """Basic search function. Returns a Dict object based upon the returned JSON"""

        url = f"{self.session.url}/photos?count={count}&q={query}"
        r = requests.get(url, headers=self.header)
        return json.loads(r.text)

    def get_uid_list_of_search(self, query, count=100):
        """Return a list of UIDs based upon the search"""

        photos = self.search(query, count)
        photolist = []
        for ps in photos:
            photolist.append(ps["UID"])

        return photolist

    def list_albums(self):
        """Provide a list of all albums within the photoprism instance, with a max of 100000"""

        url = f"{self.session.url}/albums?count=100000"
        r = requests.get(url, headers=self.header)
        return json.loads(r.text)

    def check_if_album_exists(self, name, create_if_not=False):
        """Small function to check if an album exists"""

        data = self.list_albums()
        for d in data:
            if name == d["Title"]:
                return True

        if create_if_not:
            self.create_album(name)

        return False

    def get_album_uid_by_name(self, name):
        """Get the UID of an album using the name of the album. Be aware, it uses the list_albums function that is limited to 100000 albums"""

        data = self.list_albums()
        uid = None
        for d in data:
            if name == d["Title"]:
                return d["UID"]
        
        return False

    def create_album(self, title):
        """Create an album, returns a boolean if it worked"""

        url = f"{self.session.url}/albums"
        data = {"Title":title,"Favorite":False}
        r = requests.post(url=url, data=json.dumps(data), headers=self.header)
        
        if r.status_code == 200:
            return True
        
        return False

    def add_photos_to_album(self, photos, album_uid):
        """Add photos to an album, you will need to provide a list of UIDs of the photos you want to add. Returns True if successfull"""

        url = f"{self.session.url}/albums/{album_uid}/photos"
        data = {
            "photos":photos
        }
        r = requests.post(url, data=json.dumps(data), headers=self.header)
        
        if r.status_code == 200:
            return True

        return False

    def add_to_album_from_query(self, query, albumname):
        """Provide a search query and add all photos that are returned into an album. Provide the albumname, not the UID of the album."""

        self.check_if_album_exists(albumname, create_if_not=True)
        album_uid = self.get_album_uid_by_name(albumname)
        photolist = self.get_uid_list_of_search(query, count=1000000)
        result = self.add_photos_to_album(photolist, album_uid)
        return result

    def get_album(self, uid):
        """Get all information of an album based upon the UID of the album"""

        url = f"{self.session.url}/albums/{uid}"
        r = requests.get(url, headers=self.header)
        
        if r.status_code == 200:
            return json.loads(r.text)
        
        return False

    def remove_photos_from_album(self,albumname, photos=False, count=1000000):
        """Remove photos from an album, Returns True if successfull"""
        album_uid = self.get_album_uid_by_name(albumname)
        if photos == False:
            query = f"album:\"{albumname}\""
            photos = self.get_uid_list_of_search(query,count=count)

        url = f"{self.session.url}/albums/{album_uid}/photos"
        data = {
            "photos":photos
        }
        r = requests.delete(url, data=json.dumps(data), headers=self.header)
        result = False
        if r.status_code == 200:
            result = True
        return result

    def remove_album(self, albumname):
        """Remove album based on album name"""
        album_uid = self.get_album_uid_by_name(albumname)
        url = f"{self.session.url}/albums/{album_uid}"
        r = requests.delete(url, headers=self.header)
        result = False
        if r.status_code == 200:
            result = json.loads(r.text)
        return result

    def start_import(self, path="upload", move=False):
        """Start an import job, default path is upload. It returns True when the import started, not when finished"""

        url = f"{self.session.url}/import"
        data = {
            "path": path,
            "move": move
        }
        r = requests.post(url, data=json.dumps(data), headers=self.header)
        
        if r.status_code == 200:
            return True
        
        return False

    def stop_import(self):
        """Stop an import job"""
        url = f"{self.session.url}/import"
        r = requests.delete(url, headers=self.header)

        if r.status_code == 200:
            return True
        
        return False

    def raw_call(self, endpoint, type="GET", data=None):
        """Function to perform a request to the photoprism server"""

        url = f"{self.session.url}/{endpoint}"
        if type == "GET":
            return requests.get(url, headers=self.header)
        elif type == "POST":
            return requests.post(url, data=json.dumps(data) if data else None, headers=self.header)
        elif type == "DELETE":
            return requests.delete(url, headers=self.header)
        
        return False
