# BuHub

**Project Name**: BU Hub Calculator

_Input your major and AP credits to receive a selection of classes which will fulfill remaining hub credits_

**Built With**: Python, HTML/CSS(Bootstrap), javascript, jQuery, Django, Requests/BeautifulSoup4, 

**Team Members**: Jing Lin, Alice Wang, Eric Chao, Erin Chung

**Inspiration**: For the current freshman class, BU implemented a new system for their general
education requirements which is called "The Hub". It revolves around taking courses within 6
"Essential Capacities" organized by this chart: [link](http://https://www.bu.edu/sargent/files/2018/06/BUHub-2.jpg).
Many of the current freshman class find the requirements for The Hub unintuitive and have trouble deciding
which classes to take in order to efficiently fulfill all the requirements. Our project aims to help these
students and after they input their major and which AP credits they received, provide them with a personalized list
of classes which they may take throughout their time at BU which will ensure that the Hub is fulfilled.

**What We Did**: 1) We scraped various BU pages to fetch class data for all the courses that fulfill Hub requirements.
2) We then wrote an algorithm to generate a greedy strategy to search for classes. 3) Then we built the UI for the app. 