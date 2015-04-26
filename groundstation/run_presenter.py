from .config import PRESENTER
from .presenter import app

if __name__ == '__main__':
    # reloader modifies system path and system modules
    # it cannot be used.
    app.run(host=PRESENTER["address"], port=PRESENTER["port"],
            debug=PRESENTER["debug"], use_reloader=False)
