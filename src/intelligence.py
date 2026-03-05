def analyze_mix_intelligence(scores, results):

    insights = []

    # tonal balance

    if scores["presence"] < 70:
        insights.append(
        "Your mix lacks presence energy. This can make vocals and lead elements sound distant."
        )

    if scores["sub"] > 90:
        insights.append(
        "Your sub energy is stronger than the reference. This may cause translation issues on smaller speakers."
        )

    # masking

    for issue in results["issues"]:

        if issue["type"] == "Low-Mid Masking":

            insights.append(
            "Low-mid frequencies between 200–400Hz are masking other elements. This region often becomes crowded with guitars, pads, and vocals."
            )

    # dynamics

    crest = results["dynamics"]["crest_factor"]

    if crest < 4:

        insights.append(
        "Your mix may be over-compressed. Low crest factor indicates reduced transient impact."
        )

    # stereo

    width = results["spatial"]["stereo_width"]

    if width < 0.05:

        insights.append(
        "Stereo width is narrow compared to typical mixes. Consider widening high-frequency elements."
        )

    return insights