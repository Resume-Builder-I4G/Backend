'''Module that runs the application'''
from app import app

@app.errorhandler(500)
def server_error(e):
    return  {
        'error': 'Server Error',
        'message' : str(e)  
        }, 500

@app.errorhandler(404)
def endpoint_error(e):
    return  {
        'error': 'Invalid endpoint',
        'message' : str(e)  
        }, 404

@app.errorhandler(400)
def client_error(e):
    return  {
        'error': 'Bad request',
        'message' : str(e)  
        }, 500
        
if __name__ == "__main__":
    app.run()