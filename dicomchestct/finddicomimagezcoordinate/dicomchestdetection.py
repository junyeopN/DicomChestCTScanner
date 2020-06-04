
class ResultPrinter:
    def __init__(self, lung_detection_result_table, dicom_image_table):
        self.__lung_detection_result_table = lung_detection_result_table
        self.__dicom_image_table = dicom_image_table

    def __find_image_z_coordinate_boundaries(self, ct_index):
        ct_images = self.__dicom_image_table[ct_index]

        first_image = self.__find_first_image(ct_images)
        last_image = self.__find_last_image(ct_images)

        return (self.__get_z_coordinate(first_image), self.__get_z_coordinate(last_image))

    def __find_first_image(self, ct_images):
        return ct_images[0]

    def __find_last_image(self, ct_images):
        return ct_images[len(ct_images) - 1]

    def __get_z_coordinate(self, ct_image):
        return ct_image.ImagePositionPatient[2].real

    def __find_lung_z_coordinate_boundaries(self, ct_index):
        result_list = self.__lung_detection_result_table[ct_index]
        ct_images = self.__dicom_image_table[ct_index]

        (first_lung_image_index, last_lung_image_index) = self.__find_first_last_lung_image(result_list)

        first_lung_image = None
        last_lung_image = None

        first_lung_image = self.__find_image(ct_images, first_lung_image_index)
        last_lung_image = self.__find_image(ct_images, last_lung_image_index)

        return (self.__get_z_coordinate(first_lung_image), self.__get_z_coordinate(last_lung_image))

    def __find_image(self, ct_images, index):
        if (index < 0):
            return None
        else:
            return ct_images[index]

    def __find_first_last_lung_index(self, result_list):
        first_detected_index = -1
        last_detected_index = -1

        for i in range(len(result_list)):
            if (self.__satisfies_detection_condition(result_list, i)):
                if (first_detected_index < 0):
                    first_detected_index = i

                last_detected_index = i

        return (first_detected_index, last_detected_index)

    def __satisfies_detection_condition(self, result_list, index):
        return result_list[index]

    def make_result(self, lung_detection_result_table):
        coordinate_list = []
        for i in range(len(lung_detection_result_table)):
            image_boundaries = self.__find_image_z_coordinate_boundaries(i)
            lung_boundaries = self.__find_lung_z_coordinate_boundaries(i)
            coordinate_list.append([image_boundaries, lung_boundaries])

        return coordinate_list


# Create your models here.
class DicomChestCTScanner:

    def execute(self, ct_image_table, lung_detection_model):
        patient_number = len(ct_image_table)
        lung_detection_result_table = LungDetectionResultTable()

        for i in range(patient_number):
            lung_detection_result_table.make_new_list()

            for j in range(len(ct_image_table[i])):
                current_dicom_image = ct_image_table[i][j]
                image_scan_result = lung_detection_model.predict(current_dicom_image.pixel_array)
                lung_detection_result_table.add_result(image_scan_result)

        return ResultPrinter(lung_detection_result_table, ct_image_table).make_result()

class LungDetectionResultTable:
    def __init__(self):
        self.__result_table = []
        self.__table_size = 0

    def add_result(self, new_result):
        target_list = self.__result_table[self.__table_size - 1]
        target_list.append(new_result)
        return

    def make_new_list(self):
        self.__result_table.append([])
        self.__table_size = self.__table_size + 1
        return

    def get_result_list(self, result_id):
        return self.__result_table[result_id]
