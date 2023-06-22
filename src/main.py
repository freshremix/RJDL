import sys
import re
import webbrowser
from functools import partial
from radio import RadioJavan
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

def download(url):
    """
    Open web browser with the URL scraped from the action function.
    """
    webbrowser.open(url)

def action(url):
    """
    Call the scraper.
    :param url: URL of the song in www.radiojavan.com
    """
    if url.text():
        url_text = url.text().strip()  # Get text from QLineEdit and remove leading/trailing spaces
        match = re.match(r"(https://www.radiojavan.com/mp3s)", url_text)  # Match for the correct pattern
        if match:
            radio_javan = RadioJavan(url=url_text)  # Create an instance of the scraper
            final_url = radio_javan.scrap()  # Scrape the URL
            if final_url:
                download_btn.show()  # Show the download button
                download_btn.clicked.connect(partial(download, final_url))  # Connect the download function to open the URL
            else:
                result_lbl.setText("Failed to retrieve the download URL.")
        else:
            result_lbl.setText("Please enter a correct URL.")
    else:
        result_lbl.setText("Please enter a URL.")

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Radio Javan Downloader')
window.setGeometry(500, 300, 700, 300)  # Set the window size
window.setFixedSize(700, 300)  # Fix the window size

# Label that shows what the user should do
main_lbl = QLabel('Please enter the URL:', parent=window)
main_lbl.move(140, 50)

# Input box
url_input = QLineEdit(parent=window)
url_input.setGeometry(100, 80, 500, 40)
url_input.setPlaceholderText('Enter the URL of the song')
url_input.setFocus()

# Button to start scraping the URL
btn = QPushButton('Find', parent=window)
btn.setGeometry(210, 140, 280, 40)
btn.clicked.connect(partial(action, url_input))  # Call the action() function when the button is pressed

# Download button
download_btn = QPushButton('Download', parent=window)
download_btn.setGeometry(300, 140, 100, 40)
download_btn.hide()

# Label to show the result
result_lbl = QLabel(parent=window)
result_lbl.setGeometry(50, 190, 600, 40)
result_lbl.setAlignment(Qt.AlignCenter)

window.show()  # Show the window
sys.exit(app.exec_())  # Keep the app running in the main loop
