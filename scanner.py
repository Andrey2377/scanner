import requests
import socket
import ssl
import os
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class PDFReport:
    def __init__(self, filename="scan_report.pdf"):
        self.folder_path = r"D:\projects\Scanner"  # Променена директория
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        
        self.filename = os.path.join(self.folder_path, filename)
        self.canvas = canvas.Canvas(self.filename, pagesize=A4)
        self.y_position = 800
    
    def add_text(self, text):
        self.canvas.setFont("Helvetica", 10)
        for line in text.split("\n"):
            self.canvas.drawString(50, self.y_position, line)
            self.y_position -= 15
            if self.y_position < 50:
                self.canvas.showPage()
                self.y_position = 800
    
    def add_json(self, json_data):
        formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        self.add_text(formatted_json)
    
    def save(self):
        self.canvas.save()
        print(f"\n[+] Отчетът е записан в: {self.filename}")


def get_headers_info(url, pdf_report):
    try:
        response = requests.get(url)
        pdf_report.add_text("[+] HTTP Headers:")
        for header, value in response.headers.items():
            pdf_report.add_text(f"  {header}: {value}")
    except Exception as e:
        pdf_report.add_text(f"[-] Грешка при получаване на хедърите: {e}")


def get_ip_info(url, pdf_report):
    try:
        domain = urlparse(url).netloc
        ip_address = socket.gethostbyname(domain)
        pdf_report.add_text(f"[+] IP адрес: {ip_address}")
        return ip_address
    except Exception as e:
        pdf_report.add_text(f"[-] Грешка при извличане на IP адреса: {e}")
        return None


def get_ssl_info(url, pdf_report):
    try:
        domain = urlparse(url).netloc
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                pdf_report.add_text("[+] SSL сертификат информация:")
                pdf_report.add_text(f"  Издаден от: {cert.get('issuer', 'Неизвестен')}")
                pdf_report.add_text(f"  Валиден от: {cert.get('notBefore', 'Неизвестна')}")
                pdf_report.add_text(f"  Валиден до: {cert.get('notAfter', 'Неизвестна')}")
    except Exception as e:
        pdf_report.add_text(f"[-] Грешка при получаване на SSL информацията: {e}")


def analyze_html(url, pdf_report):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "Няма заглавие"
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else "Няма описание"
        
        pdf_report.add_text("[+] HTML информация:")
        pdf_report.add_text(f"  Заглавие: {title}")
        pdf_report.add_text(f"  Описание: {description}")
    except Exception as e:
        pdf_report.add_text(f"[-] Грешка при анализ на HTML: {e}")


def check_vpn_usage(ip, pdf_report):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        pdf_report.add_text("[+] Проверка за VPN:")
        pdf_report.add_text(f"  Организация: {data.get('org', 'Неизвестна')}")
        pdf_report.add_text(f"  Държава: {data.get('country', 'Неизвестна')}")
        pdf_report.add_text(f"  Град: {data.get('city', 'Неизвестен')}")
        if 'VPN' in data.get('org', ''):
            pdf_report.add_text("  [!] Възможно е IP адресът да е VPN.")
        else:
            pdf_report.add_text("  [+] IP адресът не изглежда да е VPN.")
    except Exception as e:
        pdf_report.add_text(f"[-] Грешка при проверка на VPN: {e}")


def main():
    url = input("Въведете URL адрес (например https://example.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    pdf_report = PDFReport(filename="scan_report.pdf")
    pdf_report.add_text(f"Сканиране на сайта: {url}")

    ip_address = get_ip_info(url, pdf_report)
    get_headers_info(url, pdf_report)
    get_ssl_info(url, pdf_report)
    analyze_html(url, pdf_report)
    if ip_address:
        check_vpn_usage(ip_address, pdf_report)

    pdf_report.save()


if __name__ == "__main__":
    main()
