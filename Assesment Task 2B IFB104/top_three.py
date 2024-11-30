
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 2, 2024.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#  Put your student number here as an integer and your name as a
#  character string:
#
student_number = 12157627
student_name   = 'Fartun M Said'
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment task you will combine your knowledge of Python
#  programming, HTML-style mark-up languages, pattern matching,
#  database management, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows its user to view and save
#  data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#



#-----Set up---------------------------------------------------------#
#
# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar



# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  You are not required to use this function, but it may
# save you some effort.  Feel free to modify the function or copy
# parts of it into your own code.
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.  However, the root cause of the
# problem is not always easy to diagnose, depending on the quality
# of the response returned by the web server, so the error
# messages generated by the function below are indicative only.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (not recommended!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; ' + \
                               'rv:91.0; ADSSO) Gecko/20100101 Firefox/91.0')
            print("Warning - Request to server does not reveal client's true identity.")
            print("          Use this option only if absolutely necessary!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError as message: # probably a syntax error
        print(f"\nCannot find requested document '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except HTTPError as message: # possibly an authorisation problem
        print(f"\nAccess denied to document at URL '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except URLError as message: # probably the wrong server address
        print(f"\nCannot access web server at URL '{url}'")
        print(f"Error message was: {message}\n")
        return None
    except Exception as message: # something entirely unexpected
        print("\nSomething went wrong when trying to download " + \
              f"the document at URL '{str(url)}'")
        print(f"Error message was: {message}\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as message:
        print("\nUnable to decode document from URL " + \
              f"'{url}' as '{char_set}' characters")
        print(f"Error message was: {message}\n")
        return None
    except Exception as message:
        print("\nSomething went wrong when trying to decode " + \
              f"the document from URL '{url}'")
        print(f"Error message was: {message}\n")
        return None

    # Optionally write the contents to a local text file
    # (silently overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(f'{target_filename}.{filename_extension}',
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print(f"\nUnable to write to file '{target_filename}'")
            print(f"Error message was: {message}\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# 
# Create the main window
main_window = Tk()
main_window.title('Top Music Hits')
main_window.configure(bg='white')

#--------------------------------------------------------------

# Update function for messages
def update_output(text):
    message_label.config(text=text)


# Function to display the top hits and handling errors
def show_hits():
    ranking_selection = ranking_var.get()
    if ranking_selection == "none" or ranking_selection == "":
        update_output("Please select a ranking to view.")
    else:
        try:
            show_text.delete(1.0, END)
            top_hits = extract_top_hits(ranking_selection)
            if top_hits:
                show_text.insert(END, "\n".join(top_hits))
                update_output(f"Top three hits ")
            else:
                update_output("No hits found for the selected ranking.")
        except Exception as e:
            update_output("Unable to access the hits.\nPlease check your internet connection.")


# Function for showing the different Webistes
def show_details():
    ranking_selection = ranking_var.get()

    urls = {
        "aussiehits": "https://www.aria.com.au/charts/australian-artist-singles-chart/",  
        "americanhits": "https://www.americantop40.com/charts/top-40-238/latest/",
        "nzhits": "https://nztop40.co.nz/chart/singles"
    }

    if ranking_selection in urls:
        url = urls[ranking_selection]
        urldisplay(url) 
    else:
        update_output("Please select a ranking option.")

# Extract top hits from the selected websites
def extract_top_hits(ranking_selection):
    # Open the URL and read the page content
    urls = {
        "aussiehits": "https://www.aria.com.au/charts/australian-artist-singles-chart/", 
        "americanhits": "https://www.americantop40.com/charts/top-40-238/latest/",
        "nzhits": "https://nztop40.co.nz/chart/singles"
    }
    
    url = urls[ranking_selection]
    response = urlopen(url)
    html_code = response.read().decode('UTF-8')
    response.close()

    # Markers 
    if ranking_selection == "aussiehits":
        song_start_marker = '<a class="c-chart-item__title">' 
        song_end_marker = '</a>'  
        artist_start_marker = '<a class="c-chart-item__artist">'  
        artist_end_marker = '</a>' 
    elif ranking_selection == "americanhits":
        song_start_marker = 'class="track-title" target="_blank" rel="noopener">'
        song_end_marker = '</a>'
        artist_start_marker = 'class="track-artist" target="_blank" rel="noopener">'
        artist_end_marker = '</a>'
    elif ranking_selection == "nzhits":
        song_start_marker = '<h2 class="title"><span>'
        song_end_marker = '</span></h2>'
        artist_start_marker = '<h3 class="artist"><span>'
        artist_end_marker = '</span></h3>'

    # Initializing a list to hold the top hits
    top_hits = []
    start_position = 0

    # Extracting the top three song titles and artist names
    for i in range(3):
        song_start_position = html_code.find(song_start_marker, start_position)
        song_end_position = html_code.find(song_end_marker, song_start_position)
        artist_start_position = html_code.find(artist_start_marker, song_end_position)
        artist_end_position = html_code.find(artist_end_marker, artist_start_position)

        if song_start_position == -1 or artist_start_position == -1:
            break

        # Extracting song title and artist name
        song = html_code[song_start_position + len(song_start_marker): song_end_position].strip()
        artist = html_code[artist_start_position + len(artist_start_marker): artist_end_position].strip()

        start_position = artist_end_position
        
        # Make it to a list
        top_hits.append(f"{i + 1}. {artist} - {song}")

    return top_hits


#Saving the ranking to the database
import sqlite3
def save_to_database(data_source, ranking, identifier, property):
    try:
        # Connect to the existing database
        conn= sqlite3.connect('saved_rankings.db')
        sql_cursor = conn.cursor()
        
        insert_command = "INSERT INTO rankings (data_source, ranking, identifier, property) VALUES (?, ?, ?, ?)"
        
        # Execute the insertion 
        sql_cursor.execute(insert_command, (data_source, ranking, identifier, property))
        
        # Commit 
        conn.commit()
        update_output("Database updated successfully.")
    except sqlite3.Error as e:
        update_output(f"Error saving ranking: {e}")
    finally:
        #Closing the conn
        if conn:
            conn.close()

#Mapping for names 
ranking_names = {
    "aussiehits": "ARIA Top Australian Singles",
    "americanhits": "American top hits",
    "nzhits": "New Zealand top singles"
}

# Function for saving and handling errors 
def save_selection(rank):
    selection = ranking_var.get()
    
    if selection != "none":
        try:
            top_hits = extract_top_hits(selection)
            
            if rank <= len(top_hits):  
                artist_song = top_hits[rank - 1].split(" - ")
                identifier = artist_song[0].strip()  
                property = artist_song[1].strip()  
                
                data_source = selection 
                ranking = rank  

                # Removing the number when saving for it in the identifier 
                identifier = identifier.split(". ", 1)[1] if ". " in identifier else identifier
                # Displaying names for the data_source in db
                data_source = ranking_names.get(selection, selection)
                ranking = rank  
                
                # Save to the database
                save_to_database(data_source, ranking, identifier, property)
            else:
                update_output("Rank not found.")
        except Exception as e:
            update_output("Unable to save the rank.\nPlease check your internet connection.")
    else:
        update_output("You must choose something to save.")

#----------------------------------------------------------------------------

# Creating a frame for the image
hits_frame = Frame(main_window, bg='white')
hits_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

# Importing the image
hits_image = PhotoImage(file='hits.gif')

# Label to display the image in the frame
img_label = Label(hits_frame, image=hits_image, bg='#ffd0d7')
img_label.pack()

# Frame for the ranking options
ranking_frame = Frame(main_window, bg='#ffd0d7', relief='ridge', borderwidth=1)
ranking_frame.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')

# Label for ranking frame
Label(ranking_frame, text="Choose and view top hits!", bg='#ffd0d7', font=('Arial', 14)).pack(anchor='w')

# Buttons for ranking options
ranking_var = StringVar(value="none")
Radiobutton(ranking_frame, text="ARIA Top Australian Singles", variable=ranking_var, value="aussiehits", bg='#ffd0d7', command=lambda: update_output("Selected: ARIA Top Australian Singles")).pack(anchor='sw')
Radiobutton(ranking_frame, text="American top hits", variable=ranking_var, value="americanhits", bg='#ffd0d7', command=lambda: update_output("Selected: American top hits")).pack(anchor='w')
Radiobutton(ranking_frame, text="New Zealand top singles", variable=ranking_var, value="nzhits", bg='#ffd0d7', command=lambda: update_output("Selected: New Zealand top singles")).pack(anchor='w')

# Buttons to view top three or details
Button(ranking_frame, text="Show top three", command=show_hits).pack(side='left', padx=20, pady=5)
Button(ranking_frame, text="Show website", command=show_details).pack(side='right', padx=20, pady=5)

# Frame for the saved items
save_frame = Frame(main_window, bg='#ffd0d7', relief='ridge', borderwidth=1)
save_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

# Label for saving frame
Label(save_frame, text="Save", bg='#ffd0d7', font=('Arial', 14)).pack(anchor='w')

# Buttons to save 1, 2, 3 from the list
Button(save_frame, text="Rank 1", command=lambda: save_selection(1)).pack(pady=5)
Button(save_frame, text="Rank 2", command=lambda: save_selection(2)).pack(pady=5)
Button(save_frame, text="Rank 3", command=lambda: save_selection(3)).pack(pady=5)

# Message frame
message_frame = Frame(main_window, bg='#ffd0d7', relief='ridge', borderwidth=1)
message_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# Displaying messages
message_label = Label(message_frame, text="Message", bg='#ffd0d7', font=('Arial', 14))
message_label.pack(fill='x')

# Text area to display the top hits
show_text = Text(main_window, height=5, width=50, bg='white')
show_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the event loop to detect user inputs
main_window.mainloop()

