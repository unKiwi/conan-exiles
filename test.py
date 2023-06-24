import cv2
import numpy as np

# Charger l'image
image = cv2.imread("image.jpg")  # Remplacez "image.jpg" par le chemin de votre propre image

# Convertir l'image en espace de couleur HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Définir la plage des valeurs de couleur violette dans l'espace HSV
lower_violet = np.array([150, 50, 50])
upper_violet = np.array([170, 255, 255])

# Masque pour isoler les pixels violets
mask = cv2.inRange(hsv, lower_violet, upper_violet)

# Appliquer le masque à l'image originale
result = cv2.bitwise_and(image, image, mask=mask)

# Afficher l'image résultante avec seulement les pixels violets
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()