from tkinter import *
from PIL import ImageTk, Image
import requests
import json
from io import BytesIO
from tkinter import messagebox

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZjI2NGQwYjdmNWIxNjFjOTM2MmZlYWU2NmU1YTkyMyIsInN1YiI6IjY1YTJiMDVhYjdiNjlkMDEzMTNjMDE1OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FrX3hrih4lNBUuzpDe5e8hrTxhb_wyBzIaHlBA9VKtM"
}

link = "https://api.themoviedb.org/3/discover/movie"
response = requests.get(link, headers=headers)
link2 = "https://api.themoviedb.org/3/discover/tv"
response2 = requests.get(link2, headers=headers)


if response.status_code == 200:
    data = response.json()
    with open("movie.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        
if response2.status_code == 200:
    data2 = response2.json()
    with open("tvshow.json", "w", encoding="utf-8") as json_file:
        json.dump(data2, json_file, ensure_ascii=False, indent=2)
        
#MOVIE FRAME FUNCTION 

def perform_search():
    query = search_entry1.get()
    if query:
        search_url = "https://api.themoviedb.org/3/search/movie"
        base_image_url = "https://image.tmdb.org/t/p/w500"
        api_key = '0f264d0b7f5b161c9362feae66e5a923'  
        headers = {'Authorization': 'Bearer ' + api_key}
        params = {'query': query, 'api_key': api_key}
        
        response = requests.get(search_url, headers=headers, params=params)
        data = response.json()

        if 'results' in data and data['results']:
            # Display information for the first result
            result = data['results'][0]
            movie_title = result['original_title']
            output.config(text=movie_title)

            movie_overview = result["overview"]
            output1.config(text=movie_overview)

            movie_id = result["id"]
            output2.config(text=movie_id)

            movie_release_date = result["release_date"]
            output3.config(text=movie_release_date)

            # Clear the previous image if any
            for widget in image_frame.winfo_children():
                widget.destroy()

            # Display image for the first result
            if 'poster_path' in result:
                image_path = result['poster_path']
                full_image_url = base_image_url + image_path

                image_response = requests.get(full_image_url)
                if image_response.status_code == 200:
                    image = Image.open(BytesIO(image_response.content))
                    image = image.resize((160, 230))
                    image = ImageTk.PhotoImage(image)
                    image_label = Label(image_frame, image=image, padx=0, pady=0)
                    image_label.image = image
                    image_label.pack(side=LEFT)
        else:
            
            output.config(text="Movie not found")
            for widget in image_frame.winfo_children():
                widget.destroy()

                
#TV SHOW FUNCTION SEARCH 

def tv_show_search():
    query = search_entry.get()
    if query:
        search_url = "https://api.themoviedb.org/3/search/tv"
        base_image_url = "https://image.tmdb.org/t/p/w500"
        params = {'query': query, 'api_key': '0f264d0b7f5b161c9362feae66e5a923'} 
        response = requests.get(search_url, params=params)
        data = response.json()

        if 'results' in data and data['results']:
            result = data['results'][0]

            tv_title = result['original_name']
            title_output.config(text=tv_title)

            tv_overview = result["overview"]
            overview_output.config(text=tv_overview)

            tv_id = result["id"]
            id_output.config(text=tv_id)

            tv_release_date = result["first_air_date"]
            release_date_output.config(text=tv_release_date)

            for widget in image_frame2.winfo_children():
                widget.destroy()

                # Display image for each result
            if 'poster_path' in result:
                image_path = result['poster_path']
                full_image_url = base_image_url + image_path

                image_response = requests.get(full_image_url)
                if image_response.status_code == 200:
                        image = Image.open(BytesIO(image_response.content))
                        image = image.resize((160, 230))    
                        image = ImageTk.PhotoImage(image)
                        image_label = Label(image_frame2, image=image, padx=0, pady=0)
                        image_label.image = image
                        image_label.pack(side=LEFT)
        else:
            # Handle the case when no results are found
            tv_output.config(text="TV shows not found")
            for widget in image_frame2.winfo_children():
                widget.destroy()


def navigate_to_section(section_name):
    # Hide all frames
    home_frame.pack_forget()
    movies_frame.pack_forget()
    tv_shows_frame.pack_forget()
    

    # Show the selected frame
    if section_name == "Home":
        home_frame.pack()
    elif section_name == "Movies":
        movies_frame.pack()
    elif section_name == "TV Shows":
        tv_shows_frame.pack()

def instructions():
    message = "This app gives information about the movies  and tv shows you are looking for. \n \n Click the home or tv shows button and search it in the seeach entry."
    messagebox.showinfo("Instructions",message)


root = Tk()
root.title("Test")
root.geometry("500x500")
root.configure(bg="black")


#Frames 
movies_frame = Frame(root, width="500", height="500", bg="black")
movies_frame.place(relx=1, anchor=NE)

tv_shows_frame = Frame(root, width="500", height="500", bg="black")
tv_shows_frame.place(relx=1, anchor=NE)

home_frame = Frame(root, width="500", height="500", bg="black")
home_frame.place(relx=1, anchor=NE)

#HOME FRAME WIDGETS

InstructionButton = Button(home_frame, text = "Instructions", bg="white" ,fg="green",font=('Roboto',15,'bold'),command=instructions)
InstructionButton.place(x=180, y=330)

paragraph_text = "Made by Aliyah San Pedro"
paragraph = Label(home_frame, text=paragraph_text, fg="white", bg="black", font=('Roboto', 20))
paragraph.place(x=75, y=180)

paragraph_text = "What is Nflicks?."
paragraph = Label(home_frame, text=paragraph_text, fg="white", bg="black")
paragraph.place(x=75, y=233)

paragraph_text = "Nflicks is a movie and tv show finder which helps the user to find"
paragraph = Label(home_frame, text=paragraph_text, fg="white", bg="black")
paragraph.place(x=75, y=260)

paragraph_text = "details about the movie or tv show they want to check ."
paragraph = Label(home_frame, text=paragraph_text, fg="white", bg="black")
paragraph.place(x=75, y=275)

# Open the first image using PIL
img1 = Image.open("image1.jpg")
resized_image1 = img1.resize((95, 40))
new_image1 = ImageTk.PhotoImage(resized_image1)

label1 = Label(root, image=new_image1, bd=0)
label1.pack(anchor=NW)

# Open the second image using PIL    
img2 = Image.open("image2.jpg")
resized_image2 = img2.resize((200, 70))
new_image2 = ImageTk.PhotoImage(resized_image2)

window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
x_position2 = (window_width - -94) // 2
y_position2 = (window_height - 80) // 2

label2 = Label(root, image=new_image2, bd=0)
label2.place(x=x_position2, y=y_position2)

# Navigation bar
navbar_frame = Frame(root, bg="black")
navbar_frame.place(relx=1, anchor=NE)

movies_button = Label(navbar_frame, text="Movies", fg="white", bg="black", padx=10, pady=5, cursor="hand2")
movies_button.pack(side=RIGHT)
movies_button.bind("<Button-1>", lambda event: navigate_to_section("Movies"))

tv_shows_button = Label(navbar_frame, text="TV Shows", fg="white", bg="black", padx=10, pady=5, cursor="hand2")
tv_shows_button.pack(side=RIGHT)
tv_shows_button.bind("<Button-1>", lambda event: navigate_to_section("TV Shows"))

home_button = Label(navbar_frame, text="Home", fg="white", bg="black", padx=10, pady=5, cursor="hand2")
home_button.pack(side=RIGHT)
home_button.bind("<Button-1>", lambda event: navigate_to_section("Home"))


#MOVIE FRAME WIDGETS 

search_entry1 = Entry(movies_frame, bg="white", fg="black", width=30, borderwidth=0)
search_entry1.place(x=150, y=100)  

search_button = Button(movies_frame, text="Search", bg="black", fg="white", command=perform_search, borderwidth=0)
search_button.place(x=170 + 180, y=100)  

label1 = Label(movies_frame, text="Title: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label1.place(x=221, y=160)

output = Label(movies_frame, text="", bg="black", fg="white", font=('Roboto', 11),wraplength=220,anchor='center')
output.place(x=270, y=160)

label2 = Label(movies_frame, text="ID: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label2.place(x=221, y=200)

output2 = Label(movies_frame, text="", bg="black", fg="white", font=('Roboto', 11), wraplength=180)
output2.place(x=280, y=200)

label3 = Label(movies_frame, text="Release-Date: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label3.place(x=221, y=240)

output3 = Label(movies_frame, text="", bg="black", fg="white", font=('Roboto', 11), wraplength=180)
output3.place(x=330, y=240)

label4 = Label(movies_frame, text="Overview: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label4.place(x=221, y=280)

output1 = Label(movies_frame, text="", bg="black", fg="white", font=('Roboto', 8), wraplength=260)
output1.place(x=230, y=310)

#TV SHOW FRAME WIDGETS

tv_output= Label(tv_shows_frame, text="", bg="black", fg="white", font=('Roboto', 11),wraplength=95,anchor='center')
tv_output.place(x=235, y=145)

search_entry = Entry(tv_shows_frame, bg="white", fg="black", width=30, borderwidth=0)
search_entry.place(x=150, y=100)   

search_button = Button(tv_shows_frame, text="Search", bg="black", fg="white", command=tv_show_search, borderwidth=0)
search_button.place(x=170 + 180, y=100)

label1 = Label(tv_shows_frame, text="Title: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label1.place(x=221, y=160)

title_output = Label(tv_shows_frame, text="", bg="black", fg="white", font=('Roboto', 11),wraplength=220,anchor='center')
title_output.place(x=270, y=160)

label2 = Label(tv_shows_frame, text="ID: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label2.place(x=221, y=200)

id_output = Label(tv_shows_frame, text="", bg="black", fg="white", font=('Roboto', 11), wraplength=180)
id_output.place(x=280, y=200)

label3 = Label(tv_shows_frame, text="Release-Date: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label3.place(x=221, y=240)

release_date_output = Label(tv_shows_frame, text="", bg="black", fg="white", font=('Roboto', 11), wraplength=180)
release_date_output.place(x=330, y=240)

label4 = Label(tv_shows_frame, text="Overview: ", bg="black", fg="white", font=('Roboto', 11),wraplength=120,anchor='center')
label4.place(x=221, y=280)

overview_output = Label(tv_shows_frame, text="", bg="black", fg="white", font=('Roboto', 8), wraplength=260)
overview_output.place(x=230, y=310)

image_frame = Frame(movies_frame, bg="black")
image_frame.place(x=32, y=170)

image_frame2 = Frame(tv_shows_frame, bg="black")
image_frame2.place(x=32, y=170)

# Initial navigation to the Home section
navigate_to_section("Home")

root.resizable(0,0)
root.mainloop()