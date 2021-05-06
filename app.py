from flask import Flask

app = Flask(__name__)
#app.debug = False   
app.config["SECRET_KEY"] = "fvj34rjh2b4h3jk{34r3}42fgf"
   
from routes import *

if __name__ == "__main__":
    app.run()