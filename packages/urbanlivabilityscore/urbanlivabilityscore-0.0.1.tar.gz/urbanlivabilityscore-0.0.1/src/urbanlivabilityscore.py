def street_lighting_score(w, n):
    road_width = []
    height_pole = []
    spacing_pole = []

    for width in w:
        road_width.append(width)
        h = width/3
        height_pole.append(h)

    for numb in n:
        s = 100/numb
        spacing_pole.append(s)

    h_score = [(height_pole/2.5)/spacing_pole for height_pole,
               spacing_pole in zip(height_pole, spacing_pole)]
    w_score = [(h_score*2.5)/road_width for h_score,
               road_width in zip(h_score, road_width)]

    lighting_score = [h_score + w_score for h_score,
                      w_score in zip(h_score, w_score)]

    lighting_score_min = min(lighting_score)
    lighting_score_max = max(lighting_score)

    norm = [round(((lgt_score - lighting_score_min) / (lighting_score_max -
                                                       lighting_score_min) * 10), 3) for lgt_score in lighting_score]
    return norm
