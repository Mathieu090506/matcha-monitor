from playwright.sync_api import sync_playwright
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body_html, to_email):
    from_email = "duongthanh09052006@gmail.com"
    password = "xerj wfuq etdg oxrc" 
    
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    part2 = MIMEText(body_html, 'html')
    msg.attach(part2)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def create_html_body(title, items):
    item_list = "".join(
        f"<tr><td style='padding: 10px; border: 1px solid #dddddd;'><a href='{url}'>{name}</a></td></tr>" 
        for name, url in items
    )
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; margin: 20px auto; border: 1px solid #cccccc;">
                <tr>
                    <td align="center" bgcolor="#0073e6" style="padding: 20px 0; color: white; font-size: 24px; font-weight: bold;">
                        {title}
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#ffffff" style="padding: 20px 30px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td style="color: #153643; font-size: 16px;">
                                    <b>Dear Customer,</b>
                                    <p>We are excited to inform you about the following updates on our products:</p>
                                    <table style="width: 100%; border-collapse: collapse;">
                                        {item_list}
                                    </table>
                                    <p>Thank you for choosing our products!</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#0073e6" style="padding: 10px 30px; color: white; font-size: 12px;">
                        &copy; 2024 Your Company. All rights reserved.
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    return html

def check_stock(playwright):
    url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/category/matcha/principal/"
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # Go to page
    page.goto(url)
    
    # Get Items
    items = {
        'item-352': "https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1/",
        'item-403': "https://example.com/product-403",
        'item-397': "https://example.com/product-397"
    }
    
    restocked_items = []
    
    for item_id, item_url in items.items():
        sel_item = page.locator(f"#{item_id}")
        try:
            sel_item.wait_for(state='visible', timeout=60000)  # Chờ tối đa 60 giây để phần tử xuất hiện
            classes = sel_item.get_attribute('class')
            if "outofstock" in classes:
                print(f"Item ID {item_id} is out of stock")
            else:
                
                print(f"Item ID {item_id} is in stock")
                restocked_items.append((item_id, item_url))
        except Exception as e:
            print(f"Error for item {item_id}: {e}")
    
    if restocked_items:
        body_html = create_html_body("Products Restocked", restocked_items)
        send_email("Products Restocked", body_html, "duongthanh09052006@gmail.com")
    
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        check_stock(playwright)
