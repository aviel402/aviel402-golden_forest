from flask import Flask

app = Flask(__name__)

@app.route('/api/get_world_data', methods=['GET'])
def a():
  x=open('players_data.json','r')
  return x
