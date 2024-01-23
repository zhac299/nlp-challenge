import random
import sqlite3
from confection import Config
from sklearn.model_selection import train_test_split
import spacy
from spacy.training.example import Example
from spacy.pipeline.textcat import single_label_cnn_config

# Function to fetch data from the SQLite database
def fetch_data_from_database():
    try:
        conn = sqlite3.connect("./db/demo.db")  # Replace with your actual database file
        cursor = conn.cursor()

        # Fetch data from the database
        cursor.execute("SELECT brand_name, label_desc FROM BRANDLABEL")
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return []

def nlp_model():
    # Load spaCy model
    nlp = spacy.blank("en")

    # Fetch data from the database
    data_from_database = fetch_data_from_database()

    # Prepare the data for training
    train_data = []
    for row in data_from_database:
        brand_name, description = row
        train_data.append((description, {"cats": {brand_name: 1.0}}))

    # Split the dataset into training and testing sets
    train_data, test_data = train_test_split(train_data, test_size=0.2, random_state=42)

    # Define the text classification model using a predefined configuration
    config = Config().from_str(single_label_cnn_config)
    text_cat = nlp.add_pipe("textcat", config=config, last=True)

    # Add labels dynamically based on the unique brands in the dataset
    unique_brands = set(row[0] for row in data_from_database)
    for brand in unique_brands:
        text_cat.add_label(brand)

    # Train the model
    nlp.begin_training()

    for epoch in range(10):
        losses = {}
        random.shuffle(train_data)
        for text, annotations in train_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.5, losses=losses)
        
        # Print training loss after each epoch
        print(f"Epoch {epoch + 1}, Loss: {losses['textcat']:.4f}")

    # Evaluate on the test set
    test_losses = {}
    for text, annotations in test_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], drop=0.0, losses=test_losses)

    print(f"Test Loss: {test_losses['textcat']:.4f}")

    # Save the trained model
    nlp.to_disk("car_recommendation_model")

def run_model(inputString):
    # Load the trained model
    nlp = spacy.load("car_recommendation_model")

    # Test the model on new examples
    new_texts = [
        inputString
    ]

    doc = nlp(inputString)
    predicted_label = max(doc.cats, key=doc.cats.get)
    return(f"Input: {inputString}\nPrediction: {predicted_label}\n")

run_model("I want a luxury SUV")