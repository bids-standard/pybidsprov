# pybidsprov

PyBIDSProv is a Python library containing utility tools to work with provenance inside BIDS datasets.

For more information about BIDS, visit https://bids.neuroimaging.io.

## Installation

PyBIDSProv is most easily installed from pip. To install the latest official release:

```shell
pip install pybidsprov
```

## Usage

PyBIDSProv consists in a main command line tool `bids_prov`, giving access to several sub commands:

- `merge`: Aggregates all provenance metadata available in a BIDS dataset to generate a provenance graph inside a single JSON-LD file.
- `extract`: Isolates the provenance graph of a given prov:Entity (e.g. a file, dataset or another prov:Entity) and generates a provenance graph inside a JSON-LD file.
- `check`: Perform a sanity check on a proveance graph contained in a JSON-LD file.
- `visualize`: Generates an image (*graphviz* graph) representing a proveance graph contained in a JSON-LD file.

### `bids_prov merge` - Aggregate the provenance metadata of a BIDS dataset

> [!TIP]
> Find executable examples for this command inside the [doc/examples.md](/doc/examples.md#bids_prov-merge-examples) file.

```shell
bids_prov merge -h
	usage: bids_prov merge [-h] [--dataset DATASET] [--derivative] --output_file OUTPUT_FILE [--entity ENTITY]

	options:
	  -h, --help            show this help message and exit
	  --dataset DATASET, -d DATASET
	                        The path to the input BIDS dataset. Do not provide this argument if the dataset is in the current directory.
	  --derivative          Set this option to specify the dataset is a BIDS derivative dataset.
	  --output_file OUTPUT_FILE, -o OUTPUT_FILE
	                        Name for the output JSON-LD file containing the provenance graph for the input dataset.
	  --entity ENTITY, -e ENTITY
	                        `prov-` BIDS entity for which to extract the metadata. E.g.: for `prov-spm`, provide "-e spm"
```

Run this command from inside a BIDS dataset containing provenance metadata inside e.g. `dataset_description.json`, `prov/` files or JSON sidecars.

### `bids_prov extract` - Isolate the provenance of a given prov:Entity

> [!TIP]
> Find executable examples for this command inside the [doc/examples.md](/doc/examples.md#bids_prov-extract-examples) file.

```shell
bids_prov extract -h
	usage: bids_prov extract [-h] --input_file INPUT_FILE --node_id NODE_ID --output_file OUTPUT_FILE

	options:
	  -h, --help            show this help message and exit
	  --input_file INPUT_FILE, -i INPUT_FILE
	                        Provenance graph as a JSON-LD file.
	  --node_id NODE_ID, -n NODE_ID
	                        Identifier for the prov:Entity.
	  --output_file OUTPUT_FILE, -o OUTPUT_FILE
	                        Name for the output JSON-LD file containing the subgraph.
```

Knowing the identifier of a prov:Entity of interest (a file, dataset or another prov:Entity) inside an input JSON-LD file representing a provenance graph, you are able to generate a sub-graph that includes the nodes involved in the provenance of this prov:Entity only.

### `bids_prov check` - Perform a sanity check on a provenance graph

> [!TIP]
> Find executable examples for this command inside the [doc/examples.md](/doc/examples.md#bids_prov-check-examples) file.

```shell
bids_prov check -h
	usage: bids_prov check [-h] (-i INPUT_FILE | -d INPUT_DIRECTORY) [-r] [-v]

	options:
	  -h, --help            show this help message and exit
	  -i INPUT_FILE, --input_file INPUT_FILE
	                        Input JSON-LD file.
	  -d INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
	                        Input directory containing JSON-LD files.
	  -r, --recursive       Search recursively for files in the input directory.
	  -v, --verbose         verbose mode
```

Pass a JSON-LD file or a directory containing JSON-LD files to perform sanity checks on the corresponding provenance graphs.
This will list:
* All prov:Activities that did not use any prov:Entity.
* All prov:Activity that did not generate any prov:Entity.

### `bids_prov visualize` - Visualize a provenance graph as an image

> [!TIP]
> Find executable examples for this command inside the [doc/examples.md](/doc/examples.md#bids_prov-visualize-examples) file.

```shell
bids_prov visualize -h
	usage: bids_prov visualize [-h] --input_file INPUT_FILE [--output_file OUTPUT_FILE] [--detailed]

	options:
	  -h, --help            show this help message and exit
	  --input_file INPUT_FILE, -i INPUT_FILE
	                        Input BIDS-Prov data as a JSON-LD file.
	  --output_file OUTPUT_FILE, -o OUTPUT_FILE
	                        Name for the output PNG file showing the `graphviz` graph. If not provided, the input name
	                        stem will be used for the output file name.
	  --detailed, -d        Set this option to write a detailed version of the graph.
```

This allows to generate a PNG file containing a Graphviz graph illustrating what is inside a JSON-LD file.

## Development and testing

After cloning the repository, install the `bids_prov` package with [uv](https://docs.astral.sh/uv/):

```shell
uv venv
source .venv/bin/activate
uv sync
```

You are now able to run `bids_prov` and ready to develop.

```shell
bids_prov -h
	usage: bids_prov [-h] {merge,extract,check,visualize} ...

	One command line tool for all BIDS-Prov executables.

	positional arguments:
	  {merge,extract,check,visualize}
	                        One of these subcommands is required.
	    merge               Merge all provenance metadata from a BIDS dataset into one JSON-LD BIDS-Prov file.
	    extract             Generate the provenance graph of a given prov:Entity in a BIDS dataset from a JSON-LD BIDS-Prov file.
	    check               Sanity check on a JSON-LD BIDS-Prov file.
	    visualize           Generate a `graphviz` graph as PNG file from a JSON-LD BIDS-Prov file.

	options:
	  -h, --help            show this help message and exit
```

PyBIDSProv uses [pytest](https://docs.pytest.org/en/stable/) for testing. Install the test suite with:

```shell
uv sync --group tests
```

You are now able to run tests and coverage:

```shell
python -m pytest --cov=./
```
