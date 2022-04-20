# from curses import raw
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_entries, get_single_entry, delete_entry, create_entry, get_entries_by_search, update_entry, get_all_moods, get_all_tags


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
    
    
    def parse_url(self, path):
        """Parses the URL into separate strings and returns them in a tuple to use in the relevant method"""
        
        path_params = path.split("/")
        resource = path_params[1]

        
        if "?" in resource:
        

            param = resource.split("?")[1]  
            resource = resource.split("?")[0]  
            pair = param.split("=")
            key = pair[0]
            value = pair[1]
            
            
            try:
                value = int(value)
            except IndexError:
                pass
            except ValueError:
                pass
    
            return ( resource, key, value )

        else:
            id = None
    
            try:
                id = int(path_params[2])            
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)
    
    def _set_headers(self, status):
        """
        Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def do_GET(self):
        
        self._set_headers(200)

        response = {}


        parsed = self.parse_url(self.path)

        if len(parsed) == 2:

            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"
            elif resource == "tags":
                response = f"{get_all_tags()}"

        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            if key == "q" and resource == "entries":
                response = f"{get_entries_by_search(value)}"

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
                
        content_len = int(self.headers.get('content-length', 0)) 
        
        post_body = self.rfile.read(content_len) 
        
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        response = None

        if resource == "entries":
            response = create_entry(post_body)

        self.wfile.write(f"{response}".encode()) 

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)

        if success:
            self._set_headers(200)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """This method handles delete requests
        """
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)
        if resource == "customers":
            delete_customer(id)
        if resource == "employees":
            delete_employee(id)
        if resource == "locations":
            delete_location(id)

        self.wfile.write("".encode())

def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()