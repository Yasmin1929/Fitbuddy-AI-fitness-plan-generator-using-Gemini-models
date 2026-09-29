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


def generate_workout_gemini(
    goal: str,
    intensity: str,
    age: int,
    weight: str
) -> str:

    prompt = f"""
You are a certified personal trainer. Create a structured 7-day workout plan.

User profile:
- Age: {age}
- Weight: {weight} kg
- Fitness goal: {goal}
- Workout intensity: {intensity}

For each of the 7 days, include:
- A short label for the day's focus
- Warm-up (5-10 minutes)
- Main workout with exercises, sets, reps/duration and rest
- Cooldown or recovery tip

Format clearly with headings per day (Day 1, Day 2, ...).
Keep it practical and safe for the stated intensity level.
"""

    try:
        response = _get_model().generate_content(prompt)
        return response.text.strip()

    except Exception as exc:
        error_message = str(exc).lower()

        # Gemini quota/rate-limit fallback
        if "429" in error_message or "quota" in error_message:

            return f"""
Day 1 – Full Body

Warm-up: 5–10 minutes of light walking and stretching.

Main Workout:
• Squats – 2 sets × 10 reps
• Wall Push-ups – 2 sets × 10 reps
• Glute Bridges – 2 sets × 12 reps
• Rest – 60 seconds between sets

Cooldown: 5 minutes of gentle stretching.


Day 2 – Upper Body

Warm-up: 5–10 minutes.

Main Workout:
• Wall Push-ups – 2 sets × 10 reps
• Shoulder Raises – 2 sets × 10 reps
• Arm Circles – 2 sets × 15 reps
• Rest – 60 seconds between sets

Cooldown: 5 minutes of stretching.


Day 3 – Lower Body

Warm-up: 5–10 minutes.

Main Workout:
• Bodyweight Squats – 2 sets × 10 reps
• Reverse Lunges – 2 sets × 8 reps each leg
• Calf Raises – 2 sets × 12 reps
• Rest – 60 seconds between sets

Cooldown: 5 minutes of stretching.


Day 4 – Rest & Recovery

Take a rest day.
Do light walking and gentle stretching.
Stay hydrated and get adequate sleep.


Day 5 – Full Body

Warm-up: 5–10 minutes.

Main Workout:
• Squats – 2 sets × 10 reps
• Wall Push-ups – 2 sets × 10 reps
• Glute Bridges – 2 sets × 12 reps
• Bird Dog – 2 sets × 10 reps

Cooldown: 5 minutes of stretching.


Day 6 – Core

Warm-up: 5 minutes.

Main Workout:
• Plank – 2 sets × 20 seconds
• Bird Dog – 2 sets × 10 reps
• Dead Bug – 2 sets × 10 reps
• Rest – 60 seconds between sets

Cooldown: 5 minutes of gentle stretching.


Day 7 – Recovery

Light walking for 15–20 minutes.
Do gentle full-body stretching.
Focus on hydration, nutrition and recovery.
"""

        # Other errors
        return (
            "Workout plan is temporarily unavailable. "
            "Please try again later."
        )


def update_workout_plan(original_plan: str, feedback: str) -> str:

    prompt = f"""
You are a certified personal trainer. A user has an existing 7-day workout plan
and has given feedback. Revise the plan to incorporate their feedback while
keeping the same overall structure.

Original plan:
{original_plan}

User feedback:
{feedback}

Return the full revised 7-day plan, clearly labeled Day 1 through Day 7.
"""

    try:
        response = _get_model().generate_content(prompt)
        return response.text.strip()

    except Exception as exc:

        error_message = str(exc).lower()

        if "429" in error_message or "quota" in error_message:
            return (
                "The AI service is temporarily unavailable because the "
                "Gemini API quota has been reached. Please try again later."
            )

        return (
            "Workout plan update is temporarily unavailable. "
            "Please try again later."
        )

