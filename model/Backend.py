import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from tensorflow.keras.models import load_model
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/get-prediction', methods=['GET'])
def get_string():
    # Create a session using your AWS credentials
    session = boto3.Session(
        aws_access_key_id= os.getenv('AWS_ACCESS_KEY'), # Replace with your access key or use environment variables
        aws_secret_access_key= os.getenv('AWS_SECRET_KEY'), # Replace with your secret key or use environment variables
        region_name= os.getenv('AWS_REGION') # Replace with your region or use environment variables
    )

    # Create an S3 resource object using the session
    s3 = session.resource('s3')

    bucket = s3.Bucket('frubucket')

    # Create an S3 client using the session
    s3_client = session.client('s3', config=Config(signature_version='s3v4'))

    try:
        # Get the list of all objects and sort them by last modified date
        objs = sorted(bucket.objects.all(), key=lambda obj: obj.last_modified, reverse=True)

        # Get the most recent object
        most_recent_obj = objs[0]

        # Get the URL of the most recent object
        most_recent_obj_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket.name, 'Key': most_recent_obj.key}, ExpiresIn=3600)
        print(most_recent_obj_url)

    except NoCredentialsError:
        print("No AWS credentials found")
    except IndexError:
        print("No objects found in the bucket")

    def resize_and_pad_image(image_url, max_dimension, target_size=(100, 100)):
        # Download the image from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        # Get original width and height
        original_width, original_height = image.size
        
        # Calculate aspect ratio
        aspect_ratio = original_width / original_height
        
        # Determine new dimensions
        if original_width >= original_height:
            new_width = max_dimension
            new_height = int(max_dimension / aspect_ratio)
        else:
            new_height = max_dimension
            new_width = int(max_dimension * aspect_ratio)
        
        # Resize the image while maintaining aspect ratio
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a new blank white image with the target size
        new_image = Image.new("RGB", target_size, color="white")

        # Paste the resized image onto the center of the blank white image
        position = ((target_size[0] - resized_image.size[0]) // 2, (target_size[1] - resized_image.size[1]) // 2)
        new_image.paste(resized_image, position)
        
        return new_image

    new_image = resize_and_pad_image(most_recent_obj_url, 100)

    # Load the model
    model = load_model('CNN_model.keras')

    # Convert the image to a numpy array
    image_array = np.array(new_image)

    # Normalize the image array
    image_array = image_array / 255.0

    # Reshape the image array to match the input shape of your model
    # Assuming your model takes input of shape (100, 100, 3)
    image_array = image_array.reshape(1, 100, 100, 3)

    # Use the model to make a prediction
    prediction = model.predict(image_array)

    # Find the index of the category with the highest probability
    predicted_category_index = np.argmax(prediction)

    # List of category names in the order they were encoded
    category_names = ['Aloe Vera', 'Banana', 'Bilimbi', 'Cantaloupe', 'Cassava', 'Coconut', 'Corn', 'Cucumber', 'Curcuma', 'Eggplant', 'Galangal', 'Ginger', 'Guava', 'Kale', 'Longbeans', 'Mango', 'Melon', 'Orange', 'Paddy', 'Papaya', 'Peperchili', 'Pineapple', 'Pomelo', 'Shallot', 'Soybeans', 'Spinach', 'Sweetpotatoes', 'Tobacco', 'Waterapple', 'Watermelon']

    # Get the name of the predicted category
    predicted_category_name = category_names[predicted_category_index]

    # Print the predicted category
    print(predicted_category_name)
    
    prediction = predicted_category_name
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True, port=3001)
