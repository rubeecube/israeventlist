from Globals import *

dic = {
    "welcome text": "Welcome to Israel Event List (IsraEL)! By clicking on this link, you've opened the door to the "
                    "list of all activities in Tel Aviv! From kosher breakfasts to shows, classes, organized dinners, "
                    "excursions, and parties... Simply select your interests, and you'll receive notifications. It's "
                    "easy, it's free, and it's fantastic. You can always retrieve the list of commands by sending "
                    "/commands. To stop the service, send /stop.",
    "goodbye text": "We're delighted to have you with us. Feel free to share your feedback with us using the /contact "
                    "command so we can continue improving. To start over, use the /start command.",
    'retrieve phone': "To enhance the quality of our service, we need your phone number. You can provide it later.",
    "share contact": "Send my phone number.",
    'phone not retrieved, we try later': "The phone number couldn't be retrieved. We'll try again later.",
    'retrieve location': "To improve our service, we need your location. You can provide it later.",
    "share location": "Send my location",
    'location not retrieved, we try later': "The location couldn't be retrieved. We'll try again later.",
    'thanks phone': "Thank you for sharing your phone number.",
    'thanks location': "Thank you for sharing your location.",
    'thanks interests': "Thank you for sharing your interests.",
    'retrieve interests': "Choose one or more interests.",
    'finish': "I'm done %s" % Globals.EMOJI_THUMBS_UP,
    "contact us": "You can send your suggestions anytime.",
    "command list": "Please choose:",

    "command interests": "Select or edit my interests.",
    "command phone": "Share my phone number.",
    "command location": "Share my location.",
    "command commands": "View the list of commands.",
    "command contact": "Contact us.",
    "command stop": "Stop the service.",
    "command search": "Search.",

    "exit menu": "Exit the menu",
    "inform commands": "You can always retrieve the list of commands by sending /commands.",
    'search category': "Search by:",

    'poi for search': "Choose the point of interest:",
    'inerest for search': "Choose the interest category:",
    'no event found for poi, showing all': "No events found for this point of interest. Here are the results for a "
                                           "broader search.",
    'shpwing events': "Here are the results:",

    # Admin
    "welcome admin": "Hello! Welcome to the admin section of @IsraEventList_bot. To view the list of commands, send "
                     "/commands.",
    "command_admin add": "Add an entry.",
    "command_admin commands": "View the list of commands.",
    "command_admin list": "Please choose:",
    "admin add category": "Choose the category:",
    'saved': "Saved.",

    'name of poi': "Name of the POI?",
    'name of event': "Name of the event?",

    'desc of poi': "Description of the POI?",
    'desc of event': "Description of the event?",

    'location of poi': "GPS location of the POI?",
    'address of poi': "Address of the POI?",

    'interest for add': "Choose the interest category:",
    'poi for add': "Choose the point of interest:",

    'poi': "Location",
    'interest': "Interest category",
    'event': "Event",


    "no parent interest": "Main interest (No parent)",
    'name of interest': "Name of interest",

    'date': "Date?",
    'date format': "Accepted formats: 'Monday, Tomorrow, 07/06...'",

    'hour': "Hour?",
    'hour format': "Accepted formats: '10am, 10:30am; 10:30am'",

    'retry': "Retry",

    'info to add': "Choose the fields to fill",

    # MAASSER
    "MASR: welcome text": "Hello! This bot helps you keep track of income and expenses to fulfill the Maasser "
                          "mitzvah optimally. To add a salary, send /salaire.\n"
                          "To record a donation, send /don.\n"
                          "To display a summary, send /recap.\n"
                          "To change the Maasser percentage, send /maasser.\n"
                          "To change the currency, send /devise.\n"
                          "Data is securely stored and protected by a password.\n"
                          "For more information, send /details.\n"
                          "To contact the author, send /contact.",
    "MASR: details": "Each data entry is protected by the password you set during the first use.\n"
                     "Data is only revealed during display.\n"
                     "Neither the robot nor the author can read the data (except for the Maasser percentage for "
                     "technical reasons).\n"
                     "For technical details, send /details2.",
    "MASR: details2": "During initialization, a pair of RSA 3072 keys is generated. The private key is encrypted "
                      "with the provided password.\n"
                      "In the database, there are the public key and the encrypted private key (using the password), "
                      "along with an array of encrypted data.\n"
                      "For each insertion, a symmetric key is generated, encrypted with the public key. The insertion "
                      "(date, amount) is encrypted (using AES GCM 128) and stored for consolidation.\n"
                      "During display, the private key is decrypted, and all pending data is also decrypted. "
                      "The consolidated message is then re-encrypted.\n"
                      "That's enough technical details for now. For more, send /contact :D.",
    'MASR: user not found': "To use the service, please choose a password. You'll be asked for it each time you "
                            "view the data. Be careful, as we won't be able to recover it if you forget it. "
                            "You'll lose all data (except displayed tables).",
    'MASR: user found': 'The account has already been initialized.',
    "MASR: command list": 'List of commands',
    'MASR: date': "Date?\nAccepted formats: 'Monday, Tomorrow, 07/06/2022...'",

    'MASR: retry': 'Retry...',
    "MASR: amount--format": 'Amount in {}.\n'
                    'To insert another currency, add a symbol (EUR, €, USD, $, ILS, ₪).',
    'MASR: amount table--format': 'Amount ({})',
    'MASR: percentage': 'Percentage',
    "MASR: explain table": "A negative amount indicates what you still need to contribute this month.",
    "MASR: added": 'Added!',
    "MASR: password set": 'Saved!',
    "MASR: password?": "Please enter your password",
    "MASR: invalid, bad password?": "Incorrect password!",

    "MASR: command commands": "Display the list of commands",
    "MASR: command don": "Record a donation",
    "MASR: command salaire": "Record a salary",
    "MASR: command maasser": "Change the Maasser percentage",

    "MASR: command contact": "Contact the author",
    "MASR: command details": "Display details",
    "MASR: command devise": "Change the default currency",
    "MASR: command recap": "Display a summary table",
    "MASR: command edit": "Delete an entry",
    "MASR: command show": "List entries",

    "MASR: choose edit": "Choose the row to delete",
    "MASR: percentage ask": "What is the new percentage to apply?",
    "MASR: changed": "Changed!",
    "MASR: removed": "Removed!",
    "MASR: error": "Error...",
    "MASR: comment": "Description",

    "MASR: currency ask": "What is the new currency to apply (EUR, ILS, USD)?",
    "MASR: fingeprint?": "Reference? (You can retrieve the reference using the /show function)",
    "MASR: fingerprint show": "Reference",
    "MASR: date show": "Date",

    'Yesterday': 'Yesterday',
    'Today': "Today",
    'month': "Month",
    'MASR: total': "Total",
}


def localize(key):
    if key in dic.keys():
        return dic.get(key)
    return key
