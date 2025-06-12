**Lab1: Single-Threaded Python Web Server**
A minimal HTTP/1.1 server that serves files from its working directory over TCP.

**Features**

* Listens on a user-specified port
* Handles one client at a time
* Serves existing files with a “200 OK” + `Content-Type: text/html`
* Returns “404 Not Found” for missing files (including `/favicon.ico`)
* Prints each request and its outcome to the console

**Requirements**

* Python 3.x

**Usage**

1. Put `server.py` and any `.html` files (e.g. `HelloWorld.html`) in the same folder.
2. (Optional) add a `favicon.ico` if you want to avoid 404s on icon requests.
3. From that folder, run:

   ```bash
   python3 server.py <port>
   ```
4. In your browser (or via `curl`), navigate to:

   ```
   http://localhost:<port>/<filename>.html
   ```

5. To stop the server, press **Ctrl-C** in the terminal.

