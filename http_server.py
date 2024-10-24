import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HOST = os.getenv("HOST", "localhost")
HTTP_PORT = int(os.getenv("HTTP_PORT", 8080))


class MyHandler(SimpleHTTPRequestHandler):
  def end_headers(self):
    self.send_header("Access-Control-Allow-Origin", "*")
    super().end_headers()

  def do_GET(self):
    if self.path == "/client.html":
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(self.get_client_html().encode())
    else:
      super().do_GET()

  def get_client_html(self):
    with open("client.html", "r") as file:
      content = file.read()

    # Replace placeholders with actual values from environment variables
    content = content.replace(
        "##CLIENT_WIDTH##", os.getenv("CLIENT_WIDTH", "400"))
    content = content.replace(
        "##CLIENT_HEIGHT##", os.getenv("CLIENT_HEIGHT", "300"))
    content = content.replace(
        "##CLIENT_JPG_COMPRESSION##", os.getenv("CLIENT_JPG_COMPRESSION", "0.5"))

    return content


def run(server_class=HTTPServer, handler_class=MyHandler):
  server_address = (HOST, HTTP_PORT)
  httpd = server_class(server_address, handler_class)
  print(f'Serving HTTP on {HOST}:{HTTP_PORT}...')
  httpd.serve_forever()


if __name__ == "__main__":
  run()
