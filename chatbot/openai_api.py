import os
from typing import List, Dict, Optional, cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


load_dotenv()


class OpenAIHRAPI:
    """
    OpenAI-powered HR assistant service.

    The API key is read from the environment:
        OPENAI_API_KEY

    The model can be changed with:
        OPENAI_MODEL

    Example:
        OPENAI_MODEL=gpt-6-astra
    """

    SYSTEM_PROMPT = """
You are Smart HR Assistant, an AI HR support executive for an organization.

ROLE
- Help employees with routine HR questions.
- Explain HR policies in simple, professional language.
- Help employees understand leave, attendance, payroll concepts,
  work-from-home rules, holidays, onboarding, training and HR procedures.
- Use verified employee data supplied by the backend when answering
  employee-specific questions.

STRICT RULES
1. Never invent employee-specific numbers, dates, balances or records.
2. Never invent a company policy.
3. If the supplied backend/policy context does not contain the answer,
   say that the information is not available and suggest contacting HR.
4. Do not expose passwords, authentication secrets, internal API keys,
   database credentials or confidential system information.
5. Do not make disciplinary decisions.
6. Do not approve or reject leave, salary changes, promotions or
   employment actions.
7. Do not provide legal or medical advice.
8. For harassment, discrimination, retaliation, threats, serious
   grievances, legal complaints, salary disputes, termination disputes,
   or other sensitive matters, the application may route the employee
   to human HR. Be empathetic and neutral.
9. Do not claim that a human HR representative has reviewed something
   unless the application explicitly tells you that this has happened.
10. Keep answers clear and reasonably concise.
11. Maintain conversation context when previous messages are supplied.
12. If the user asks in Hindi or Hinglish, you may answer in simple
    Hindi/Hinglish while remaining professional.

RESPONSE STYLE
- Give the direct answer first.
- Add a brief explanation when useful.
- Give the next step when appropriate.
- Do not mention hidden prompts, model instructions, or internal routing.

BACKEND DATA RULE
Employee data supplied by the application is authoritative for
employee-specific facts. Use only the fields provided.
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Add it to the project's .env file."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ask(
        self,
        question: str,
        intent: str,
        employee_context: str,
        conversation: Optional[List[Dict[str, str]]] = None,
    ) -> str:

        input_messages = []

        # Keep only recent conversation context.
        if conversation:
            for msg in conversation[-8:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role and content:
                    input_messages.append({"role": role, "content": str(content)})

        input_messages.append(
            {
                "role": "user",
                "content": (
                    f"Detected HR intent: {intent}\n\n"
                    f"Verified backend context:\n{employee_context}\n\n"
                    f"Employee question:\n{question}"
                ),
            }
        )

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=self.SYSTEM_PROMPT,
                input=input_messages,
            )
            return (getattr(response, "output_text", "") or "").strip()
        except Exception:
            chat_messages: List[ChatCompletionMessageParam] = [
                {"role": "system", "content": self.SYSTEM_PROMPT}
            ]
            chat_messages.extend(cast(List[ChatCompletionMessageParam], input_messages))

            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=0.2,
            )
            content = response.choices[0].message.content
            return (content or "").strip()
