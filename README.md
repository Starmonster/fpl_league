# fpl_league
An app to analyse team performance in local FPL leagues

#### Required Files
1 Procfile
2 setup.sh
3 requirements.txt
4 code scripts
5 resources

## Blog
#### Pre commit work
Notebooks constructed to call in relevant data from fpl endpoints. \
Data wrangled and functions built to access current standings, league details, player histories etc \
Experiments with various plotting libraries. We settled on Plotly express for MVP. 

#### Blog 5th Jan 2022
1. Initial git commit made. Points and ranking plots display with few bugs. \
2. Inputs include league id, type of points, compare close rivals, username\
3. MVP app deployed through streamlit and Heroku
4. external link - https://fpl-league-app.herokuapp.com/


#### Bugs 5th Jan 2022
1. Rivals comparison does not work if user is top of table (notebook ready - move to live env)
2. Drop down options not user friendly for weekly / overall request
3. When comparing rivals the rank plot displays local rank not true league rank (noteboom ready - move to live env)

#### Next Steps 5th Jan 2022
1. Debug 
2. Alignment of title and text with plots
3. Introduction text below title
4. Build user guide
5. Display detailed user stats below plots
6. Improve visability of plots including axis labels, ticks, and make titles specific to search request. (notebook ready - move to live env)

#### Blog 6th Jan
1. In draft notebook - altered ranking function call to ensure focussed plots return real world rankings
2. Improved plot text and labels for clarity - increase font sizes of ticks, labels and titles
3. Amended rivals comparison so that league leader compares with two closest, chasing rivals only

#### Blog 7th Jan

#### Bugs 7th Jan
1. On opening a new window the app defaults to an error as there is no league id entered


#### Next Steps 7th Jan
Debug
