# _mood_

## About _mood_
_mood_ is a personal journal web application built using Javascript and Python. Javascript
is used for front-end interactivity while the Python Django framework is utilised for
back-end data storage. This project is submitted as my capstone project for CS50W
Web Programming with Python and Javascript. You can view a video [here](#) that provides
an overview of _mood_.

![Ui of Mood](images/Ui.png)

## Requirements
There are several requirements that you need to have before you can launch _mood_. Ensure that you have pip installed before proceeding to install the other Python frameworks and modules.

### Pip Installation
Pip is a python package mangement system that allows you to install Python packages on your computer.
Ensure that you have pip installed. Otherwise, you can visit [here](https://pip.pypa.io/en/stable/installation/) to download pip.

### Django Installation
Django is a Python framework that allows you to manage databases via Python code. You can download Django
by running the command `pip install Django` in your terminal.

### Pillow Installation
Pillow is a Python library for media processing. You can download Pillow by running the command
`pip install Pillow` in your terminal.

### Pyperclip Installation
Pyperclip is a Python module that supports copy and paste clipboard functions. You can download Pyperclip by running the command `pip install pyperclip` in your terminal.

### Dateutil Installation
Dateutil is a Python module that supports operations on date and time. You can download Dateutil by running the command `pip install python-dateutil` in your terminal.

### Chart.js Installation
Chart.js is a Javascript library to visualise data through beautiful charts. You can download
Chart.js by running the command `npm install chart.js` in your terminal.


## Quick Start
Ensure that you have installed all the necessary requirements before proceeding with the following steps.

1. Download the application by pressing the button `Code`, and then `Download Zip` on the GitHub interface.
2. A zipped folder called `mood-main.zip` will be downloaded. Unzip the folder to obtain a folder called `mood-main`. Within `mood-main`, you will see the following: `README.md` (file), `requirements.txt` (file), `mood` (folder) and `images` (folder). Take note of the path of the `mood` folder.
3. Open a terminal and change directory (via the `cd` command) to the `mood` folder mentioned in Step 2.
4. Run `python manage.py makemigrations`, followed by `python manage.py migrate`.
5. Finally, run `python manage.py runserver`. You will be prompted with a message that indicates `Starting development server at {URL}` where URL looks like an IP address.
6. Visit the URL mentioned in Step 5 through your browser.
7. Start using _mood_!






## Core Features

### Register
#### About
You need to register an account with _mood_ before you can start using it. To do so, you can use the `Register` feature which provides a nice interface for you to create an account.

![Register Feature](images/register.png)

#### Implementation
The registration page is shown when the user visits the url `/register`. The function `register(request)` in `views.py` handles the back-end. It differentiates between a POST and a GET
request. If the user visits `/register` via a GET request, the registration fields will
be shown to the user. Else if the user visits `/register` via a POST request, then _mood_
will process the details entered by the user. A new account will be created if the details
are valid, otherwise an error message is shown to the user.


### Login

#### About
You can log into _mood_ if you have an existing account. The `Login` feature allows you
to easily do so.

![Login Feature](images/login.png)

#### Implementation

The login page is shown when the user visits the url `/login`. The function `login_view(request)` in `views.py` handles the back-end. It differentiates between a POST and a GET
request. If the user visits `/login` via a GET request, the login fields will
be shown to the user. Else if the user visits `/login` via a POST request, then _mood_
will process the details entered by the user. The user will be logged in if the details
are valid, otherwise an error message is shown to the user.


### View All Entries

#### About
You can view all your journal entries once you have logged in. Apart from viewing all
your entries, you can filter the entries by date - view all entries posted today, view
all entries posted within the week, and view all entries posted within the month. Also,
pagination is implemented where you would see a maximum of 5 entries at any point in time.

![View All Entries Feature](images/view-all.png)

#### Implementation
The url for this feature is `home/<str:criteria>` where `criteria` can be either `all`, `today`, `week` or `month`. The value of `criteria` depends on what which filter the user chooses, as indicated by the green button shown in the above diagram. A user should only be able to view his posts, hence to display the list of posts, I filtered the posts by only accepting posts whose associated owner is the current user that is logged in.

To obtain entries filtered by date, I further processed the filtered entries by checking their date fields to ensure that it satisifies the respective date filters.



### Create an Entry
#### About
You can easily add a new journal entry into _mood_ via the `Create` feature. For each entry, you can
input the following information:
1. Title of Entry
2. Content of Entry
3. Emotion (select from Happy, Surprised, Sad or Angry)
4. Image (you can upload an image from your local drive)


![Create an Entry Feature](images/create.png)

#### Implementation
The url for this feature is `create`. If you visit it via a GET request, the form to create a new entry
will be presented. Once you click the `Create` button, assuming that you have filled up the fields, a
POST request is made to the url and using Django, a new `Entry` will be created with the information
that you have provided. After creating the new `Entry`, a HTTPResponseRedirect will be made, redirecting
you to view the post that you have created.


### View an Entry
#### About
You can view the contents of a specific entry by clicking on it in the `View All` page. You will be able
to view the information that you have input, as well as the date at which the entry is created. An interesting
thing to note that is that the background of the site changes depending on the emotion associated with the
post that you are currently viewing!

![View an Entry Feature](images/view.png)

#### Implementation
The url for this feature is `view/<int:entry_number>`. It is handled by the `view(request, entry_number)`
method in `views.py`. The method checks that you are the owner of the entry that has the id `entry_number`
before displaying the post since you are not allowed to view the posts of another user. Then, it uses
the id `entry_number` to retrieve the corresponding `Entry`. The `Entry` is then passed into the
HTML file `view.html` to render the correct information.


### Edit an Entry

#### About
You are able to edit an entry via the `Edit` button found in the page whenever you view an entry. This
allows you to easily make changes when required. Note that the fields (except the image upload) will be
prefilled with the existing information of the entry.

![Edit an Entry Feature](images/edit.png)

#### Implementation
When one presses the `Edit` button, I utilised Javascript to hide the contents of the post, and
display the edit form instead. If the user presses `Cancel`, I then did the reverse where I hid
the edit form and redisplay the contents of the post. Once the user presses `Confirm`, I would
submit the form via a POST request to the `update<int: entry_number>` url which will then update
the contents of the post. I wanted to update the content asynchronously by sending an API request,
but I was not able to figure out how to do so because of the image upload. Unlike normal text
fields, the image upload cannot be easily sent over in the form of a JSON string. Thus, in the end,
I resorted to URL redirecting instead.



### Copy an Entry
#### About
You can easily copy the text content of an journal entry to your clipboard by pressing the
`Copy` button found in the page whenever you view an entry. This allows you to easily export and
share the title and content of your entry.

#### Implementation

When one presses the `Copy` button, I will use Javascript to make an API call to the route
`copy<int: entry_number>`. This invokes the `copy(request, entry_number)` method in `views.py`,
which retrieves the corresponding entry and copy its information to the clipboard using
the Pyperclip module. I did consider using Javascript to copy the information since I can
access the entry in the HTML file, but without HTTPs, the browser prevents me from interacting
with the clipboard.

### Delete an Entry
#### About
You can delete a journal entry by pressing the `Delete` button found in the page whenever you
view an entry. Don't worry if you accidentally pressed the button, because there is an additional
confirmation message that you have to accept before the entry gets deleted.

#### Implementation
I used Javascript to create an alert using the `confirm` method. If the user confirms deletion, I
made an API call to the route `delete<int: entry_number>` which will then find the corresponding
entry and delete it. The API call is done via a POST request, so the user will not be able to use
a GET request to bypass the delete mechanism.


### Meditation
#### About
The `Meditation` feature offers a timer with a duration of 1 minute. Whenever you are feeling stressed, you
can use it to start the timer, and close your eyes while relaxing music plays in the background. Once the time
is up, the music stops. This feature also keeps track of the total number of meditations that you have
successfully completed.

![Meditate Feature](images/meditate.png)

#### Implementation
The timer is created using Javascript, providing a front-end interface that the user can use to start and stop
the timer when necessary. After a user successfully completes a 1-minute meditation, I would make an API call
to the url `meditate` to update the total number of the meditations that the user has completed using Django.
A JSONResponse containing the new number of meditations is returned, and I used it to asychronously update the
count that is displayed on the webpage.

As for the audio, I utilised Javascript to play the audio when the user presses the `Start` button, and stop
the audio when either the user presses the `Stop` button or when time is up.

### Profile
#### About
In the profile page, you can view a breakdown of the posts that you have made in _mood_, categorised by emotions.
Furthermore, a random inspirational quote is present to encourage you. If you wish to log out, you can also
do so via the `Logout` button present in this page.

![ProfileFeature](images/profile.png)

#### Implementation
I used Chart.js to allow me to present data in a visually-appealing pie chart. I first made an API call
to the route `emotions` to return me a JSON response which captures the number of entries for each
emotion associated with the user. The values in the JSON response is then fed into the pie chart.

To display the random inspirational quote, I made an API call to an
[external API](https://type.fit/api/quotes) that hosts data regarding quotes and their authors.
Once the data arrives, I randomly pick a quote to display on screen by updating the inner HTML of the
display elements.

For the logout feature, once the user presses the logout button, he will be sent to the url
`logout` which runs the `logout_view(request)` method in `views.py`. This method would log the user out,
then redirect the user back to the `index` route which displays the start screen of _mood_.

### Responsive User Interface
_mood_ provides a responsive user interface, where the content would adapt to the size of the browser window. This is implemented primarily via CSS-Flex and media queries.



## File Breakdown
Most of my code resides in the `journal` folder. The following briefly explains what is contained within each file.

1. `urls.py`

This file contains the urls for the _mood_ application, which specifies which function in `views.py` will be called when the user visits the different urls.


2. `views.py`

This file contains the views for the _mood_ application, which are functions that will run
when a specific URL is visited. For example, it contains the function `copy(request, entry_number)` which has the functionality of copying an entry to the clipboard when the
URL for the copy feature is visited.


3. `models.py`

This file contains the code for the models used in the _mood_ application. In _mood_, there
are 2 models used. The models are `User` which represents a user of _mood_ and `Entry` which
represents a journal entry stored in _mood_.

4. `templates/journal`

This folder contains the HTML pages used in _mood_. I incorporated my Javascript code into
the HTML code, hence this folder is also responsible for the front-end functionality of _mood_.

| File        | Description |
| ----------- | ----------- |
| create.html    | HTML code for the webpage displaying the form responsible for creating a journal entry      |
| home.html    | HTML and Javascript code for the webpage displaying the list of journal entries     |
| index.html    | HTML code for the webpage displaying the start screen of _mood_     |
| login.html    | HTML code for the webpage displaying the form responsible for login     |
| meditate.html    | HTML and Javascript code for the webpage responsible for the `Meditate` feature      |
| profile.html    | HTML and Javascript code for the webpage displaying the user's profile      |
| register.html    | HTML code for the webpage displaying the form responsible for registration     |
| view.html    | HTML and Javascript code for the webpage displaying a specific journal entry      |




5. `static/journal`

This folder contains two main types of resources. The first are the media assets used in
_mood_, such as the emoticon images and the audio track file used for the Meditation feature. The second are the CSS files used to style the webpages in _mood_.

| File        | Description |
| ----------- | ----------- |
| angry.png     | Emoticon image for "Angry" emotion       |
| happy.png  | Emoticon image for "Happy" emotion      |
| mood_logo.png     | Logo image for _mood_       |
| sad.png  | Emoticon image for "Sad" emotion      |
| surprised.png  | Emoticon image for "Surprised" emotion      |
| create.css     | CSS code for the `create.html`       |
| home.css     | CSS code for the `home.html`       |
| index.css     | CSS code for the `index.html`       |
| login.css     | CSS code for the `login.html`       |
| meditate.css     | CSS code for the `meditate.html`       |
| profile.css     | CSS code for the `profile.html`       |
| register.css     | CSS code for the `register.html`       |
| view.css     | CSS code for the `view.html`       |
| meditation_soundtrack.mp3     | Audio soundtrack for the `Meditation` feature       |




## Distinctiveness and Complexity
_mood_ is a web application that is distinct and more complex from the homework projects in CS50W.

### Distinctiveness
The concept of _mood_ revolves around a personal journal application, which is an idea that was not explored in all the previous projects. While it uses Django like the other projects, instead of allowing interactions
between users, _mood_ focuses on isolating each user's data from others as journal entries are meant to be personal.

It offers features that are unique to the concept of a journal, such as the `Meditation` feature. The `Meditation` feature is a new feature I implemented, that is not seen in any of the previous projects. This feature ties in well with the concept of a journal, because the main purpose is to allow users of _mood_ to pen down their thoughts and relax whenever they feel stressed. Another example is the `Copy` feature which is not seen in previous projects. It provides a way for one to easily export data stored in the application by copying an entry to the clipboard, without having to go into the database and manually retrieve the information.

Keeping track of journal entries may seem similar to posts in Network and emails in Mail, but I feel that some similiarites are inevitable because web applications would need to keep track of information in some way or another. Hence, to set my journal entries apart, I allowed users to associate an emotion with the entry and upload an image. Emotions and images are unique to the concept of a journal entry which cannot be found in the Network and Mail projects. Furthermore, the selection of emotions is implemented as a radio button, which is not seen in previous projects as well.

_mood_ offers a profile page but the profile page's features and functionality are distinctly different from that of Network. In Network, one can view his/her posts and the number of followers/following. I did my best to be different by choosing a different mode of visualisation when I choose to explore a pie chart to analyse information instead of simply displaying information retrieved from models. Also, there is a random element involved in _mood_ where the quote displayed is different everytime one visits the page.

### Complexity
_mood_ is more complex because while it builds on the learning points from the previous projects, it has features that are created using knowledge not covered in CS50W. CS50W provided me with the foundations to independently explore more of Django and Javascript, but I had to learn how to incorporate the new knowledge with what I have learnt in CS50W.

1. Timer from the `Meditation` feature

In my opinion, many of the previous projects such as `commerce` and `mail` revolved heavily around the
usage of Django. I wanted to explore more of Javascript in this project, hence I thought of the idea of
building a timer just via Javascript. I took reference from online resources such as [W3Schools](https://www.w3schools.com/howto/howto_js_countdown.asp), but modified the functionality and design to suit my application. Furthermore, I tied it with Django where I would asynchronously update the meditation count after the timer is up, but would not update the meditation count if the user stops the timer in advance. To add audio to my timer, I explored the usage of `<audio>` elements in HTML and programmatically interacted with it through Javascript.

2. Piechart from the `Profile` feature

I tried out a new Javascript framework, ChartJS, that was previously foreign to me. The previous projects did not utilise Javascript frameworks, so I had a bit of difficulty trying to get ChartJS to work for me. In my opinion, the terminologies used in the documentation were more complex than what I am accustomed to where usually, W3Schools have simple instructions that I can follow. I had to incorporate API calls with my pie chart because I needed to get information from the models to determine the breakdown (by emotions) of the user's journal entries. To further customise the pie chart, I also had to learn about the `Configurations` and
`Chart Types` aspects of ChartJS. While it was something new, I enjoyed exploring the framework and would use it for future data visualisation features.

3. `Copy` Feature

I explored a new module, Pyperclip, to learn how to copy text to clipboard. I incorporated this functionality with my Javascript code to allow users to send API request such that `views.py` can handle the request and copy the details of an `Entry` stored in the back-end to the user's clipboard.

4. External API call for the `Inspirational Quote` feature

In the `Profile` page, the inspirational quote is generated by making an external API call. The previous projects revolved around internal API calls, and making external API calls was only covered in the lecture. I wanted to try out an external API call because in reality, many web applications rely on API provided by others. Thus, I utilised what I have learnt to find a suitable API that hosts inspirational quotes, and further processed the response that I got to display a random quote out of the many quotes that were received from the API call.

5. Uploading and processing of images

In the projects, we have not explored the feature of uploading an image and storing it in a model. However, I felt that the ability for a user to add an image to a journal entry is important because _mood_ is designed to be something personal, and users might want to keep track of images in journal entries. However, it turns out that uploading and processing of images is not as simple as text fields or integer fields. I had to download the Pillow library and specify how form data is encoded when sent over my server. Furthermore, I have to specify a local location in which the images uploaded would be stored so that they can be displayed when the user views the entries. Thus, the feature of image upload made form processing more complicated and additional Python code is required to parse the image into a string location that can be stored in my Django model. The string location would then allow me to retrieve the correct image thereafter.

6. Responsive Design

In my opinion, responsive design added to the complexity of the project. In the previous CS50W projects, we focused solely on functionality where we did not have to handle responsiveness. However, I had to make _mood_ responsive and to do so, I explored the usage of CSS Flex and media queries. This added to the complexity of the HTML and CSS code as I had to ensure that HTML elements are grouped correctly such that I can apply CSS flex to either align items horizontally or vertically, depending on the flex-direction. Also, I have to take into account the different breakpoints and screen resolution such that my elements can scale responsively. In some parts, I had to use media queries to resize elements in smaller screens. This is definitely more complex as compared to previous projects because previous projects did not consider screen size and design outcomes.


## Acknowledgements
_mood_ is only made possible with the help of the following people and resources:
1. Teaching resources from [CS50W Web Programming with Python and Javascript](https://cs50.harvard.edu/web/2020/).
2. Padsound Meditation Audio by [Samuel Francis Johnson](https://pixabay.com/users/samuelfrancisjohnson-1207793/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=21384) from [Pixabay](https://pixabay.com/sound-effects//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=21384).
3. Inspirational Quotes API by [SergeyWebPro](https://type.fit/api/quotes)
