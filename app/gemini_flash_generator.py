"""
gemini_flash_generator.py
--------------------------
Generates a short nutrition or recovery tip using Gemini Flash.
"""

import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

_model = None


def _get_model():
    global _model

    if _model is None:
        _model = genai.GenerativeModel("gemini-3.8-flash")

    return _model


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a concise, actionable nutrition or recovery tip
    based on the user's fitness goal.
    """

    prompt = f"""
Give one short, practical nutrition or recovery tip (2-4 sentences)
for someone whose fitness goal is "{goal}".

Be specific and actionable.
Mention suitable food sources, timing, hydration, or recovery where relevant.

Do not add headings or bullet points.
Return only a short paragraph.
"""

    try:
        response = _get_model().generate_content(prompt)
        return response.text.strip()

    except Exception as exc:
        error_message = str(exc)

        # Handle Gemini quota/rate-limit errors
        if "429" in error_message or "quota" in error_message.lower():
            return (
                f"For your {goal} goal, include protein-rich foods such as "
                "eggs, milk, curd, paneer, dal, or chicken in your meals. "
                "Drink enough water and get adequate sleep to support "
                "muscle recovery and overall fitness."
            )

        # Handle other Gemini/API errors
        return (
            "Nutrition tip is temporarily unavailable. "
            "Please try again later."
        )