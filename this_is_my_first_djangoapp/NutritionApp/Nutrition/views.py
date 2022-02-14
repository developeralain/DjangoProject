
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Account, PersonalizedNutrition, NutritionixInfoReceived
from .forms import AccountForm, NutritionalQuery
import requests
import json
from bs4 import BeautifulSoup
import pprint
# Create your views here.

#Home page view
def nutrition_home(request):
    return render(request, 'Nutrition/Nutrition_home.html')

#Create account view
def create_account(request):
    form = AccountForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('Nutrition_home')
    content = {'form': form}
    return render(request, 'Nutrition/Nutrition_createnewaccount.html', content)
"""First time this view is called, it skips the IF statement (as it would be a GET Request) and renders the 
Nutrition_createnewaccount page. The second time this view is called is when the user clicks the Submit button to submit 
their completed form. This is coded as a POST and would trigger the IF statement, saving the form fields as an entry in 
the form object's corresponding table in the database."""

#create a nutrition path view
def make_query(request):
    form = NutritionalQuery(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('Nutrition_home')
    content = {'form': form}
    return render(request, 'Nutrition/Nutrition_makequery.html', content)
"""Same logic applies here as the create_account view above."""

#display database table entries view for both account and nutrition path tables
def display_db(request):
    accounts = Account.Accounts.all() #collect account table records and store in variable
    nutritionqueries = PersonalizedNutrition.Personalized.all() #collect nutrition path table records and store

    content = {'accounts': accounts, 'nutritionqueries': nutritionqueries}
    return render(request, 'Nutrition/Nutrition_displaydb.html', content)
"""The above view collects and stores records for each table in a separate variable. These accounts and nutritionqueries
records are passed on to the template as dictionaries"""


#Displays account details view, showing the entire record details for a given record in Account table per its primary key
def display_account_details(request, pk):
    item = get_object_or_404(Account, pk=pk) #stores single record corresponding to primary key in variable 'item'

    # above : query dB table 'Account' for all data on that particular account (i.e. that particular record/row).

    return render(request, 'Nutrition/Nutrition_details.html', {'item': item})

    # on the page this view is taking us to, user will have a chance to make edits to the row/entry he selected


#Displays nutrition path details view, showing the entire record details for a given record in the PersonalizedNutrition
#table
def display_nutrition_details(request, pk):
    nutrition_item = get_object_or_404(PersonalizedNutrition, pk=pk)

    # above : query dB for all data on that particular account

    return render(request, 'Nutrition/Nutrition_details.html', {'nutrition_item': nutrition_item})

    # on the page this view is taking us to, user will have a chance to make edits to the row/entry he selected



#This view first takes us to template that confirms our wish to delete a record, then it performs the deletion.
def delete_account(request, pk):

    item = get_object_or_404(Account, pk=pk)
    if request.method == 'POST': #initially this will be called on a GET, not a post
                                #as it will GET the confirmdelete.html page to confirm a POST before posting.
        item.delete()
        return redirect('display_db') #go back to products_page after confirming delete
    context = {"item": item,} #passing the record as a dictionary item into context variable
    return render(request, "Nutrition/Nutrition_confirmdelete.html", context)#takes you to a page to confirm your intention


#Same logic as above view, except this pertains to confirming a record deletion of the PersonalizedNutrition table
def delete_nutrition(request, pk):

    item = get_object_or_404(PersonalizedNutrition, pk=pk)
    if request.method == 'POST': #initially this will be called on a GET, not a post
                                #as it will GET the confirmDelete.html page to confirm a POST before posting.
        item.delete()
        return redirect('display_db') #go back to products_page after confirming delete
    context = {"item": item,} #passing the record as a dictionary item into context variable
    return render(request, "Nutrition/Nutrition_confirmdelete.html", context)#takes you to a page to confirm your intention


#Upon selecting a record from the displayed account table, this view takes the user to a template that allows for edits
def edit_account(request, pk):

    item = get_object_or_404(Account, pk=pk)
    # above : query dB for all data on that particular Account
    aform = AccountForm(data=request.POST or None, instance=item)

    """the data will be from request object's post method...the instance will be all the info for 
    that item...we're saying take the item info (instance) and put it into the fields of that form 
    and call it form so it may be displayed to the user for editing purposes."""

    if request.method == 'POST':
        if aform.is_valid():
            aform2 = aform.save(commit=False)
            aform2.save()
            return redirect('display_db')
        else:
            print(aform.errors)
    #STEP 2: the above if statements will run once the user has made item changes and submitted them (POST)
    else:
        return render(request, 'Nutrition/Nutrition_edit.html', {'aform': aform})
    # this else says we will be rendering the edit page for the user FIRST (STEP 1):

    """as you can see above, the form variable has been passed on to the render so that the 
    form with item fields filled in can be rendered on the user's screen...form variable is 
    passed on to the render and will be rendered within the edit page"""


#This view performs same function/logic as edit_account view above, except it targets the NutritionalQuery table.
def edit_nutrition(request, pk):
    item = get_object_or_404(PersonalizedNutrition, pk=pk)
    # above : query dB table for all data on that particular product
    nform = NutritionalQuery(data=request.POST or None, instance=item)
    """the data will be from request object's post method...the instance will be all the info for 
    that item...we're saying take the item info (instance) and put it into the fields of that form 
    and call it form so it may be displayed to the user for editing purposes"""
    if request.method == 'POST':
        if nform.is_valid():
            nform2 = nform.save(commit=False)
            nform2.save()
            return redirect('display_db')
        else:
            print(nform.errors)
    # STEP 2: the above if statements will run once the user has made item changes and submitted them (POST)
    else:
        return render(request, 'Nutrition/Nutrition_edit.html', {'nform': nform})
    # this else says we will be rendering the edit page for the user FIRST (STEP 1):

    """as you can see above, the form variable has been passed on to the render so that the 
    form with item fields filled in can be rendered on the user's screen...form variable is 
    passed on to the render and will be rendered within the present_product page"""


#_________________BELOW CODE REPRESENTS THE WEB SCRAPER FUNCTIONALITY OF THE APPLICATION_______________________________

def scraper(request):
    page = requests.get('https://www.nutraingredients-usa.com/')
    #above line store a get request for target website in variable 'page'

    soup = BeautifulSoup(page.content, 'html.parser')
    #Above line calls BeautifulSoup and HTML partser and, using page variable, collects and parses the page content.

    nutrition_data = dict()
    #initializes an empty dictionary variable

    refined = soup.find_all('div', class_='Teaser-text')
    """Above line finds all instances of a div of class 'Teaser-text' within the contents of 'soup' and extracts only 
    them, storing them in 'refined' variable. Here, your arguments should correspond to whatever page content you want
    extracted. You would target this desired content by looking at what unique classes/ids are associated with them.
    """
    """Refined will be a list variable with only one element that is comprised of a bunch of html markup and content
    data from the target webpage per your arguments of WHAT to extract-out specifically. Here it will be the contents
    of all the div tags with class 'Teaster-text' in the form of a list with ONE element. I.E. data is not organized."""

    nutrition_data['values'] = [pt.get_text() for pt in refined]
    """the above uses list comprehension to strip the markup of the 'refined' list and store just the
    text we want as a new dictionary called 'nutrition_data'. This creates an embedded list under the key 'values'.
    Further, this also parses the giant block of content represented as a single list element into several separate 
    elements within the list. Each element is defined by the start of the 'div' tag and the end of this tag. Thus, we
    have created an organized list with each element representing a distinct piece of content we wish to display.
    """
    return render(request, 'Nutrition/Nutrition_scrapedcontent.html',{'nutrition_data': nutrition_data})

"""The above function scrapes https://www.nutraingredients-usa.com/ ... specifically, it looks at the 
'div' tags of class 'Teaser-text' located within the overall contents of this web page and extracts only those. 

"""


#the below is the logic for a button-triggered scrape that takes you to, and displays results in, home page
"""  
def scraper(request):
    if request.method == 'POST':
        page = requests.get('https://www.nutraingredients-usa.com/')
        soup = BeautifulSoup(page.content, 'html.parser')
        nutrition_data = dict()
        refined = soup.find_all('div', class_='Teaser-text')
        nutrition_data['values'] = [pt.get_text() for pt in refined]
        return render(request, 'Nutrition/Nutrition_home.html',{'nutrition_data': nutrition_data})
    else:
        return render(request, 'Nutrition/Nutrition_scrapedcontent.html')

"""




#_________________BELOW CODE REPRESENTS THE API ACCESS FUNCTIONALITY OF THE APPLICATION_______________________________
"""
API Name: nutritionix has a dB of ~600,000 real food items (e.g. BigMac, Cheetos, large apple, etc.)
and their corresponding nutritional information (e.g. calories, saturated fat, vitamin C, etc.)
API Guide: https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit#heading=h.73n49tgew66c
API Endpoint: we are focusing on the basic nutritional information endpoint, as opposed to the micronutrient data
"""


def nutritionix_nutrients_api(request):
    #user_query is a variable with the value of whatever the user entered into the search bar before pressing 'search'
    # we are saying if a user has entered a query
    if 'user_query' in request.GET:

        #below we use f strings to neatly compartmentalize the different aspects involved in accesing an API
        #thus we can easily modify the API version, the base URL, or the endpoint path as needed.
        api_version = 'v2'
        api_base_url = f'https://trackapi.nutritionix.com/{api_version}'
        endpoint_path = f'/natural/nutrients'
        endpoint = f'{api_base_url}{endpoint_path}'
        query = request.GET['user_query'] #this extracts the value for the user_query key and stores it in 'query'
        # requests.post (below) accepts 'headers' as an argument.
        # we provide api credentials, as specified in the API documentation, in 'headers'
        
        #NOTE: you will need to provide your own app-id and key in the below fields to be able to use this app feature
        headers = {
            'x-app-id': 'INSERT_APP_ID_HERE',
            'x-app-key': 'INSERT_API_KEY_HERE',
            # remote-user-id is used for billing purposes, but this isn't relevant so
            # api told us to use '0' as a value to disregard.
            'x-remote-user-id': '0'
        }


        # our 'query' value is stored as a dictionary in 'data', an argument that requests.post
        # can accept (requests.post can only accept certain arguments per its documentation)
        data = {
            "query": query,
        }

        user_query = {'user_query': query}
        # api stated this endpoint requires a POST request.
        # the 'endpoint' argument stores the precise URL endpoint--i.e. the entire and precise path we need to use
        # the 'headers' argument stores API credentials (keys)
        # the 'data' argument is what stores the actual query itself
        a_request = requests.post(endpoint, headers=headers, data=data)

        # prints a status code to verify our request was successful: we are looking for a code in the 200-299 range
        print(a_request.status_code)

        #the below code filters JSON response data to include only nutritional info
        #all nutritional info in JSON response starts with 'nf_', hence we targeted only KVPs with 'nf_'' in the key
        #error codes between 200 and 300 are failures, so we want to execute only if it succeeded

        if a_request.status_code in range(200, 299):
            data = a_request.json()
            results = data['foods']
            search_key = 'nf_'
            out = {}
            for i in results:
                if not isinstance(i, dict):
                    continue
                for k, v in i.items():

                    if search_key in k:
                        out[k] = v

            nutrients_dict = out
            del nutrients_dict['nf_p'] #nf_p is extraneous so we delete it
            print(nutrients_dict)#verifies dictionary integrity in console (we can see if it looks good)
            print(user_query)
            #take user to template and display results
            return render(request, 'Nutrition/Nutrition_API_results.html', {'nutrients_dict': nutrients_dict,
                          'user_query': user_query})
    return render(request, 'Nutrition/Nutrition_API.html')
"""
We are accessing nutritionix's API: a database of ~600,000 real food items (e.g. BigMac, Cheetos, large apple, etc.)
and their corresponding nutritional information (e.g. calories, saturated fat, protein, etc.)

!
"""

#below is a version of the above function, but it allows a user to send another query and SAVE it
def save_nutritionix_nutrients_api(request):
    #user_query is the name value of the input element where a user enters a query
    # we are saying if a user has entered a query
    if 'user_query' in request.GET:
        api_version = 'v2'
        api_base_url = f'https://trackapi.nutritionix.com/{api_version}'
        endpoint_path = f'/natural/nutrients'
        endpoint = f'{api_base_url}{endpoint_path}'
        query = request.GET['user_query']
        # requests.post accepts 'headers' as an argument.
        # we provide api credentials, as specified in the API documentation, in 'headers'
        #NOTE: you will need to provide your own app-id and key in the below fields to be able to use this app feature
        headers = {
            'x-app-id': 'INSERT_APP_ID_HERE',
            'x-app-key': 'INSERT_API_KEY_HERE',
            # remote-user-id is used for billing purposes, but this isn't relevant so
            # api told us to use '0' as a value to disregard.
            'x-remote-user-id': '0'
        }

        # our 'query' value is stored as a dictionary in 'data', an argument that requests.post
        # can accept (requests.post can only accept certain arguments per its documentation)
        data = {
            "query": query,
        }
        user_query = {'user_query': query}
        # api stated this endpoint requires a POST request.
        # the 'endpoint' argument stores the precise URL endpoint
        # the 'headers' argument stores API credentials (keys)
        # the 'data' argument is what stores the actual query itself
        a_request = requests.post(endpoint, headers=headers, data=data)

        # prints a status code to verify our request was successful
        print(a_request.status_code)

        #the below function filters JSON response data to include only nutritional info
        #all nutritional info in JSON response starts with 'nf_', hence we targeted only KVPs with 'nf_'' in the key
        #error codes between 200 and 300 are failures, so we want to execute only if it succeeded

        if a_request.status_code in range(200, 299):
            data = a_request.json()
            results = data['foods']
            search_key = 'nf_'
            out = {}
            for i in results:
                if not isinstance(i, dict):
                    continue
                for k, v in i.items():

                    if search_key in k:
                        out[k] = v

            nutrients_dict = out
            del nutrients_dict['nf_p'] #nf_p is extraneous so we delete it
            print(nutrients_dict)#verifies dictionary integrity in console (we can see if it looks good)
            #experimental logic to attempt saving to dB

            #we turn the dictionary into a list of values (floats) to allow for dB entry without iteration
            nutrients_dict2 = nutrients_dict
            nutrients_dict2.update({'search_query': query})
            nutrient_list = list(nutrients_dict2.values())
            print(nutrient_list)


            #we reference our NutritionixInfoReceived model and put each list element into their respective field
            nutrition_data = NutritionixInfoReceived(
            calories=nutrient_list[0],
            total_Fat=nutrient_list[1],
            saturated_fat=nutrient_list[2],
            cholesterol=nutrient_list[3],
            sodium=nutrient_list[4],
            total_carbohydrate = nutrient_list[5],
            dietary_fiber = nutrient_list[6],
            sugars = nutrient_list[7],
            protein = nutrient_list[8],
            potassium = nutrient_list[9],
            search_query= nutrient_list[10]
            )
            nutrition_data.save()

            del nutrients_dict['search_query']
            #for some reason nutrients_dict carries over the search_query value as well and this displays in the rendered table
            #Not sure why, but this del allowed it to save with query in dB but be omitted in table rendering for API_results.html


        #end experimental logic



            #take user to template and display results
            return render(request, 'Nutrition/Nutrition_API_results.html', {'nutrients_dict': nutrients_dict, 'user_query': user_query})
    return render(request, 'Nutrition/Nutrition_saveAPI.html')
