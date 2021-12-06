STARTED, HANDLE_PHONE, AFTER_PHONE, HANDLE_LOCATION, AFTER_LOCATION,\
    HANDLE_INTERESTS, FINISH_INIT, NOMINAL, HELP = range(9)
ASK_PHONE = STARTED
ASK_LOCATION = AFTER_PHONE
ASK_INTERESTS = AFTER_LOCATION

# Admin
AUTHENTICATED, POI_ADD_INTEREST, POI_ADD_NAME, POI_ADD_DESC, POI_ADD_LOCATION, POI_ADD_ADDRESS = range(6)

"""
x:
- Intitiator:
-- Initiated with /start
- Preconditions:
-- User sent /start
- Postcondition:
-- State = STARTED
-- Context = Infos(First name, Last name, Language)
- Actions:
-- Retrieve Infos (Not interactive):
--- First name,
--- Last name,
--- Language
-- Set jobs:
--- ???

STARTED || ASK_PHONE:
- Preconditions:
-- Context = Infos(First name, Last name, Language)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = HANDLE_PHONE
- Actions:
-- Ask for phone

HANDLE_PHONE:
- Preconditions:
-- Context = Infos(First name, Last name, Language)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = AFTER_PHONE
-- if User is OK:
--- Context += Infos(Phone)
-- if User is NOK:
--- Context += Infos(Phone=None)
--- Jobs += reask_phone
- Actions:
-- Handle and store phone if provided

AFTER_PHONE || ASK_LOCATION:
- Preconditions:
-- Context = Infos(First name, Last name, Phone)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = HANDLE_LOCATION
- Actions:
-- Ask for location

HANDLE_LOCATION:
- Preconditions:
-- Context = Infos(First name, Last name, Phone)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = AFTER_LOCATION
-- if User is OK:
--- Context += Infos(Location)
-- if User is NOK:
--- Context += Infos(Location=None)
--- Jobs += reask_location
- Actions:
-- Handle and store location if provided

AFTER_LOCATION || ASK_INTERESTS:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = HANDLE_INTERESTS1
- Actions:
-- Ask for interests with list

HANDLE_INTERESTS1:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = HANDLE_INTERESTS2 OR NOMINAL
-- if User is OK:
--- Context += Infos(InterestsList)
- Actions:
-- Handle and store InterestsList if provided
-- Ask for precisions

HANDLE_INTERESTS2:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location, InterestsList)
-- Jobs = ??
-- User sent a message
- Postcondition:
-- State = NOMINAL
-- if User is OK:
--- Context += Infos(InterestsPreciseList)
- Actions:
-- Handle and store InterestsPreciseList if provided
-- Ask for precisions

NOMINAL:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location, InterestsList, InterestsPreciseList)
-- User sent a message
- Postcondition:
-- State = Depend on action
- Actions:
-- If message looks like command: Suggest command 
-- Show list of commands
-- Ask if need help

COMMAND:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location, InterestsList, InterestsPreciseList)
-- User sent a command
- Postcondition:
-- State = ASK_INTERESTS OR ASK_PHONE OR ASK_LOCATION
- Actions:
-- Redirect to command

AUTO:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location, InterestsList, InterestsPreciseList)
-- Run via Job
- Postcondition:
-- State = NOMINAL
- Actions:
-- Ask for non filled fields

HELP:
- Preconditions:
-- Context = Infos(First name, Last name, Phone, Location, InterestsList, InterestsPreciseList)
-- User sent a command
- Postcondition:
-- State = NOMINAL
- Actions:
-- ?Send phone number?
-- ?Open chat?
"""