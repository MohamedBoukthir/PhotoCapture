from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import os
import base64
from datetime import datetime

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'photoCapture'

mysql = MySQL(app)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for image upload
@app.route('/upload', methods=['POST'])
def upload():
    try:
        image_data = request.json['image']

        # Decode the base64 image data
        image_binary = base64.b64decode(image_data.split(',')[1])

        # Generate a unique filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'image_{timestamp}.png'

        # Save the image to the 'captured_images' folder
        image_path = os.path.join('images', filename)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_binary)

        # Save the image path to the database (you can modify your database schema accordingly)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO images (path) VALUES (%s)", (image_path,))
        mysql.connection.commit()
        cur.close()

        return jsonify(message='Image uploaded successfully')
    except Exception as e:
        print('Error uploading image:', e)
        return jsonify(error='Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
