from oct_converter.readers import E2E
from construct import Array, Int8un, Int16un, Int32sn, Int32un, PaddedString, Struct

filepaths = [
            {'path':"/Users/mark/Library/CloudStorage/Dropbox/Work/Projects/OCT-Converter/my_example_volumes/e2e-vassily/PatientIDTIN0007-ADAMIDIS/DIMIT001.E2E",
                'start': 36897},
             {'path':"/Users/mark/Library/CloudStorage/Dropbox/Work/Projects/OCT-Converter/my_example_volumes/e2e-vassily/PatientIDTIN0007-ADAMIDIS/DIMIT002.E2E",
                'start': 29565},
            {'path':"/Users/mark/Library/CloudStorage/Dropbox/Work/Projects/OCT-Converter/my_example_volumes/e2e-vassily/new-e2e-11-06-2022/TIN0901T.E2E",
                'start': 29756},
             {'path':"/Users/mark/Library/CloudStorage/Dropbox/Work/Projects/OCT-Converter/my_example_volumes/e2e-vassily/new-e2e-11-06-2022/TIN0902T.E2E",
            'start':644526}
]

file = E2E(filepaths[0]['path'])
oct_volumes = (
    file.read_oct_volume()
)  # returns a list of all OCT volumes with additional metadata if available
for volume in oct_volumes:
    list_of_slices = volume.volume
    slice_as_np_array = list_of_slices[0]
    numpy_volume = volume.volume
    #volume.peek()  # plots a montage of the volume
    volume.save("{}_{}.png".format(volume.volume_id, volume.laterality))

# fundus_images = (
#     file.read_fundus_image()
# )  # returns a list of all fundus images with additional metadata if available
# for image in fundus_images:
#     image.save("{}+{}.png".format(image.image_id, image.laterality))
