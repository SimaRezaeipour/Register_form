import streamlit as st 
import pandas as pd 
import numpy as np 
import os 
from datetime import datetime
import exifread
import streamlit.components.v1 as stc 
import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

metadata_wiki = """

"""

HTML_BANNER = """
    <div style="background-color:#364e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Power BI Presentation
 </h1>
 <h2 style="color:white;text-align:center;">Lecturer: Iman Eftekhari </h2>
 
    </div>
    """
HTML_BANNER2 = """
    <div style="background-color:#364e5f;padding:10px;border-radius:10px">
   
 <h2 style="color:white;text-align:center;">Jun 15, 2021 07:00 PM Canberra, Melbourne, Sydney</h2>

    </div>
    """
@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img

def get_readable_time(mytime):
	return datetime.fromtimestamp(mytime).strftime('%Y-%m-%d-%H:%M')

def make_downloadable(data):
	csvfile = data.to_csv(index = False)
	b64 = base64.b64encode(csvfile.encode()).decode()
	st.markdown("### ** 📥 ⬇️ Download CSV File **")
	new_filename = "metadata_result_{}.csv".format(timestr)
	href = f'<a href="data:file/csv;base64,{b64}" download = "{new_filename}">Click Here!</a>'
	st.markdown(href,unsafe_allow_html=True)

def create_uploaded_filetable():
	c.execute('CREATE TABLE IF NOT EXISTS filestable(name TEXT,family TEXT, occupation TEXT, interest TEXT, other TEXT)')

def add_file_details(name,family, occupation,interest,other):
	#c.execute(' INSERT INTO filestable  (name,family, occupation,interest,other) VALUES (?,?,?,?,?) WHERE NOT EXISTS (SELECT * FROM filestable WHERE name = "Sima" AND family = "Reza") ' ,(name,family, occupation,interest, other)) #WHERE NOT EXISTS ( SELECT * FROM filestable WHERE name = "Sima" AND family = "Reza")

	c.execute('INSERT INTO filestable(name,family, occupation,interest,other) VALUES (?,?,?,?,?) ' ,(name,family, occupation,interest, other)) #WHERE NOT EXISTS ( SELECT * FROM filestable WHERE name = "Sima" AND family = "Reza")
	conn.commit()

def view_all_data():
	c.execute('SELECT * FROM filestable ')
	data = c.fetchall()
	return data 



def main():
	st.image(load_image("pbi2.png"))
	stc.html(HTML_BANNER)
	stc.html(HTML_BANNER2)
	menu = ["Home","Register"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_uploaded_filetable()
	if choice == "Home":
		#st.subheader("Home")
		st.image(load_image("pbi.png"))
		st.write(metadata_wiki)

		
	

	elif choice == "Register":
		#st.subheader("Insert your information here:")
		
		with st.beta_expander("Insert your information here:"):
			input1 = st.empty()
			input2 = st.empty()
			input3 = st.empty()
			
			other=" "
			name = input1.text_input("* Name:", value = "")
			family = input2.text_input("* Family:", value = "")
			occupation = input3.text_input(" Occupation:", value = "")
			#m = st.multiselect("Interested in :",['Data Scientist','Data Analyst','BI Specialist', 'Business Analyst', 'Power BI Developer', 'other'])
			interest = st.radio("Interested in :",['Data Scientist','Data Analyst','BI Specialist', 'Business Analyst', 'Power BI Developer', 'Other'])
			if interest == "Other":
				input4 = st.empty()
				other =  input4.text_area("Others")
			if st.button("Submit"):
				add_file_details(name, family,occupation,interest,other)
				name = input1.text_input("* Name:", value = " ")
				family = input2.text_input("* Family:", value = " ")
				occupation = input3.text_input(" Occupation:", value = " ")
				if interest == "Other":
					other = input4.text_area("Others", value = " ")
				st.success("Registered successfully")
				st.write('''Here is the link of the presentation:\n  
Join Zoom Meeting
https://us05web.zoom.us/j/82574739442?pwd=WWRqSmdpU0dvUW4yOEwwRkFpSmJwdz09

Meeting ID: 825 7473 9442
''')
				st.write("Passcode: An9fr4")
				#st.write(view_all_data())
				
			
			


	


if __name__== "__main__":
	main()
