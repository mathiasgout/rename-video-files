import os
import cv2


def rename_file(filepath, title, vostfr=True):
    """
    Renomme une video au format : <titre-de-la-video>_<longueur>x<largeur>_<VOSTFR>_<poid du fichier>
    """

    DIR_PATH = os.path.dirname(filepath)

    cv2video = cv2.VideoCapture(filepath)
    height = int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    size_mb = int(os.path.getsize(filepath) / 10**6)
    new_title = "-".join(title.split(" ")).lower()
    video_type = filepath.split(".")[-1]

    if vostfr:
        new_name = new_title + "_" + str(width) + "x" + str(height) + "_" + "VOSTFR" + "_" + str(size_mb) + "MB" + "." + video_type
    else:
        new_name = new_title + "_" + str(width) + "x" + str(height) + "_" + "VO" + "_" + str(size_mb) + "MB" + "." + video_type
    
    NEW_PATH_NAME = os.path.join(DIR_PATH, new_name)
    os.rename(filepath, NEW_PATH_NAME)


if __name__ == "__main__":
    rename_file("/media/mathias/Mathias/Anime/Free The Movie (High Speed - Free Starting Days...BLURAY][1080p][h264_8b][HE-AAC][Circus-Fansub].mp4", "Free!", vostfr=True)    
    
