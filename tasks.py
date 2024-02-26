from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
import time  # Import the time module

from RPA.Archive import Archive

@task
def robot_orders_collection():
    browser.configure(slowmo=1000)
    Open_the_website()
    download_orders_file()
    read_orders_as_tables()

def Open_the_website():

    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def download_orders_file():
    
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def read_orders_as_tables():
    """Read the orders and store them as a table"""
    library = Tables()
    orders = library.read_table_from_csv("orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"])

    # Loop over the orders
    for row in orders:
        close_annoying_modal()
        fill_form(row)
        make_order()
        
        image = screenshot_robot(row)
        store_receipt_as_pdf(row,image)
       
     
        #embed_screenshot_to_pdf(row, image)
        order_another()


def screenshot_robot(order_row):

    page = browser.page()
    while True:
        try:
            page.wait_for_selector('#robot-preview-image')
            image = page.locator('#robot-preview-image')
            image.screenshot(path=f"output/{order_row['Order number']}.png")
            return image  # Return the image locator
        except:
            page.wait_for_selector('#robot-preview-image')
            image = page.locator('#robot-preview-image')
            image.screenshot(path=f"output/{order_row['Order number']}.png")
            return image  # Return the image locator

def close_annoying_modal():
    
    page = browser.page()
    while True:
        try:
            page.click("button:text('Yep')")
            break
        except:
            page.click("button:text('Yep')")
        
        

    

def fill_form(order_row):

    page = browser.page()
    page.select_option(".custom-select", order_row["Head"])
    radio_value = order_row["Body"]
    page.click(f"input[type='radio'][value='{radio_value}']")
    page.fill(".form-control", order_row["Legs"])
    page.fill("#address", order_row["Address"])
    page.click("#preview")
   

def make_order():
    page=browser.page()
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
             page.click("#order")
             break
        except:
             if attempt == max_attempts - 1:
            # Log an error or handle the issue appropriately
                 raise
             else:
            # Retry
                  continue
 


def order_another():
    
    page = browser.page()
    while True:
        try:
            page.click("#order-another")
            break
        except:
            page.click("#order-another")
        

def store_receipt_as_pdf(order_row,image):
    
    page = browser.page()
    page.wait_for_selector('#receipt')
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
   
            table = page.locator("#receipt").inner_html(timeout=6000)
            break
        except:
              if attempt == max_attempts - 1:
            # Log an error or handle the issue appropriately
                  raise
              else:
            # Retry
                  continue

             
    pdf = PDF()
    list_files=[image]

    pdf.html_to_pdf(table, f"output/{order_row['Order number']}.pdf")
    pdf.open_pdf(f"output/{order_row['Order number']}.pdf")
    pdf.add_files_to_pdf(files=list_files,target_document=f"output/{order_row['Order number']}.pdf")
    pdf.close_pdf(f"output/{order_row['Order number']}.pdf")
    
   
    
             
        


def screenshot_robot(order_row):
    
    page = browser.page()
    while True:
        try:
            page.wait_for_selector('#robot-preview-image')
            image=page.locator('#robot-preview-image')
            image.screenshot(path=f"output/{order_row['Order number']}.png")
            break
        except:
            page.wait_for_selector('#robot-preview-image')
            image=page.locator('#robot-preview-image')
            image.screenshot(path=f"output/{order_row['Order number']}.png")

           # return image




"""def embed_screenshot_to_pdf(pdf_name, image):
    pdf = PDF()
    pdf_metadata=pdf.open_pdf(pdf_name)
    list_files = [image]
    pdf.add_files_to_pdf(files=list_files, target_document=pdf_metadata)



def archive_receipts():
    lib=Archive()
    """
    