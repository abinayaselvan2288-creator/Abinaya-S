import json

from typing import Optional

from PIL import Image

from google import genai

from google.genai import types

from app.config import settings

from app.services.catalog import enrich


class GeminiService:

    def __init__(self):

        if settings.gemini_api_key:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        else:

            self.client = None


    # =====================================================
    # FALLBACK ENGINE
    # =====================================================

    def _fallback(
        self,
        domain,
        data
    ):

        budget = float(
            data["budget"]
        )


        # -------------------------------------------------
        # HOME
        # -------------------------------------------------

        if domain == "home":

            categories = [

                (
                    "LED ceiling light",
                    budget * 0.08
                ),

                (
                    "Ceiling fan",
                    budget * 0.12
                ),

                (
                    "Dining table",
                    budget * 0.25
                ),

                (
                    "Curtains",
                    budget * 0.08
                ),

                (
                    "Wall decor",
                    budget * 0.07
                ),

                (
                    "Storage cabinet",
                    budget * 0.20
                )
            ]


            return {

                "title":
                    "Budget-friendly home plan",

                "summary":
                    "A practical starter plan using the supplied budget.",

                "budget":
                    budget,

                "allocation": [

                    {
                        "category": category,
                        "amount": round(
                            amount,
                            2
                        )
                    }

                    for category, amount
                    in categories
                ],

                "recommendations": [

                    {

                        "name": category,

                        "estimated_price":
                            round(amount, 2),

                        "reason":
                            "Fits the planned allocation.",

                        "search_query":
                            category
                    }

                    for category, amount
                    in categories
                ]
            }


        # -------------------------------------------------
        # PARTY
        # -------------------------------------------------

        if domain == "party":

            allocations = [

                (
                    "Food & catering",
                    0.45
                ),

                (
                    "Venue",
                    0.20
                ),

                (
                    "Decoration",
                    0.15
                ),

                (
                    "Entertainment",
                    0.10
                ),

                (
                    "Contingency",
                    0.10
                )
            ]


            return {

                "title":
                    f"{data['event_type'].title()} party budget plan",

                "summary":
                    f"Plan for {data['guests']} guests with a contingency reserve.",

                "budget":
                    budget,

                "allocation": [

                    {
                        "category": category,

                        "amount":
                            round(
                                budget * percentage,
                                2
                            )
                    }

                    for category, percentage
                    in allocations
                ],

                "recommendations": [

                    {

                        "name": category,

                        "estimated_price":
                            round(
                                budget * percentage,
                                2
                            ),

                        "reason":
                            "Balanced budget allocation.",

                        "search_query":
                            (
                                f"{data['event_type']} "
                                f"{category} "
                                f"{data.get('venue_city', '')}"
                            )
                    }

                    for category, percentage
                    in allocations
                ]
            }


        # -------------------------------------------------
        # JEWELRY
        # -------------------------------------------------

        return {

            "title":
                "Occasion jewelry plan",

            "summary":
                "Style suggestions selected to stay within the jewelry budget.",

            "budget":
                budget,

            "allocation": [

                {
                    "category":
                        "Jewelry set",

                    "amount":
                        budget
                }
            ],

            "recommendations": [

                {

                    "name":
                        f"{data['style']} jewelry set",

                    "estimated_price":
                        round(
                            budget * 0.65,
                            2
                        ),

                    "reason":
                        "Main statement piece.",

                    "search_query":
                        (
                            f"{data['style']} "
                            f"jewelry "
                            f"{data['occasion']}"
                        )
                },

                {

                    "name":
                        "Matching earrings",

                    "estimated_price":
                        round(
                            budget * 0.20,
                            2
                        ),

                    "reason":
                        "Complements the main piece.",

                    "search_query":
                        (
                            f"{data['style']} earrings"
                        )
                },

                {

                    "name":
                        "Matching bracelet",

                    "estimated_price":
                        round(
                            budget * 0.15,
                            2
                        ),

                    "reason":
                        "Finishes the look.",

                    "search_query":
                        (
                            f"{data['style']} bracelet"
                        )
                }
            ]
        }


    # =====================================================
    # GEMINI GENERATION
    # =====================================================

    def generate(
        self,
        domain,
        data,
        image_path: Optional[str] = None
    ):

        # -------------------------------------------------
        # No API key
        # -------------------------------------------------

        if not self.client:

            result = self._fallback(
                domain,
                data
            )

            result["source_mode"] = (
                "demo-fallback"
            )

            result["recommendations"] = enrich(
                result["recommendations"],
                domain
            )

            return result


        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are PocketSmart AI,
a careful budget recommendation assistant.

Domain:
{domain}

User input:
{json.dumps(data, indent=2)}

Your job is to create a practical,
budget-aware recommendation plan.

IMPORTANT RULES:

1. Use INR.
2. Never claim live inventory.
3. Never claim exact current prices unless
   they were actually supplied.
4. Treat platform suggestions as search links.
5. Keep recommendations within the user's budget.
6. Give useful reasons for each recommendation.
7. Avoid unrealistic prices.
8. Return ONLY valid JSON.

Use this exact JSON structure:

{{
    "title": "string",

    "summary": "string",

    "budget": number,

    "allocation": [
        {{
            "category": "string",
            "amount": number
        }}
    ],

    "recommendations": [
        {{
            "name": "string",
            "estimated_price": number,
            "reason": "string",
            "search_query": "string"
        }}
    ]
}}

Give approximately 5 to 8 recommendations.
"""


        contents = [
            prompt
        ]


        # -------------------------------------------------
        # IMAGE
        # -------------------------------------------------

        if image_path:

            image = Image.open(
                image_path
            )

            contents.append(image)

            contents.append(
                """
Analyze the uploaded outfit image only
for color coordination, visible style,
and aesthetic compatibility.

Do not identify the person.
Do not infer sensitive personal attributes.
"""
            )


        # -------------------------------------------------
        # GEMINI REQUEST
        # -------------------------------------------------

        try:

            response = (
                self.client.models.generate_content(

                    model=settings.gemini_model,

                    contents=contents,

                    config=types.GenerateContentConfig(

                        temperature=0.4,

                        response_mime_type=
                            "application/json"
                    )
                )
            )

            result = json.loads(
                response.text
            )


            result["source_mode"] = "gemini"


            result["recommendations"] = enrich(
                result.get(
                    "recommendations",
                    []
                ),
                domain
            )


            return result


        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------
        except Exception as error:

            import traceback

            print("\n" + "=" * 60)
            print("GEMINI FULL ERROR")
            print("=" * 60)

            print("ERROR:", repr(error))

            traceback.print_exc()

            print("=" * 60 + "\n")

            result = self._fallback(
                domain,
                data
            )

            result["source_mode"] = (
                "fallback-after-ai-error"
            )

            result["recommendations"] = enrich(
                result["recommendations"],
                domain
            )

            return result
        

gemini_service = GeminiService()