from dataclasses import dataclass
#from .image_set import ImageSet
from ..io import reader


@dataclass(frozen=True)
class InstrumentModel:
    file_directry: str
    suffix:str
    extension: str 

    def path_list(self) -> list:
        return reader.get_path_list(
                                file_directry= self.file_directry,
                                suffix= self.suffix,
                                extension=self.extension
                                )
#ImageSetへ移植済み(2026.1.8)
#    def load(self):
#        path_list = self.path_list()
#        data, hdr_profile = reader.load_data(path_list)
#
#        return ImageSet(data= data, noise= None, 
#                        hdr_profile= hdr_profile,
#                        status={}, status_keyword={"POL0":{},"POL60":{},"POL120":{}}) 
