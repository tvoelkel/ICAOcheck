def checkColor(imagelist):
    for image in imagelist:
        image.matching_type_list.append("Color Check: ")
        image.matching_score_list.append(1)

        image.matching_results["Color"]="Ergebnis Color"
