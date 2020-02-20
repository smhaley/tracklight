# tracklight

A simple tool for scanning webpage HTML and JS calls for 500 of the top webpage tracking services.

Core tracking list, tracker_set.json, was compiled by scraping tracker name and "operates under" data from the top 500 listings on https://whotracks.me/trackers.html.

To obtain javascript calls, this project relies on Selenium. Due to resource intensity of using an actual virtual browser, this project is best suited for local deployment.

Currently it is hosted at, 56.6.137.60 on a micro tier EC2 instance. The server cannot handle too many hits without running out of resources. 

