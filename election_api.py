import json
from flask import Flask, request, jsonify

app = Flask(__name__)

voters_file = "voters_data.txt"
elections_file = "elections_data.txt"
voter_404_message = {"error": "voter not found"}
election_404_message = {"error": "election not found"}
candidate_404_message = {"error": "candidate not found"}
no_data_400_message = {"error": "no data provided"}


# Register A Voter
@app.route("/voters", methods=["POST"])
def register_voter():
    if not request.data:
        return jsonify(no_data_400_message), 400
    record = json.loads(request.data)
    with open(voters_file, "r") as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        for entry in records:
            if entry["id"] == record["id"]:
                return (
                    jsonify(
                        {
                            "error": {
                                "code": "VOTER_ALREADY_EXISTS",
                                "message": f"A voter with the id {record['id']} already exists.",
                            }
                        }
                    ),
                    409,
                )
        records.append(record)
    with open(voters_file, "w") as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)


# Update Voter Information
@app.route("/voters/<voter_id>", methods=["PUT"])
def update_voter(voter_id):
    if not request.data:
        return jsonify(no_data_400_message), 400
    record = json.loads(request.data)
    with open(voters_file, "r") as f:
        data = f.read()
    if not data:
        records = [record]
        with open(voters_file, "w") as f:
            f.write(json.dumps(records, indent=2))
        return jsonify(record), 201
    else:
        records = json.loads(data)
        for entry in records:
            if entry["id"] == voter_id:
                entry["name"] = record["name"]
                entry["email"] = record["email"]
                entry["year_group"] = record["year_group"]
                entry["major"] = record["major"]
                break
        # if after the loop, the voter_id is not found, then create a new voter
        else:
            records.append(record)
            with open(voters_file, "w") as f:
                f.write(json.dumps(records, indent=2))
                return jsonify(record), 201
        with open(voters_file, "w") as f:
            f.write(json.dumps(records, indent=2))
        return jsonify(record), 200


# Delete A Voter
@app.route("/voters/<voter_id>", methods=["DELETE"])
def delete_voter(voter_id):
    with open(voters_file, "r") as f:
        data = f.read()
    records = json.loads(data)
    for record in records:
        if record["id"] == voter_id:
            records.remove(record)
            with open(voters_file, "w") as f:
                f.write(json.dumps(records, indent=2))
            return jsonify(record)
    return jsonify(voter_404_message), 404


# Retrieve A Voter
@app.route("/voters", methods=["GET"])
def retrieve_voter():
    voter_id = request.args.get("voter_id")
    with open(voters_file, "r") as f:
        data = f.read()
    records = json.loads(data)
    for record in records:
        if record["id"] == voter_id:
            return jsonify(record)
    return jsonify(voter_404_message), 404


# Create An Election
@app.route("/elections", methods=["POST"])
def create_election():
    if not request.data:
        return jsonify(no_data_400_message), 400
    record = json.loads(request.data)
    with open(elections_file, "r") as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        for entry in records:
            if entry["election_id"] == record["election_id"]:
                return (
                    jsonify(
                        {
                            "error": {
                                "code": "ELECTION_ALREADY_EXISTS",
                                "message": f"An election with the id {record['election_id']} already exists.",
                            }
                        }
                    ),
                    409,
                )
        records.append(record)
    with open(elections_file, "w") as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)


# Retrieve An Election
@app.route("/elections", methods=["GET"])
def retrieve_election():
    election_id = request.args.get("election_id")
    with open(elections_file, "r") as f:
        data = f.read()
    records = json.loads(data)
    for record in records:
        if record["election_id"] == election_id:
            return jsonify(record)
    return jsonify(election_404_message), 404


# Delete An Election
@app.route("/elections/<election_id>", methods=["DELETE"])
def delete_election(election_id):
    with open(elections_file, "r") as f:
        data = f.read()
    records = json.loads(data)
    for record in records:
        if record["election_id"] == election_id:
            records.remove(record)
            with open(elections_file, "w") as f:
                f.write(json.dumps(records, indent=2))
            return jsonify(record)
    return jsonify(election_404_message), 404


# Cast A Vote
@app.route(
    "/elections/<election_id>/votes/candidates/<candidate_id>", methods=["PATCH"]
)
def cast_vote(election_id, candidate_id):
    with open(elections_file, "r") as f:
        data = f.read()
    records = json.loads(data)
    for record in records:
        if record["election_id"] == election_id:
            for candidate in record["candidates"]:
                if candidate["candidate_id"] == candidate_id:
                    candidate["num_votes"] += 1
                    with open(elections_file, "w") as f:
                        f.write(json.dumps(records, indent=2))
                    return jsonify(records)
            return jsonify(candidate_404_message), 404
    return jsonify(election_404_message), 404


app.run(debug=True)
