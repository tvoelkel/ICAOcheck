def checkBackground(imagelist):
    for image in imagelist:
        image.matching_type_list.append("Background Check: ")
        image.matching_score_list.append(1)