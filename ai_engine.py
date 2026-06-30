import google.generativeai as genai
from config import GEMINI_API_KEY


class InterviewEngine:

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")


    # --------------------------------------------------
    # Generate First Question
    # --------------------------------------------------

    def generate_first_question(self, role, company, difficulty):

        prompt = f"""
You are a Senior Technical Interviewer.

Conduct a realistic technical interview.

Candidate Role:
{role}

Target Company:
{company if company else "General Technical Interview"}

Difficulty:
{difficulty}

Rules:

1. Ask EXACTLY ONE interview question.
2. Ask only one question.
3. Do not explain anything.
4. Do not give hints.
5. Do not give the answer.
6. Return ONLY the interview question.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error generating question: {e}"


    # --------------------------------------------------
    # Generate Next Question
    # --------------------------------------------------

    def generate_next_question(
        self,
        role,
        company,
        difficulty,
        history
    ):

        conversation = ""

        for item in history:

            conversation += f"""

Question:
{item['question']}

Candidate Answer:
{item['answer']}

"""

        prompt = f"""
You are a Senior Technical Interviewer.

Candidate Role:
{role}

Company:
{company if company else "General Technical Interview"}

Difficulty:
{difficulty}

The interview so far is:

{conversation}

Instructions:

1. Read every previous answer.
2. Evaluate the answers internally.
3. Ask the NEXT logical interview question.
4. Make the interview realistic.
5. Do NOT repeat previous questions.
6. Do NOT provide explanations.
7. Return ONLY the next interview question.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error generating next question: {e}"


    # --------------------------------------------------
    # Generate Final Report
    # --------------------------------------------------

    def generate_report(
        self,
        role,
        company,
        difficulty,
        history
    ):

        conversation = ""

        for item in history:

            conversation += f"""

Question:
{item['question']}

Candidate Answer:
{item['answer']}

"""

        prompt = f"""
You are a Senior Technical Interviewer.

Candidate Role:
{role}

Company:
{company if company else "General Technical Interview"}

Difficulty:
{difficulty}

Complete Interview:

{conversation}

Evaluate the candidate based on the complete interview.

Return the response ONLY as valid HTML.

Do NOT use Markdown.

Use this exact HTML structure:

<h2>Overall Score</h2>
<p>Give a score out of 10 with a short explanation.</p>

<h2>Technical Knowledge</h2>
<p>Evaluate the candidate's technical understanding.</p>

<h2>Communication Skills</h2>
<p>Evaluate communication and clarity.</p>

<h2>Problem Solving Ability</h2>
<p>Evaluate problem-solving skills.</p>

<h2>Strengths</h2>
<ul>
<li>Strength 1</li>
<li>Strength 2</li>
<li>Strength 3</li>
</ul>

<h2>Weaknesses</h2>
<ul>
<li>Weakness 1</li>
<li>Weakness 2</li>
<li>Weakness 3</li>
</ul>

<h2>Areas for Improvement</h2>
<ul>
<li>Improvement 1</li>
<li>Improvement 2</li>
<li>Improvement 3</li>
</ul>

<h2>Final Recommendation</h2>
<p>Give a professional recommendation.</p>

Return ONLY HTML.

Do not wrap the HTML inside markdown code blocks.

Do not wrap the response in Markdown code fences.

Do not add any extra text before or after the HTML.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"<h2>Error</h2><p>{e}</p>"