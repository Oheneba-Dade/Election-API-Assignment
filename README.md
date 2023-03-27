# Election-API-Assignment
This contains the code for an assignment to design a REST API for an electronic voting system.

This API enables the following:
- Registering a student as a voter.
It will be necessary for new students to be registered to vote.
- De-registering a student as a voter.
A student may need to be de-registered once they leave campus.
- Updating a registered voter’s information.
a. A student’s year group, major or other information might change.
- Retrieving a registered voter.
- Creating an election.
- Retrieving an election (with its details).
- Deleting an election.
- Voting in an election.

# Stack
- Flask/Python

# Extra Information
- The data is stored in two text files (`voters_data.txt` and `elections_data.txt`) and the main code to be run to start the server is `election_api.py`
- I used POSTMAN to test the requests and responses from the API
- Because this is just for an assignment to be submitted within limited time, the API may not be as fullproof and comprehensive as it should be. I will try to advance it when I get the chance :)
