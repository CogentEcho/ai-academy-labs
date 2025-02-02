import anthropic
import sqlite3

class OversightAgent:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key)
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect("oversight_agent.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                step TEXT,
                approved BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def get_approval(self, step):
        prompt = f"""
        You are an oversight agent responsible for reviewing and approving steps in the AI Academy Labs project.
        Please review the following step:

        {step}

        Respond with "Approved" if the step is safe, ethical, and aligned with the project's goals. Respond with "Rejected" if the step should not be executed.
        """

        response = self.client.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=100,
        )

        approval = response.completion.strip().lower()
        self.record_approval(step, approval == "approved")
        return approval == "approved"

    def record_approval(self, step, approved):
        conn = sqlite3.connect("oversight_agent.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO approvals (step, approved) VALUES (?, ?)", (step, approved))
        conn.commit()
        conn.close()
