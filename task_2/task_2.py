"""
2. Object-Oriented Programming (OOP)
"""
import os
from dotenv import load_dotenv
import logging
import pydicom

# Load .env file
load_dotenv()
path = os.getenv("FOLDER_PATH")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PatientRecord:
    def __init__(self, name=None, age=None, birth_date=None, sex=None, weight=None, patient_id=None, patient_id_type=None):
        self.name = name
        self.age = age
        self.birth_date = birth_date
        self.sex = sex
        self.weight = weight
        self.patient_id = patient_id
        self.patient_id_type = patient_id_type
        self.diagnosis = None

    def set_patient_info(self, name, age, birth_date, sex, weight, patient_id, patient_id_type):
        self.name = name
        self.age = age
        self.birth_date = birth_date
        self.sex = sex
        self.weight = weight
        self.patient_id = patient_id
        self.patient_id_type = patient_id_type

    def get_patient_info(self):
        return {
            "Name": self.name,
            "Age": self.age,
            "Birth Date": self.birth_date,
            "Sex": self.sex,
            "Weight": self.weight,
            "Patient ID": self.patient_id,
            "Patient ID Type": self.patient_id_type,
        }

    def update_diagnosis(self, new_diagnosis):
        logging.info(f"Updating diagnosis from '{self.diagnosis}' to '{new_diagnosis}'")
        self.diagnosis = new_diagnosis


class StudyRecord(PatientRecord):
    def __init__(self, name=None, age=None, birth_date=None, sex=None, weight=None, patient_id=None, patient_id_type=None):
        super().__init__(name, age, birth_date, sex, weight, patient_id, patient_id_type)
        self.modality = None
        self.study_date = None
        self.study_time = None
        self.study_instance_uid = None
        self.series_number = None
        self.number_of_frames = None

    def set_study_info(self, modality, study_date, study_time, study_instance_uid, series_number, number_of_frames):
        self.modality = modality
        self.study_date = study_date
        self.study_time = study_time
        self.study_instance_uid = study_instance_uid
        self.series_number = series_number
        self.number_of_frames = number_of_frames

    def get_study_info(self):
        return {
            "Modality": self.modality,
            "Study Date": self.study_date,
            "Study Time": self.study_time,
            "Study Instance UID": self.study_instance_uid,
            "Series Number": self.series_number,
            "Number of Frames": self.number_of_frames,
        }

    def load_study_from_dicom(self, dicom_filepath):
        try:
            dicom_data = pydicom.dcmread(dicom_filepath)

            # Set patient information
            self.set_patient_info(
                name=dicom_data.get("PatientName", None),
                age=dicom_data.get("PatientAge", None),
                birth_date=dicom_data.get("PatientBirthDate", None),
                sex=dicom_data.get("PatientSex", None),
                weight=dicom_data.get("PatientWeight", None),
                patient_id=dicom_data.get("PatientID", None),
                patient_id_type=dicom_data.get("TypeOfPatientID", None)
            )

            # Set study information
            self.set_study_info(
                modality=dicom_data.get("Modality", None),
                study_date=dicom_data.get("StudyDate", None),
                study_time=dicom_data.get("StudyTime", None),
                study_instance_uid=dicom_data.get("StudyInstanceUID", None),
                series_number=dicom_data.get("SeriesNumber", None),
                number_of_frames=dicom_data.get("NumberOfFrames", None)
            )
        except Exception as e:
            logging.error(f"Error loading DICOM file '{dicom_filepath}': {e}")

    def __str__(self):
        patient_info = self.get_patient_info()
        study_info = self.get_study_info()

        info = "Patient Information:\n"
        info += "\n".join([f"{key}: {value}" for key, value in patient_info.items()])

        info += "\n\nStudy Information:\n"
        info += "\n".join([f"{key}: {value}" for key, value in study_info.items()])

        return info


# Example usage
if __name__ == '__main__':
    study_record = StudyRecord()
    study_record.load_study_from_dicom(f"{path}/sample-02-dicom.dcm")
    print(study_record)
