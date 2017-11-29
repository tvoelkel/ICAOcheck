# ICAOcheck

## Lighting:
Lighting check works by examining the mean intensity values of each color channel at 4 specific locations in the image. An edge detection filter is applied as well, to make sure that each measurement zone is homogeneous enough for an accurate mean intensity measurement.

<p align="center">
  <img src="https://i.imgur.com/eVDUu2n.jpg" width="350"/>
</p>

### Explanation of output messages
**Failed: More than one face detected.**  
Dlib frontal face detector detected more than one face in the input image.

**Failed: No face detected.**  
Dlib frontal face detector detected no face in the input image.

**Failed: Inner eye distance smaller than 90px.**  
As stated in the ICAO standard for passport photographs, the distance between both eyes has to be at least 90 Pixels. Try a higher resolution image.

**Failed:  Not enough homogenous facial zones.**  
Two or more zones in the image are not homogenous. That means, there is a certain amount of edges detected inside the zone to flag it as inhomogeneous. An example for this is the red zone in the example image above.

**Failed: Light intensity difference to high.**  
The mean intensity value of one zone is less than half of the mean intensity value of another zone, regarding each color channel. This determines whether the lighting across the face is in compliance with ICAO standards.

**Passed.**  
The image is in compliance with ICAO standards in regard to lighting requirements.
