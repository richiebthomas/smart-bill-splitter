# Smart Bill Splitter

Smart Bill Splitter is a web application designed to help users easily split bills by scanning receipts using their device's camera. The app extracts items, quantities, and prices from the receipt image and allows users to assign items to people and calculate their individual share.

## Features

- **Receipt Scanning**: Use your device's camera to scan receipts directly.
- **Automatic Extraction**: Automatically extract item names, quantities, and prices from the scanned receipt.
- **Item Assignment**: Assign extracted items to multiple people to split the bill.
- **Cost Calculation**: Calculate each person's share of the bill.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.
![image](https://github.com/user-attachments/assets/e50f6ca8-91fb-4f82-84bf-a0754cd2a412)

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Python (Flask)
- **Image Processing**: OCR using Tesseract or other services
- **Deployment**: Flask server

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

- Python 3.x
- Flask
- MS Azure Document Intelligence API  (for receipt processing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/smart-bill-splitter.git
   cd smart-bill-splitter

2. **Set up a virtual environment:**
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**
pip install -r requirements.txt
   
4. **Set up Azure Document Intelligence:**
Get endpoint and API key

5. **Run the application:**
python app.py


Usage

    Scan a Receipt:
        Click the "Scan Receipt" button to open your device's camera.
        Capture the receipt image.

    Extract and Assign Items:
        The app will extract items and display them in a list.
        Assign items to different people for cost sharing.

    Calculate Costs:
        The app will calculate the total cost and individual shares based on the assigned items.

Project Structure

    app.py: Main Flask application file.
    templates/: HTML templates for rendering pages.
    static/: Static files such as CSS and JavaScript.
    uploads/: Folder for storing uploaded receipt images.

