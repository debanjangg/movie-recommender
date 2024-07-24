import pickle

def get_simMat():
    file_prefix = 'sim_mat_tfIdf_part_'

    merged_data = bytearray()
    
    for i in range(4):
        part_file = f"{file_prefix}{i:02}"
        with open(part_file, "rb") as f:
            merged_data.extend(f.read())
    
    with open(output_file, "wb") as f:
        f.write(merged_data)
    
    with open(output_file, "rb") as f:
        matrix = pickle.load(f)

    return matrix