import requests
from bs4 import BeautifulSoup
import csv
import os
import tkinter as tk
from tkinter import messagebox

def scrape_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for product in soup.find_all('div', class_='product'):  # Example HTML
            name = product.find('h2', class_='product-name').text.strip()
            price = product.find('span', class_='product-price').text.strip()
            rating = product.find('span', class_='product-rating').text.strip()
            products.append([name, price, rating])
        
        save_to_csv(products)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def save_to_csv(data):
    filename = "product_data.csv"
    file_path = os.path.abspath(filename)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Rating"])
        writer.writerows(data)
        print(f"Data has been saved successfully to: {file_path}")
    messagebox.showinfo("Success", f"Data has been saved to {file_path}")

def fetch_data():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
    else:
        scrape_data(url)

root = tk.Tk()
root.title("Product Data Scraper")
root.geometry("400x200")

label_url = tk.Label(root, text="Enter E-commerce URL:")
label_url.pack(pady=10)

entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

button_scrape = tk.Button(root, text="Scrape Data", command=fetch_data)
button_scrape.pack(pady=20)

root.mainloop()
