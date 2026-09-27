

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


def generate_workout_gemini(goal: str, intensity: str, age: int, weight: str) -> str:
    """
    Generate a personalized 7-day workout plan.

    Returns a plain-text/markdown-ish structured plan with a warm-up,
    main workout, and cooldown for each day, tailored to the user's goal
    (e.g. muscle gain, weight loss) and intensity (low/medium/high).
    """
    prompt = f"""
You are a certified personal trainer. Create a structured 7-day workout plan.

User profile:
- Age: {age}
- Weight: {weight} kg
- Fitness goal: {goal}
- Workout intensity: {intensity}

For each of the 7 days, include:
- A short label for the day's focus (e.g. Full Body, Upper Body, Cardio, Core, Rest/Recovery)
- Warm-up (5-10 minutes)
- Main workout: a list of exercises with sets, reps (or duration), and rest intervals
- Cooldown or recovery tip

Format clearly with headings per day (Day 1, Day 2, ...). Keep it practical and
safe for the stated intensity level.
"""
    try:
        response = _get_model().generate_content(prompt)
        return response.text.strip()
    except Exception as exc:  # pragma: no cover - network/SDK errors
        return (
            "We couldn't reach the AI service to generate your plan "
            f"right now ({exc}). Please check your GOOGLE_API_KEY and try again."
        )


def update_workout_plan(original_plan: str, feedback: str) -> str:
    """
    Revise an existing 7-day workout plan based on user feedback,
    e.g. "Add yoga", "Include more cardio", "Too intense".
    """
    prompt = f"""
You are a certified personal trainer. A user has an existing 7-day workout plan
and has given feedback. Revise the plan to incorporate their feedback while
keeping the same overall structure (7 days, warm-up/main workout/cooldown).

Original plan:
{original_plan}

User feedback:
{feedback}

Return the full revised 7-day plan, clearly labeled Day 1 through Day 7.
"""
    try:
        response = _get_model().generate_content(prompt)
        return response.text.strip()
    except Exception as exc:  # pragma: no cover
        return (
            "We couldn't reach the AI service to update your plan "
            f"right now ({exc}). Please check your GOOGLE_API_KEY and try again."
        )
