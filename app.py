import os
from flask import Flask, request, redirect, url_for, render_template, flash, session
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from werkzeug.utils import secure_filename
from PIL import Image

# Azure Form Recognizer credentials
ENDPOINT = "YOUR ENDPOINT HERE"
API_KEY = "API KEY"


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_IMAGE_SIZE = (2000, 2000)  # Maximum image dimensions allowed by Azure
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the Azure Document Analysis client
client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

# Global variables to store extracted items and assignments
extracted_items = []
assignments = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global extracted_items, assignments
    extracted_items = []
    assignments = {}

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Resize image if necessary
            resize_image(filepath, MAX_IMAGE_SIZE)

            process_receipt(filepath)
            return redirect(url_for('assign'))

    return render_template('index.html', items=extracted_items)

def resize_image(filepath, max_size):
    """Resize the image to the maximum allowed size."""
    with Image.open(filepath) as img:
        # Check if image size exceeds the max size
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size)
            img.save(filepath)

def process_receipt(filepath):
    global extracted_items
    # Open the file and send it to Azure for analysis
    with open(filepath, 'rb') as f:
        poller = client.begin_analyze_document("prebuilt-receipt", document=f)
        result = poller.result()

    # Reset extracted items
    extracted_items = []
    
    

    # Parse the result from Azure
    for receipt in result.documents:
        
        
        print(receipt)
        for item in receipt.fields.get("Items").value:
            item_name = item.value.get("Description").value if item.value.get("Description") else "Unknown Item"
            item_quantity = item.value.get("Quantity").value if item.value.get("Quantity") else 1
            #item_price = item.value.get("Price").value if item.value.get("Price") else item.value.get("TotalPrice").value/item_quantity if item.value.get("TotalPrice") else 0.0
            if(item.value.get("Price")):
                
                item_price = item.value.get("Price").value

            else:

                item_price = item.value.get("TotalPrice").value / item_quantity if item.value.get("TotalPrice") else 0.0
                
    

            extracted_items.append({
                'name': item_name,
                'price': item_price,
                'quantity': item_quantity
            })

@app.route('/assign', methods=['GET', 'POST'])
def assign():
    global assignments
    

    if request.method == 'POST':
        if 'add_person' in request.form:
            # Add a new person
            person_name = request.form.get('person_name')
            if person_name and person_name not in assignments:
                assignments[person_name] = []

        elif 'assign_item' in request.form:
            # Assign items to multiple people
            item_name = request.form.get('item')
            selected_people = request.form.getlist('person')
            
            if selected_people and item_name:
                # Find the item by name
                item = next((item for item in extracted_items if item['name'] == item_name), None)
                
                if item:
                    # Determine total cost based on rate or amount
                    if 'amount' in item and item['amount'] is not None:
                        total_item_cost = item['amount']
                    else:
                        total_item_cost = item['price'] * item['quantity']

                    # Calculate split cost per person
                    split_cost = total_item_cost / len(selected_people)

                    # Assign item to each person
                    for person_name in selected_people:
                        if person_name not in assignments:
                            assignments[person_name] = []
                        # Append the split item to the person's assignments
                        assignments[person_name].append({'name': item_name, 'cost': split_cost})

                    # Remove the item from extracted_items once assigned
                    extracted_items[:] = [item for item in extracted_items if item['name'] != item_name]

                    # Reduce the total bill by the assigned item's total cost
                    

        return redirect(url_for('assign'))

    # Calculate totals for each person
    totals = {person: sum(item['cost'] for item in items) for person, items in assignments.items()}

    return render_template('assign.html', items=extracted_items, assignments=assignments, totals=totals)

if __name__ == '__main__':
    # Calculate the initial total bill from extracted items
    
    app.run(debug=True)



