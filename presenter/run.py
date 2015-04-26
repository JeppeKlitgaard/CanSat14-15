from config import PORT, ADDRESS, DEBUG
from app import app
app.run(host=ADDRESS, port=PORT, debug=DEBUG)
