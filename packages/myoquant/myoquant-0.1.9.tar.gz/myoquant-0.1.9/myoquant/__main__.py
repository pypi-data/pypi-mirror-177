import time
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Analysis Results")

app = typer.Typer(
    name="MyoQuant",
    add_completion=False,
    help="MyoQuant Analysis Command Line Interface",
    pretty_exceptions_show_locals=False,
)

from .utils.docs import app as docs_app

app.add_typer(docs_app, name="docs", help="Generate documentation")


@app.command()
def sdh_analysis(
    image_path: Path = typer.Argument(
        ...,
        help="The image file path to analyse.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    mask_path: Path = typer.Option(
        None,
        help="The path to a binary mask to hide slide region during analysis. It needs to be of the same resolution as input image and only pixel marked as 1 will be analyzed.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    model_path: Path = typer.Option(
        None,
        help="The SDH model path to use for analysis. Will download latest one if no path provided.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    cellpose_path: Path = typer.Option(
        None,
        help="The pre-computed CellPose mask to use for analysis. Will run Cellpose if no path provided. Required as an image file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    output_path: Path = typer.Option(
        None,
        help="The path to the folder to save the results. Will save in the current folder if not specified.",
    ),
    cellpose_diameter: int = typer.Option(
        None,
        help="Approximative single cell diameter in pixel for CellPose detection. If not specified, Cellpose will try to deduce it.",
    ),
    export_map: bool = typer.Option(
        True,
        help="Export the original image with cells painted by classification label.",
    ),
    export_stats: bool = typer.Option(True, help="Export per fiber stat table."),
):
    """Run the SDH analysis and quantification on the image."""
    import os
    import urllib.request
    from .common_func import (
        is_gpu_availiable,
        load_cellpose,
        load_sdh_model,
        run_cellpose,
    )
    from .SDH_analysis import run_sdh_analysis
    import numpy as np
    from PIL import Image

    try:
        from imageio.v2 import imread
    except:
        from imageio import imread

    console.print(f"Welcome to the SDH Analysis CLI tools.", style="magenta")
    console.print(f"Running SDH Quantification on image : {image_path}", style="blue")
    start_time = time.time()

    if output_path is None:
        output_path = image_path.parents[0]
    else:
        Path(output_path).mkdir(parents=True, exist_ok=True)

    if is_gpu_availiable():
        console.print(f"GPU is available.", style="green")
    else:
        console.print(f"GPU is not available.", style="red")

    if model_path is None:
        console.print("No SDH model provided, will download latest one.", style="blue")
        model_path_abs = Path(os.path.abspath(__file__)).parents[0] / "model.h5"
        if not os.path.exists(model_path_abs):
            urllib.request.urlretrieve(
                "https://lbgi.fr/~meyer/SDH_models/model.h5",
                model_path_abs,
            )

        console.print(
            f"SDH Model have been downloaded and is located at {model_path_abs}",
            style="blue",
        )
        model_path = model_path_abs
    else:
        console.print(f"SDH Model used: {model_path}", style="blue")

    if cellpose_path is None:
        console.print(
            "No CellPose mask provided, will run CellPose during the analysis.",
            style="blue",
        )
        model_cellpose = load_cellpose()
        console.print("CellPose Model loaded !", style="blue")
    else:
        console.print(f"CellPose mask used: {cellpose_path}", style="blue")
    console.print("Reading image...", style="blue")

    image_ndarray_sdh = imread(image_path)
    console.print("Image loaded.", style="blue")

    if mask_path is not None:
        console.print(f"Reading binary mask: {mask_path} and masking...", style="blue")
        mask_ndarray = imread(mask_path)
        if np.unique(mask_ndarray).shape[0] != 2:
            console.print(
                "The mask image should be a binary image with only 2 values (0 and 1).",
                style="red",
            )
            raise ValueError
        if len(image_ndarray_sdh.shape) > 2:
            mask_ndarray = np.repeat(
                mask_ndarray.reshape(mask_ndarray.shape[0], mask_ndarray.shape[1], 1),
                image_ndarray_sdh.shape[2],
                axis=2,
            )
        image_ndarray_sdh = image_ndarray_sdh * mask_ndarray
        console.print(f"Masking done.", style="blue")

    console.print("Starting the Analysis. This may take a while...", style="blue")
    if cellpose_path is None:
        console.print("Running CellPose...", style="blue")
        mask_cellpose = run_cellpose(
            image_ndarray_sdh, model_cellpose, cellpose_diameter
        )
        mask_cellpose = mask_cellpose.astype(np.uint16)
        cellpose_mask_filename = image_path.stem + "_cellpose_mask.tiff"
        Image.fromarray(mask_cellpose).save(output_path / cellpose_mask_filename)
        console.print(
            f"CellPose mask saved as {output_path/cellpose_mask_filename}",
            style="green",
        )
    else:
        mask_cellpose = imread(cellpose_path)

    model_SDH = load_sdh_model(model_path)
    console.print("SDH Model loaded !", style="blue")

    if mask_path is not None:
        mask_ndarray = imread(mask_path)
        mask_cellpose = mask_cellpose * mask_ndarray

    result_df, full_label_map, df_cellpose_details = run_sdh_analysis(
        image_ndarray_sdh, model_SDH, mask_cellpose
    )
    console.print("Analysis completed ! ", style="green")
    table.add_column("Feature", justify="left", style="cyan")
    table.add_column("Raw Count", justify="center", style="magenta")
    table.add_column("Proportion (%)", justify="right", style="green")
    for index, row in result_df.iterrows():
        table.add_row(
            str(row[0]),
            str(row[1]),
            str(row[2]),
        )
    console.print(table)
    csv_name = image_path.stem + "_results.csv"
    result_df.to_csv(
        output_path / csv_name,
        index=False,
    )
    console.print(
        f"Table saved as a .csv file named {output_path/csv_name}", style="green"
    )
    if export_stats:
        cell_details_name = image_path.stem + "_cell_details.csv"
        df_cellpose_details.drop("image", axis=1).to_csv(
            output_path / cell_details_name,
            index=False,
        )
        console.print(
            f"Cell Table saved as a .csv file named {output_path/cell_details_name}",
            style="green",
        )
    label_map_name = image_path.stem + "_label_map.tiff"
    Image.fromarray(full_label_map).save(output_path / label_map_name)
    console.print(
        f"Labelled image saved as {output_path/label_map_name}", style="green"
    )
    painted_img_name = image_path.stem + "_painted.tiff"
    console.print("--- %s seconds ---" % (time.time() - start_time))


@app.command()
def he_analysis(
    image_path: Path = typer.Argument(
        ...,
        help="The HE image file path to analyse. If using single channel images, this will be used as cytoplasm image to run CellPose. Please use the --fluo-nuc option to indicate the path to the nuclei single image to run Stardist.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    mask_path: Path = typer.Option(
        None,
        help="The path to a binary mask to hide slide region during analysis. It needs to be of the same resolution as input image and only pixel marked as 1 will be analyzed.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    cellpose_path: Path = typer.Option(
        None,
        help="The pre-computed CellPose mask to use for analysis. Will run Cellpose if no path provided. Required as an image file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    stardist_path: Path = typer.Option(
        None,
        help="The pre-computed Stardist mask to use for analysis. Will run Stardist if no path provided. Required as an image file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    output_path: Path = typer.Option(
        None,
        help="The path to the folder to save the results. Will save in the same folder as input image if not specified.",
    ),
    cellpose_diameter: int = typer.Option(
        None,
        help="Approximative single cell diameter in pixel for CellPose detection. If not specified, Cellpose will try to deduce it.",
    ),
    nms_thresh: float = typer.Option(
        0.4, help="NMS Threshold for Stardist nuclei detection.", min=0, max=1
    ),
    prob_thresh: float = typer.Option(
        0.5, help="Probability Threshold for Stardist nuclei detection.", min=0.5, max=1
    ),
    eccentricity_thresh: float = typer.Option(
        0.75,
        help="Eccentricity threshold value for a nucleus to be considered as internalized during nuclei classification. When very close to 1 almost all nuclei are considered as internalized.",
        min=0,
        max=1,
    ),
    export_map: bool = typer.Option(
        True,
        help="Export the original image with cells painted by classification label.",
    ),
    export_stats: bool = typer.Option(
        True, help="Export per fiber and per nuclei stat table."
    ),
    fluo_nuc: Path = typer.Option(
        None,
        help="The path to single channel fluo image for nuclei.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
):
    """Run the HE analysis and quantification on the image."""
    from .common_func import (
        is_gpu_availiable,
        load_cellpose,
        load_stardist,
        run_cellpose,
        run_stardist,
    )
    from .HE_analysis import run_he_analysis
    import numpy as np
    from PIL import Image

    try:
        from imageio.v2 import imread
    except:
        from imageio import imread

    console.print(f"Welcome to the HE Analysis CLI tools.", style="magenta")
    console.print(f"Running HE Quantification on image : {image_path}", style="blue")
    start_time = time.time()

    if output_path is None:
        output_path = image_path.parents[0]
    else:
        Path(output_path).mkdir(parents=True, exist_ok=True)

    if is_gpu_availiable():
        console.print(f"GPU is available.", style="green")
    else:
        console.print(f"GPU is not available.", style="red")

    if cellpose_path is None:
        console.print(
            "No CellPose mask provided, will run CellPose during the analysis.",
            style="blue",
        )
        model_cellpose = load_cellpose()
        console.print("CellPose Model loaded !", style="blue")
    else:
        console.print(f"CellPose mask used: {cellpose_path}", style="blue")

    if stardist_path is None:
        console.print(
            "No Stardist mask provided, will run Stardist during the analysis.",
            style="blue",
        )
        if fluo_nuc is None:
            model_stardist = load_stardist(fluo=False)
        else:
            model_stardist = load_stardist(fluo=True)
        console.print("Stardist Model loaded !", style="blue")
    else:
        console.print(f"Stardist mask used: {stardist_path}", style="blue")

    console.print("Reading image...", style="blue")

    image_ndarray = imread(image_path)
    if fluo_nuc is not None:
        fluo_nuc_ndarray = imread(fluo_nuc)

    if mask_path is not None:
        console.print(f"Reading binary mask: {mask_path} and masking...", style="blue")
        mask_ndarray = imread(mask_path)
        if np.unique(mask_ndarray).shape[0] != 2:
            console.print(
                "The mask image should be a binary image with only 2 values (0 and 1).",
                style="red",
            )
            raise ValueError
        if len(image_ndarray.shape) > 2:
            mask_ndarray = np.repeat(
                mask_ndarray.reshape(mask_ndarray.shape[0], mask_ndarray.shape[1], 1),
                image_ndarray.shape[2],
                axis=2,
            )
        image_ndarray = image_ndarray * mask_ndarray
        if fluo_nuc is not None:
            fluo_nuc_ndarray = fluo_nuc_ndarray * mask_ndarray
        console.print(f"Masking done.", style="blue")
    console.print("Image loaded.", style="blue")
    console.print("Starting the Analysis. This may take a while...", style="blue")
    if cellpose_path is None:
        console.print("Running CellPose...", style="blue")
        mask_cellpose = run_cellpose(image_ndarray, model_cellpose, cellpose_diameter)
        mask_cellpose = mask_cellpose.astype(np.uint16)
        cellpose_mask_filename = image_path.stem + "_cellpose_mask.tiff"
        Image.fromarray(mask_cellpose).save(output_path / cellpose_mask_filename)
        console.print(
            f"CellPose mask saved as {output_path/cellpose_mask_filename}",
            style="green",
        )
    else:
        mask_cellpose = imread(cellpose_path)

    if stardist_path is None:
        console.print("Running Stardist...", style="blue")
        if fluo_nuc is not None:
            mask_stardist = run_stardist(
                fluo_nuc_ndarray, model_stardist, nms_thresh, prob_thresh
            )
        else:
            mask_stardist = run_stardist(
                image_ndarray, model_stardist, nms_thresh, prob_thresh
            )
        mask_stardist = mask_stardist.astype(np.uint16)
        stardist_mask_filename = image_path.stem + "_stardist_mask.tiff"
        Image.fromarray(mask_stardist).save(output_path / stardist_mask_filename)
        console.print(
            f"Stardist mask saved as {output_path/stardist_mask_filename}",
            style="green",
        )
    else:
        mask_stardist = imread(stardist_path)

    console.print("Calculating all nuclei eccentricity scores... !", style="blue")

    if mask_path is not None:
        mask_ndarray = imread(mask_path)
        mask_stardist = mask_stardist * mask_ndarray
        mask_cellpose = mask_cellpose * mask_ndarray

    result_df, full_label_map, df_nuc_analysis, all_nuc_df_stats = run_he_analysis(
        image_ndarray, mask_cellpose, mask_stardist, eccentricity_thresh
    )
    console.print("Analysis completed ! ", style="green")
    table.add_column("Feature", justify="left", style="cyan")
    table.add_column("Raw Count", justify="center", style="magenta")
    table.add_column("Proportion (%)", justify="right", style="green")
    for index, row in result_df.iterrows():
        table.add_row(
            str(row[0]),
            str(row[1]),
            str(row[2]),
        )
    console.print(table)
    csv_name = image_path.stem + "_results_summary.csv"
    cell_details_name = image_path.stem + "_cell_details.csv"
    nuc_details_name = image_path.stem + "_nuc_details.csv"
    result_df.to_csv(
        output_path / csv_name,
        index=False,
    )
    console.print(
        f"Summary Table saved as a .csv file named {output_path/csv_name}",
        style="green",
    )
    if export_stats:
        df_nuc_analysis.drop("image", axis=1).to_csv(
            output_path / cell_details_name,
            index=False,
        )
        console.print(
            f"Cell Table saved as a .csv file named {output_path/cell_details_name}",
            style="green",
        )
        all_nuc_df_stats.drop("image", axis=1).to_csv(
            output_path / nuc_details_name,
            index=False,
        )
        console.print(
            f"Nuclei Table saved as a .csv file named {output_path/nuc_details_name}",
            style="green",
        )
    label_map_name = image_path.stem + "_label_map.tiff"
    Image.fromarray(full_label_map).save(output_path / label_map_name)
    console.print(
        f"Labelled image saved as {output_path/label_map_name}", style="green"
    )
    painted_img_name = image_path.stem + "_painted.tiff"
    console.print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    app()
