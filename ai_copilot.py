import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def analyze_security_alert(
    ip,
    attack_type,
    severity,
    attempts,
    usernames,
    time_span,
    reasons
):
    evidence = "\n".join(
        f"- {reason}"
        for reason in reasons
    )

    prompt = f"""
You are an AI assistant helping a SOC analyst investigate
an authentication security alert.

Analyze only the evidence provided below.

Source IP: {ip}
Attack Type: {attack_type}
Severity: {severity}
Failed Attempts: {attempts}
Targeted Accounts: {", ".join(usernames)}
Time Span: {time_span:.0f} seconds

Detection Evidence:
{evidence}

Return a concise assessment using exactly this format:

Summary:
Write one short paragraph explaining what appears to be happening.

Risk:
Write one short paragraph explaining why this activity matters.

Recommended Actions:
Provide 3 to 5 numbered practical investigation or remediation steps.

Formatting rules:
- Use plain text only.
- Do not use Markdown.
- Do not use asterisks.
- Do not use bold formatting.
- Keep the response concise and professional.

Do not claim the source IP is definitely malicious.
Do not invent evidence that was not provided.
"""

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return response.output_text