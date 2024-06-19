import datetime
import cv2
from trasformazioni import equirettangolare_a_planare, zoom
import os


def processa_frame(frame, w_output, fov, theta, phi, scale, tempo=""):
    frame = equirettangolare_a_planare(frame, fov, theta + 180, 90 - phi, w_output, w_output)
    frame = zoom(frame, scale)
    testo = f"(Fov, Theta, Phi, Zoom) = ({fov}, {theta}, {phi}, {scale}x)\n{tempo}"
    aggiungi_testo(frame, testo)
    cv2.imshow(f"output {w_output}x{w_output}", frame)
    return frame


def leggi_frame(filename, param1, param2, param3):
    frame = cv2.imread(filename)
    if frame is None:
        print("Impossibile aprire l'immagine. Assicurati che il percorso sia corretto.")
        return
    muovi(frame, param1, param2, param3, False)


def leggi_video(filename, param1, param2, param3):
    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Impossibile aprire il video. Assicurati che il percorso sia corretto.")
        return
    muovi(cap, param1, param2, param3, True)


def aggiungi_testo(img, testo):
    testo1, tempo = testo.split("\n")
    if tempo != "":
        _, parte_decimale = tempo.split('.')
        if len(parte_decimale) == 1:
            tempo += "0"
        tempo = "Tempo trascorso: " + tempo + " s"
    font = cv2.FONT_HERSHEY_SIMPLEX
    # per adattare a risoluzioni piu' grandi
    font_scale = img.shape[1] / 900
    thickness = int(font_scale * 3)
    h = cv2.getTextSize(testo1, font, font_scale, thickness)[0][1]
    # Posizione del testo nell'angolo in alto a sinistra
    posizione = (50, h + 50)
    cv2.putText(img, testo1, posizione, font, font_scale, (0, 0, 255), thickness)
    posizione = (50, h + 100)
    cv2.putText(img, tempo, posizione, font, font_scale, (0, 0, 255), thickness)


def screenshot(frame):
    now = datetime.datetime.now()
    data_ora_stringa = now.strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs('screenshots', exist_ok=True)
    cv2.imwrite(f"screenshots/screenshot-{data_ora_stringa}.png", frame)


def muovi(file, fov, theta, phi, is_video):
    if is_video:
        ret, frame = file.read()
        frame_time_total = 0
        frame_time = 1 / file.get(cv2.CAP_PROP_FPS)
        process_time = 0
        start_time = cv2.getTickCount() / cv2.getTickFrequency()
        paused_time = 0
    else:
        frame = file
    w_output = frame.shape[1]
    # Per migliorare le prestazioni riduco in base l'ampiezza dell'immagine di input
    if w_output < 4096:
        w_output //= 2
    else:
        w_output //= 4
    key = 0
    scale = 1.0
    is_paused = False
    while key != 27:
        if is_video:
            start = cv2.getTickCount() / cv2.getTickFrequency()
            if not is_paused:
                current_time = start - start_time - paused_time
            frame_p = processa_frame(frame, w_output, fov, theta, phi, scale, str(round(current_time, 2)))
            end = cv2.getTickCount() / cv2.getTickFrequency()
            if not is_paused:
                process_time += end - start
                frame_time_total += frame_time
                if process_time > frame_time_total:
                    skip_frame = int((process_time - frame_time_total) / frame_time) + 1
                    for _ in range(skip_frame):
                        ret, frame = file.read()
                        if not ret:
                            break
                    process_time = frame_time_total
                    ret, frame = file.read()
                    if not ret:
                        break
        else:
            frame_p = processa_frame(frame, w_output, fov, theta, phi, scale)
        key = cv2.waitKey(int(is_video)) & 0xFF
        if key == ord('a'):
            theta -= 5
        elif key == ord('d'):
            theta += 5
        elif key == ord('w'):
            phi -= 5
        elif key == ord('s'):
            phi += 5
        elif key == ord('q'):
            fov += 5
        elif key == ord('e'):
            fov -= 5
        elif key == ord('z'):
            scale -= 0.2
        elif key == ord('x'):
            scale += 0.2
        elif key == ord('p'):
            screenshot(frame_p)
        elif key == ord(' ') and is_video:
            if is_paused:
                video_resume_time = cv2.getTickCount() / cv2.getTickFrequency()
                paused_time += video_resume_time - video_pause_time
            else:
                video_pause_time = cv2.getTickCount() / cv2.getTickFrequency()
            is_paused = not is_paused
        scale = round(max(1.0, min(10.0, scale)), 2)
        fov %= 180
        theta %= 360
        phi %= 360

    if is_video:
        file.release()
    cv2.destroyAllWindows()
