from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.iris_data import IrisDataFilter
import matplotlib.pyplot as plt
import os

app = FastAPI()

# Initialize the IrisDataFilter with the path to your dataset
iris_data_filter = IrisDataFilter(
    file_path="C:\Users\Lenovo\Downloads\Assignment21\Data\Iris.csv")


@app.get("/species/")
async def get_filtered_data(species: str):
    # Filter data by species
    filtered_data = iris_data_filter.filter_by_species(species)

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Species not found")
    
    image_folder = "visualizations"
    os.makedirs(image_folder, exist_ok=True)
    image_path = os.path.join(image_folder, f"{species}_distribution.png")

    # Generate and save the visualization
    plt.figure()
    filtered_data.hist(bins=20, figsize=(10, 8))
    image_path = f"{species}_distribution.png"
    plt.savefig(image_path)
    plt.close()

    # Check if the image was actually saved
    if not os.path.exists(image_path):
        raise HTTPException(status_code=500, detail="Image generation failed")

    # Return the filtered data and the path to the visualization image
    return {"data": filtered_data.to_dict(orient="records"), "image": image_path}


@app.get("/visualize/")
async def visualize_species(species: str):
    # Construct the image path based on species
    image_folder = "visualizations"
    image_path = f"{species}_distribution.png"

    # Check if the image exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image as a FileResponse
    return FileResponse(image_path)