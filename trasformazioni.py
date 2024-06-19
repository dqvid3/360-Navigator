import cv2
import numpy as np


def matrice_rotazione_y(pitch):
    """
        Ruota intorno all'asse Y.
        :param pitch: Angolo di rotazione (in radianti).
    """
    return np.array([[np.cos(pitch), 0, np.sin(pitch)],
                     [0, 1, 0],
                     [- np.sin(pitch), 0, np.cos(pitch)]])


def matrice_rotazione_z(yaw):
    """
        Ruota intorno all'asse Z.
        :param yaw: Angolo di rotazione (in radianti).
    """
    return np.array([[np.cos(yaw), - np.sin(yaw), 0],
                     [np.sin(yaw), np.cos(yaw), 0],
                     [0, 0, 1]])


def cartesiane_a_sferiche(x, y, z, f=1):  # pag 16 sx
    """
        Passaggio di coordinate.
        :param x: ascissa
        :param y: ordinata
        :param z: quota
        :param f: distanza focale.
    """
    latitudine = np.pi / 2 - np.arccos(z / f)
    longitudine = np.arctan2(y, x)
    return latitudine, longitudine


def equirettangolare_a_planare(img, fov, theta, phi, h_output, w_output):
    """
        Trasformazione immagine da equirettangolare a planare
        :param img: immagine
        :param fov: campo visivo (in gradi)
        :param theta: angolo orizzontale (in gradi)
        :param phi: angolo verticale (in gradi)
        :param h_output: altezza immagine planare
        :param w_output: ampiezza immagine planare
    """
    # Dimensioni dell'immagine equirettangolare
    h_input, w_input = img.shape[:2]
    # Centro  dell'immagine equirettangolare (indici da 0):
    centro_x = (w_input - 1) / 2.0
    centro_y = (h_input - 1) / 2.0

    """
    Calcola il campo visivo verticale (fov_h) basandosi sul campo visivo
    orizzontale (fov_W) e sulle dimensioni dell'immagine di output (h_output
    e w_output), in modo che l'immagine di output abbia le proporzioni corrette.
    """
    fov_w = fov
    aspect_ratio = float(h_output) / w_output
    fov_h = aspect_ratio * fov_w

    # Calcola la meta' della lunghezza del lato orizzontale del piano di proiezione.
    w_2 = np.tan(np.radians(fov_w / 2.0))
    # Calcola la meta' della lunghezza del lato verticale del piano di proiezione. (pag 18)
    h_2 = np.tan(np.radians(fov_h / 2.0))

    """
    Crea una mappa del piano di proiezione, rappresentato da 3 matrici 2D (una per ciascun asse).
    np.linspace(a, b, c) genera una sequenza di c valori equidistanti nell'intervallo [a, b], che
    rappresenta l'intervallo delle coordinate del piano di proiezione.
    """
    # x = 1 (pag 19)
    x_map = np.ones([h_output, w_output], np.float32)
    # Replica la sequenza di valori h_output volte lungo l'asse verticale.
    y_map = np.tile(np.linspace(-w_2, w_2, w_output), [h_output, 1])
    # Replica la sequenza di valori w_output volte lungo l'asse orizzontale.
    # Il segno negativo su z_map e' necessario per creare un piano di proiezione correttamente orientato
    # secondo la convenzione del sistema di coordinate 3D utilizzata in OpenCV.
    z_map = - np.tile(np.linspace(-h_2, h_2, h_output), [w_output, 1]).T

    # Norma euclidea (norma 2).
    d = np.sqrt(x_map * x_map + y_map * y_map + z_map * z_map)

    """
    Dividiamo (normalizziamo) ogni componente del vettore di coordinate per la sua norma. 
    Per farlo:
        1) Combina le matrici 2D x_map, y_map e z_map in un singolo array 3D chiamato xyz.
        axis=2 specifica che le matrici devono essere impilate lungo il terzo asse (asse z),
        creando un array 3D con dimensione [h_output, w_output, 3].
        2) Poiche' d e' una matrice 2D con dimensione [h_output, w_output], np.newaxis aggiunge una nuova
        dimensione all'array d, trasformandolo in un array 3D con shape [height, width, 1].
    """
    xyz = np.divide(np.stack((x_map, y_map, z_map), axis=2), d[:, :, np.newaxis])  # pag 15

    # Converte in radianti:
    theta = np.radians(theta)
    phi = - np.radians(phi)

    # Applica le matrici di rotazione:
    Rz = matrice_rotazione_z(theta)
    Ry = matrice_rotazione_y(phi)
    R = np.dot(Rz, Ry)
    # Per "appattare" le dimensioni
    xyz = xyz.reshape([h_output * w_output, 3]).T
    xyz = np.dot(R, xyz).T

    # Passaggio di coordinate:
    lat, lon = cartesiane_a_sferiche(xyz[:, 0], xyz[:, 1], xyz[:, 2])

    """
    Convertiamo in gradi.
    Poiche' le immagini hanno un'origine in alto a sinistra, mentre i piani sono convenzionalmente 
    orientati in basso a sinistra, e' necessario invertire il segno della latitudine. 
    Questo assicura che l'asse verticale dell'immagine sia correttamente allineato con il sistema 
    di riferimento delle coordinate sferiche.
    """
    lat = - np.degrees(lat.reshape([h_output, w_output]))
    lon = np.degrees(lon.reshape([h_output, w_output]))

    # Normalizza le coordinate (pag 16 dx):
    lat /= 90
    lon /= 180

    """
    Moltiplica le coordinate per il centro in modo da mapparle nell'intervallo originale (indici da 0).
    Aggiunge il centro per spostare l'origine delle coordinate al centro dell'immagine. (pag 16 dx)
    """
    lat = lat * centro_y + centro_y
    lon = lon * centro_x + centro_x

    # Interpolazione bilineare (usando remap). (pag 19)
    return cv2.remap(img, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_LINEAR)


def zoom(img, scale):
    """
        Ingrandisci l'immagine nel centro
        :param img: immagine
        :param scale: zoom (da 0 a 10)
    """
    h_nuova, w_nuova, _ = [scale * i for i in img.shape]
    centro_x, centro_y = (w_nuova - 1) / 2, (h_nuova - 1) / 2
    img_ritagliata = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    """
    Esempio: 
        100x100
        Diventa 200x200 con zoom 2
        (100,100) e' il centro
        x1 = 100-200/2/2 = 50 = y1
        x2 = 100+50/2/2 = 150 = y2
    """
    x1 = int(round(centro_y - h_nuova / scale / 2))
    x2 = int(round(centro_y + h_nuova / scale / 2))
    y1 = int(round(centro_x - w_nuova / scale / 2))
    y2 = int(round(centro_x + w_nuova / scale / 2))

    return img_ritagliata[x1:x2, y1:y2]
