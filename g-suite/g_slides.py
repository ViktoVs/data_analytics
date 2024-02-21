import time
import datetime
from google.cloud import storage

import os.path

# for Google Drive API:
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Requests
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

# imports to write into google sheets
import gspread
import gspread_dataframe as gd

### Setup authentication to google sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("name_of_file")
g_client = gspread.authorize(creds)

def update_charts_in_gslide(PRESENTATION_ID: str
                            , path_to_service_file: str
                           ):
    """
    This function updates all linked objects in a google slides presentation.
    :param PRESENTATION_ID: Id of your google slide presentation
    :param path_to_service_file: location of your service account file
    :return: None
    """

    # Set up connection
    scopes = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_service_file)

    service = build("slides", "v1", credentials=creds)

    # Call the slides API
    presentation = service.presentation().get(presentation_id=PRESENTATION_ID).execute()
    slides = presentation.get("slides")


    # get object ids of all linked charts in g-slide

    chart_ids = []
    for i in range(len(slides)):
        slide = presentation.get("slides")[i]
        
        if slide.get("pageElements") != None:

            for j in range(len(slide.get("pageElements"))):
                if slide.get("pageElements")[j].get("sheetChart") != None:
                    chart_ids.append(slide.get("pageElements")[j].get("objectID"))

    # update all linked charts
    # check if it can be simplified

    for i, presentation_chart_id in zip(range(len(chart_ids)), chart_ids):
        requests = [
            {"refreshSheetChart" : {
                "objectId" : str(presentation_chart_id)
                }
            }
        ]
        body = {"requests": requests}

        requests = service.presentation().batchUpdate(presentation_id = PRESENTATION_ID, body = body).execute()
    print("Updated all linked Charts")
    return 

def create_g_slide_shape_with_text(PRESENTATION_ID
                                   , page_object_id
                                   , element_id
                                   , shape
                                   , translateX
                                   , translateY
                                   , height
                                   , width
                                   , text
                                   , path_to_service_file
                                  ):
    """
    This function creates a new shape with text in your g-slide presentation
    :param PRESENTATION_ID: Id of your presentation
    :param page_object_id: id of the slide where the shape shouhld be created
    :param element_id: id of the shape you want to create - choose for yourself
    :param shape: the shape you want to create e.g. "TEXT_BOX", "TRIANGLE"
    :param translateX: to set the position of of the shape
    :param translateY: to set the position of of the shape
    :param height: to set the size of of the shape
    :param width: to set the size of of the shape
    :param text: the text for the shape
    :param path_to_service_file: location of your service account file
    """

    # Set up connection
    scopes = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_service_file)

    service = build("slides", "v1", credentials=creds)

    # Call the slides API
    presentation = service.presentation().get(presentation_id=PRESENTATION_ID).execute()
    slides = presentation.get("slides")

    # Create the API request

    requests = [
        {
            "createShape" : {
                "object_id": element_id,
                "shapeType": shape,
                "elementProperties": {
                    "pageObjectId": page_object_id,
                    "size": {
                        "height": {"magnitude": height, "unit": "PT"},
                        "width": {"magnitude": width, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": translateX,
                        "translateY": translateY,
                        "unit": "PT"
                    }
                }
            }
        },
        {
            "insertTest": {
                "objectID": element_id,
                "insertionIndex": 0,
                "text": text
            }
        }
    ]

    # Execute the request

    body = {
        "requests": requests
    }

    response = service.presentation().batchUpdate(presentation_id = PRESENTATION_ID, body = body).execute()
    #create_shape_response = response.get("replies")[0].get("createShape") ### check if needed

def update_text_gslides( PRESENTATION_ID
                        , element_id
                        , text
                        , font_family
                        , font_size
                        , font_rgb_r
                        , font_rgb_g
                        , font_rgb_b
                        , path_to_service_file
                       ):
    """
    This function updates text in your g-slide presentation
    :param PRESENTATION_ID: Id of your presentation
    :param element_id: id of the text box where it should be updated
    :param text: new text for the slide
    :param font_family: define the font family
    :param font_size: define the font size
    :param font_rgb_r: RGB Color Red (between 0 and 1)
    :param font_rgb_g: RGB Color Green (between 0 and 1)
    :param font_rgb_b: RGB Color Blue (between 0 and 1)
    :param path_to_service_file: location of your service account file
    """

    # Set up connection
    scopes = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_service_file)

    service = build("slides", "v1", credentials=creds)

    # Call the slides API
    presentation = service.presentation().get(presentation_id=PRESENTATION_ID).execute()
    slides = presentation.get("slides")

    # build the request

    requests = [
        # delete existing text
        {
            "deleteText": {
                "objectId": element_id,
                "textRange": {"type": "ALL"}
            }
        },
        # insert text 
        {
            "insertText": {
                "objectId": element_id,
                "insertionIndex": 0,
                "text": text
            }
        },
        # update text styles
        {
            "updateTextStyle": {
                "objectId": element_id,
                "fields": "fontFamily,fontSize,foregroundColor",
                "textRange": {"type": "ALL"},
                "style": {
                    "fontFamily": font_family,
                    "fontSize": {"magnitude": font_size, "unit": "PT"},
                    "foregroundColor": {
                        "opaqueColor": {
                            "rgbColor": {
                                "blue": font_rgb_b,
                                "green": font_rgb_g,
                                "red": font_rgb_r
                            }
                        }
                    }
                }
            }
        }

    ]

    # Execute the request

    body = {
        "requests": requests
    }

    response = service.presentation().batchUpdate(presentation_id = PRESENTATION_ID, body = body).execute()
    #create_shape_response = response.get("replies")[0].get("createShape") ### check if needed    