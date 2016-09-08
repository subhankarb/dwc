# Data-Wrangling-Challenges
There are Two parts of this challange:
* Extract The data from http://www.eia.gov/dnav/ng/hist/rngwhhdm.htm and scrap the page 
  and put the data in csv files.
* Expose the data as a chart.

For the first part 3 types of csv files has been generated.
- Gas price each day.
- Average gas price each month.
- Average gas price each year.

For the second part using flask a API end point has be opened so that we can see some chart 
of the csv data. Used highchart to generate the chart and flask to parse the csv and send json to
front end.
The chart can be seen http://ec2-54-69-180-51.us-west-2.compute.amazonaws.com:5000/
