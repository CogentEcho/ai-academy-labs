import os
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)
api_key = os.environ["ANTHROPIC_API_KEY"]
client = anthropic.Client(api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-agent", methods=["POST"])
def generate_agent():
    agent_type = request.form["agent_type"]
    requirements = request.form["requirements"]

    prompt = f"""
    You are an AI agent generator responsible for creating highly specialized agents for the AI Academy Labs project.
    Please generate a Python script for an agent with the following requirements:

    Agent Type: {agent_type}
    Requirements: {requirements}

    Ensure that the generated agent follows best practices, is modular, and is capable of collaborating with other agents in the project.
    """

    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",
        max_tokens_to_sample=2000,
    )

    agent_script = response.completion.strip()
    return jsonify({"agent_script": agent_script})

@app.route("/analyze-resources", methods=["POST"])
def analyze_resources():
    resource_type = request.form["resource_type"]

    prompt = f"""
    You are an AI resource analyzer responsible for evaluating potential resources for the AI Academy Labs project.
    Please generate a detailed report analyzing the following resource type:

    Resource Type: {resource_type}

    Include the following information in your report:
    - Pros and cons of using the resource
    - Expenses and cost considerations
    - Available options and alternatives
    - Any additional questions or considerations relevant to the resource

    Provide a comprehensive analysis to help inform decision-making for the project.
    """

    response = client.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",
        max_tokens_to_sample=2000,
    )

    resource_report = response.completion.strip()
    return jsonify({"resource_report": resource_report})

if __name__ == "__main__":
    app.run(debug=True)