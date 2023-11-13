import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import json
from PIL import Image, ImageTk
import io

def fetch_data():
    response = requests.get('https://restcountries.com/v3.1/all?fields=name,region,flags,capital')
    return json.loads(response.text)

def update_countries(event):
    selected_continent = continent_combobox.get()
    countries_listbox.delete(0, tk.END)
    for country in data:
        if country['region'] == selected_continent:
            countries_listbox.insert(tk.END, country['name']['common'])

def update_country_info(event):
    selected_country = countries_listbox.get(countries_listbox.curselection())
    for country in data:
        if country['name']['common'] == selected_country:
            country_label.config(text='Country: ' + country['name']['common'])
            capital_label.config(text='Capital: ' + country['capital'][0])
            
            # Fetch the image from the URL
            response = requests.get(country['flags']['png'])
            image_bytes = io.BytesIO(response.content)

            # Create a PIL image object and then create a Tkinter ImageTk object
            pil_image = Image.open(image_bytes)
            tk_image = ImageTk.PhotoImage(pil_image)

            # Update the label to display the image
            flag_label.config(image=tk_image)
            flag_label.image = tk_image  # keep a reference to the image to prevent it from being garbage collected
data = fetch_data()

root = tk.Tk()
root.geometry('400x500')
continent_combobox = ttk.Combobox(root, values=list(set(country['region'] for country in data)))
continent_combobox.bind('<<ComboboxSelected>>', update_countries)
continent_combobox.pack()

countries_listbox = tk.Listbox(root)
countries_listbox.bind('<<ListboxSelect>>', update_country_info)
countries_listbox.pack()

country_label = tk.Label(root, text="")
country_label.pack()

capital_label = tk.Label(root, text="")
capital_label.pack()

flag_label = tk.Label(root, text="")
flag_label.pack()

root.mainloop()