Overview
scanner.py is a Python script designed to gather and analyze information about a website. It provides detailed reports about the website's IP address, HTTP headers, SSL certificate, HTML metadata, and checks if the associated IP address is potentially using a VPN. The results are compiled into a neatly formatted PDF report.

Features
Extracts HTTP headers from the target website.
Resolves and displays the IP address of the website.
Fetches SSL certificate details, including issuer, validity dates, and expiration.
Analyzes the website's HTML content for title and meta-description tags.
Checks whether the IP address belongs to a VPN provider.
Generates a PDF report containing all collected information.
Requirements
Python 3.x
Libraries:
requests
socket
ssl
os
json
bs4 (BeautifulSoup)
reportlab
To install the necessary libraries, use:

bash
Copy code
pip install requests beautifulsoup4 reportlab
Usage
Save the script as scanner.py.
Run the script using Python:
bash
Copy code
python scanner.py
Enter the URL of the website to scan (e.g., https://example.com).
The script performs the following actions:

Resolves the IP address of the website.
Retrieves and logs HTTP headers.
Analyzes the SSL certificate.
Inspects the HTML structure for key metadata.
Checks if the IP address might belong to a VPN service.
The resulting report is saved as a PDF file in a Scanner folder on your desktop.
Example
plaintext
Copy code
Enter URL (e.g., https://example.com): https://example.com

[+] Scanning site: https://example.com
[+] IP Address: 93.184.216.34
[+] HTTP Headers:
  Server: ECS (nyb/1F13)
  Content-Type: text/html; charset=UTF-8
  ...

[+] SSL Certificate Info:
  Issued by: ...
  Valid from: ...
  Valid until: ...

[+] HTML Info:
  Title: Example Domain
  Description: This domain is established to be used for illustrative examples in documents.

[+] VPN Check:
  Organization: ExampleOrg
  Country: US
  ...
Output
The script generates a PDF report named scan_report.pdf, located in a Scanner folder on your desktop. The report contains all the information gathered during the scan.

Limitations
Requires an active internet connection.
SSL certificate analysis depends on server support for HTTPS.
VPN detection relies on public data sources (e.g., ipinfo.io).
License
This script is distributed under the MIT License. Feel free to modify and use it as needed.
