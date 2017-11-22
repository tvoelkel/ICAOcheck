def checkExpression(imagelist):
    for image in imagelist:
        image.matching_type_list.append("Expression Check: ")
        image.matching_score_list.append(image.image_name)
