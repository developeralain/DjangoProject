# DjangoProject
My first application and project, created in 2 weeks during the live project portion of my TechAcademy boot camp. It used the Django Framework and Bootstrap4.
# Live Project
### Introduction

*Please note: you may view the application in action, as well as hear my narration of its features, by clicking the following YouTube image link to my video:*

<a href="http://www.youtube.com/watch?feature=player_embedded&v=NfGk2z3rD3Y
" target="_blank"><img src="http://img.youtube.com/vi/yhTrgGjiwh0/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

For the last two weeks of my time at The Tech Academy, I worked alongside my peers in developing a full stack web application using the Django Framework and Python. 

We were each tasked with completing a series of stories to achieve a certain set of functionalities for our app. 

In addition to the Django Framework, I made use of Bootstrap4 and JQuery for the front-end of my application. 

The theme of my application was 'Nutrition' and I chose to create the following features:

- Allowing users to create an account and populate user details
- Allowing users to create Nutritional Paths to follow that are associated with a given account
- Incorporating CRUD functionality by enabling visualization of all database tables on the front-end, as well as the ability to edit or delete any table entry
- Utilizing BeautifulSoup to scrape a popular Nutrition website and extract the latest supplement news story summaries and headlines for the end user to see
- Connecting to the Nutritionix API and allowing users to search for nutritional information pertaining to any food item
- Allowing users to save API responses to the database for future reference

### Back End Stories
- [Generating Models](#generating-database-models)
- [Displaying Tables](#creating-database-table-display-functionality)
- [Editing a Table Entry](#creating-edit-functionality-for-a-specific-table-entry)
- [Deleting a Table Entry](#creating-delete-functionality-for-a-specific-table-entry)
- [Displaying Scraped Data](#creating-functionality-to-display-scraped-data)
- [Display API Response](#create-functionality-to-access-API-and-view-the-response)
- [Save API Response](#enabling-the-saving-of-API-responses-to-our-database)

### Other Sections Navigation
- [Skip to Front End Stories](#front-end-stories)
- [Skip to Other Skills Learned](#other-skills-learned)


#### Generating Database Models 

Created models for the user and nutritional path

Screenshot

#### Creating Database Table Display functionality

Create the views and templates required to render the existing user and nutrition path tables in the database

Screenshot
GIF

#### Creating Edit Functionality for a specific table entry

Created the  views and templates needed to view the full details of a given table entry and edit those details 
 
Screenshot
GIF

#### Creating Delete Functionality for a specific table entry

Created the views and templates required to confirm a record deletion, perform the delete on a record, and redirect the user back to the database table display page

Screenshot
GIF

#### Creating functionality to display scraped data 

Implemented the BeautifulSoup library in targeting specific HTML elements on a nutritional supplement webpage. Created a view that would strip the markup language from the scraped data and render it via table format on a template. Incorporated a page refresh button to allow for latest data from webpage to be displayed.

Screenshot
GIF

#### Create functionality to access API and view the response 

Created a view that was able to send an API request, along with required API keys and credentials, to the Nutritionix API. 
Further, it was able to take the response--which was a messy JSON dictionary--and filter it for only a select few KVPs that I needed. I then made a template to allow users to make queries, and then I connected this template to the same view so that a query would be included in the API request. 
I made another template that served to unpack the data in a neat tabular format for the user to see upon making a search query. 

Screenshot
GIF

#### Enabling the saving of API responses to our database 

I created a modified version of the above view that would not only render the response to a user query, but would also automatically save any query, along with the targeted response data, to the database for future reference.

Screenshot
GIF

### Front End Stories
#### Bootstrap4 and Jquery

Leveraged Bootstrap4 and Jquery to create the application theme and aesthetics. I kept things simple and clean, while leaving special effects and eye-catchers to a minimum. 

Screenshot
GIF

### Other Skills Learned

Throughout this live project experience I was able to acquire and develop many non-coding skills that are yet important to the 
development process. These included such things as:
- Adhering to the Agile and Scrum methodologies of project management throughout the process
	- Attended daily standups to discuss what was done, what was to be done, and any roadblocks
	- Attended weekly retrospectives to look back on the week's accomplishments, setbacks, and discuss any ideas for improvements
	to improve the experience and ultimately the end-product
	- A work pattern of frequent commits that are small and allow for easier management of code as the project progresses
- DevOps with Azure, including Git concepts
	- Identifying assigned stories on the storyboard and creating new working branches accordingly
	- Committing and pushing completed working branches and generating pull requests
	- Updating local master branch, checking out branches, merging branches as required 
	- Addressing pull request rejections and re-submitting working branches along with clear documentation
- Research and Problem-Solving Abilities
	- Break apart a larger problem into smaller components and research how to implement each component specifically
	- Debug an issue by understanding what the errors are pointing at and tracing my steps back to those areas--iterating
	accordingly until the problem is solved 
	- Learn new technologies, quickly, as the project demands require, and implement those skills specifically to the task at
	hand
- Communication and pair programming
	- Clearly articulate the problem, including enough contextual info, so that a fellow programmer can assist in resolving it
	- Focused and stepwise approach to dissecting a problem with a colleague to get at the root of the problem 
	- Explaining my own code clearly to another so that their understanding, as well as my own, is enhanced and they can resolve their
	code impasse and proceed successfully
