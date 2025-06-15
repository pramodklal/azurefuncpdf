import logging
import azure.functions as func
import os
import azure.storage.fileshare as share
from azure.storage.fileshare import ShareFileClient
from fpdf import FPDF
import datetime
import io
from azure.storage.fileshare import ShareServiceClient
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
from dotenv import load_dotenv
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_triggerpramazfunc")
def http_triggerpramazfunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        try:
            load_dotenv()  # Load variables from .env
            Account_Key = os.getenv("envAccountKey")
            logging.info('Python timer trigger function executed.')
    # --- Replace with your Azure File Share details ---
            connection_string = "DefaultEndpointsProtocol=https;AccountName=pramstorageaccount111;AccountKey="+str(Account_Key)+";EndpointSuffix=core.windows.net"
            share_name = "safilesharepram"
            directory_name = "ecw_process_http"  # Optional: Specify a directory within the share
            file_name = "Test-Python-File" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"

            # --- 1. Create the PDF in Memory ---
            # Create a BytesIO object
            buffer = io.BytesIO()

            # Create a PDF canvas and draw some content
            c = canvas.Canvas(buffer, pagesize=A4)
            c.drawString(100, 750, "PDF file for Azure File Share created by Python code at @HTTP " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            c.drawString(100, 735, "This is a PDF by Python code and uploaded to Azure.")
            c.save()  # Save the canvas to the BytesIO buffer

            # Get the PDF content as bytes
            pdf_bytes = buffer.getvalue()

            # Close the buffer
            buffer.close()

            # --- 2. Upload to Azure File Share --
                 # Create a ShareServiceClient
            share_service_client = ShareServiceClient.from_connection_string(connection_string)

        # Get a client for the share
            share_client = share_service_client.get_share_client(share_name)

        # Get a client for the directory (create if it doesn't exist)
            directory_client = share_client.get_directory_client(directory_name)
            if not directory_client.exists():
                directory_client.create_directory()  # This will not raise an error if the directory already exists
            else:
             logging.info(f"Directory '{directory_name}' does not exist. Creating it now.")
           
        # Get a client for the file within the directory
             file_client = directory_client.get_file_client(file_name)

        # Upload the PDF bytes from BytesIO
             file_client.upload_file(pdf_bytes)

            
            #-----Return Message
            return func.HttpResponse(f"Hello, {name} :-This HTTP triggered function executed successfully and file, {file_name} created.")
        except Exception as ex:
             return func.HttpResponse(f"Hello-unction executed successfully Error Message:-, {ex}. ")
            
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )