import os
import cv2


class RenameVideoFiles:
    """
    Renomme une video au format : <titre-de-la-video>_<longueur>x<largeur>_<VOSTFR>_<poid du fichier>
    """
    def __init__(self):
        self.full_path = ""
        self.renaming_format = ""
        self.title = ""
        self.lang = ""
        self.season_number = -1

    def _check_path(self):
        """ Check if the path is valid"""

        if not os.path.exists(self.full_path):
            raise ValueError(f"Add a valid path (full_path), '{self.full_path}' does not exist")

    def _get_files(self):
        """ Get all renammable files from path """

        if os.path.isdir(self.full_path):
            self.files = [f for f in os.listdir(self.full_path) if f.endswith((".mp4", ".mkv"))]
        else:
            self.files = [os.path.basename(self.full_path)]

        self.directory = os.path.dirname(self.full_path)

    def _check_renaming_format(self):
        """ Check renaming format"""

        if self.renaming_format not in ["movie", "serie"]:
            raise ValueError(f"'{self.renaming_format}' is not a valid renaming format (renaming_format)")

    def _check_attributes(self):
        """ Check if other attributes are OK """

        # Check the title
        if not self.title or len(self.title) > 100:
            raise ValueError("Add a valid title (title)")
        
        # Check the language
        if not self.lang or len(self.lang) > 10:
            raise ValueError("Add a valid language (lang)")

        if self.renaming_format == "serie":
            # Check the season number
            if self.season_number < 0:
                raise ValueError("Add a valid season number (season_number)")
        
        else:
            if len(self.files) > 1:
                raise ValueError("You have to rename one movie at a time")
    
    @staticmethod
    def _get_file_infos(file_path):
        """ Get infos about the video file """

        cv2video = cv2.VideoCapture(file_path)
        height = int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH))
        size_mb = int(os.path.getsize(file_path) / 10**6)
        video_format = file_path.split(".")[-1]

        return {"height":height, "width":width, "size_mb":size_mb, "video_format":video_format}
    
    def _rename(self):
        """ Rename the file(s) """
        
        new_title = self.title.replace(" ", "-").lower()
        self.new_files_name = []
        self.old_files_name = []

        if self.renaming_format == "movie":
            old_file_path = os.path.join(self.directory, self.files[0])
            movie_infos = self._get_file_infos(old_file_path)
            
            new_file_name = f"{new_title}_{movie_infos['width']}x{movie_infos['height']}_{self.lang}_{movie_infos['size_mb']}MB.{movie_infos['video_format']}"
            new_file_path = os.path.join(self.directory, new_file_name)
            self.new_files_name.append(new_file_name)
            self.old_files_name.append(self.files[0])
            
            os.rename(old_file_path, new_file_path)

        if self.renaming_format == "serie":
            for f in self.files:
                old_file_path = os.path.join(self.directory, f)
                movie_infos = self._get_file_infos(old_file_path)
                episode_number = int(input(f"Numéro de l'épisode '{f}' : "))

                new_file_name = f"{new_title}_S{self.season_number:02d}E{episode_number:02d}_{movie_infos['width']}x{movie_infos['height']}_{self.lang}_{movie_infos['size_mb']}MB.{movie_infos['video_format']}"
                new_file_path = os.path.join(self.directory, new_file_name)
                self.new_files_name.append(new_file_name)
                self.old_files_name.append(f)

                os.rename(old_file_path, new_file_path)
    
    def rename(self):
        """ Rename method which can be call """

        self._check_path()
        self._get_files()
        self._check_renaming_format()
        self._check_attributes()

        self._rename()


if __name__ == "__main__":
    # f = RenameVideoFiles()
    # f.full_path = "/media/mathias/wd_1to/series/shingeki-no-kyojin/s4/"
    # f.renaming_format = "serie"
    # f.title = "shingeki-no-kyojin"
    # f.lang = "VOSTFR"
    # f.season_number = 4
    # f.rename()