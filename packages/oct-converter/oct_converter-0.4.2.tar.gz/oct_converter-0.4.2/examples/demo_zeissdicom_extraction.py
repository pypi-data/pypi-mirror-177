from oct_converter.readers import ZEISSDicom

filepath = "../sample_files/sample_zeissdcm.dcm"
img = ZEISSDicom(filepath)

oct_volumes = (
    img.read_oct_volume()
)  # returns a list of OCT volumes with additional metadata if available

for idx, volume in enumerate(oct_volumes):
    volume.save(f"zeiss_volume_{idx}.png")  # save all volumes
