from openai import OpenAI

from app.config.config import get_settings


class ApplicationSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=get_settings().open_api_key)
        self.model = "gpt-4.1-mini"

    def summarize(self, content: str, resume_data: str, cover_data: str = "", max_tokens=300):
        system_role = {
            "role": "system",
            "content": """
                You are a job-application summarization agent.

                Your task is to generate a SHORT, FACT-ONLY, RECALL-OPTIMIZED summary
                from structured job application content and resume-related data.
                
                STRICT RULES:
                - DO NOT add, assume, infer, or invent any information
                - USE ONLY the provided content
                - NO introductions, NO conclusions, NO explanations
                - NO full paragraphs
                - NO complete sentences unless unavoidable
                - USE keywords, phrases, and bullet points only
                - Be concise and scannable within 5–10 seconds
                - Focus strongly on optional details, questionnaires, and custom answers
                - Output must be deterministic and structured
                - On highlighting the strength get the details from resume details also
                
                Goal:
                This summary must help the candidate instantly remember:
                - Which company and role this is
                - What the job expects
                - What special or optional details were involved
                - What strengths or matches the candidate can highlight in a phone call
            """
        }
        user_role = {
            "role": "user",
            "content": f"""
                Summarize the following job application content for rapid recall.

                CONTENT:
                {content}
                
                RESUME (ONLY USE IN STRENGTHS/MATCHES CANDIDATE CAN HIGHLIGHT):
                {resume_data}
                
                COVER LETTER DATA (IF EXIST, EXTRACT SOME POINTS ALSO):
                {cover_data}
                
                OUTPUT FORMAT (STRICT):
                
                Company:
                - Name:
                - Location:
                
                Role:
                - Job Title:
                - Job ID:
                - Applied Date:
                
                Job Keywords (from job description only):
                - Point 1
                - Point 2
                - Point 3
                - Point 4
                - Point 5
                
                Special / Optional Details:
                - Questionnaires:
                - Custom answers:
                - Extra requirements:
                - Anything non-standard or notable:
                
                Candidate Match Highlights (ONLY if explicitly present in data):
                - Skills mentioned:
                - Experience alignment:
                - Tools / technologies:
                - Domain relevance:
                
                Rules Reminder:
                - Facts only
                - Keywords only
                - No added insights
                - No assumptions
                - No explanations

            """

        }
        return self.client.responses.create(
            model=self.model,
            input=[system_role, user_role],
            max_output_tokens=max_tokens
        ).output_text
