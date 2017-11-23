def checkGeometry(imagelist):
    for image in imagelist:
        image.matching_type_list.append("Geometry Check: ")
        image.matching_score_list.append(1)

        image.matching_results["Geometry"]="Ergebnis Geometry"