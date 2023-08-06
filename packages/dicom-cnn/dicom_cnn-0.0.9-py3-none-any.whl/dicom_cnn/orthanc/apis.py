import io
import json
import requests
import numpy

from dicom_cnn.instance.dicom_instance import DicomInstance
from dicom_cnn.reader.dicom_instance_orthanc_reader import DicomInstanceOrthancReader, DicomInstanceOrhtancReaderPT
from dicom_cnn.instance.dicom_enums import Modalities
from dicom_cnn.series.series import Series
from dicom_cnn.series.series_pt import SeriesPT


class OrthancApis:
    def __init__(self) -> None:
        self.login = ''
        self.password = ''

    def set_orthanc_server(self, url: str) -> None:
        self.host = url

    def set_orthanc_port(self, port: int) -> None:
        self.port = port

    def set_orthanc_credential(self, login: str, password: str):
        self.login = login
        self.password = password

    def get_instance_numpy(self, instance_orthanc_id: str) -> numpy.array:
        response_pixel = requests.get(
            self.host+'/instances/'+instance_orthanc_id+'/numpy?rescale=true', auth=(self.login, self.password))
        pixels = numpy.load(io.BytesIO(response_pixel.content))
        return pixels

    def get_instance_metadata(self, instance_orthanc_id: str) -> dict:
        response = requests.get(
            self.host+'/instances/'+instance_orthanc_id+'/tags', auth=(self.login, self.password))
        dicom_metadata = json.loads(response.text)
        return dicom_metadata

    def get_series_infos(self, series_orthanc_id: str) -> dict:
        response = requests.get(
            self.host+'/series/'+series_orthanc_id, auth=(self.login, self.password))
        series_data = json.loads(response.text)
        return series_data

    def read_instance(self, orthanc_instance_id: str, read_pixel: bool) -> DicomInstance:
        dicom_metadata = self.get_instance_metadata(
            orthanc_instance_id)
        pixels = None
        if (read_pixel):
            pixels = self.get_instance_numpy(orthanc_instance_id)

        temporary_instance = DicomInstanceOrthancReader(
            dicom_metadata, None).get_instance()
        modality = temporary_instance.get_modality()
        if (modality == Modalities.PT.value):
            return DicomInstanceOrhtancReaderPT(dicom_metadata, pixels).get_instance()
        else:
            return DicomInstanceOrthancReader(dicom_metadata, pixels).get_instance()

    def read_series(self, orthanc_series_id: str, read_pixel: bool) -> Series:
        series_info = self.get_series_infos(orthanc_series_id)
        instances_ids_list = series_info['Instances']
        instances = []
        for instance_orthanc_id in instances_ids_list:
            instance = self.read_instance(instance_orthanc_id, read_pixel)
            instances.append(instance)

        if (isinstance(instances[0], DicomInstanceOrhtancReaderPT)):
            return SeriesPT(instances)
        else:
            return Series(instances)
