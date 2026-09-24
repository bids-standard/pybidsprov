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

> [!TIP] Find executable examples for this command inside the [docs/examples.md](docs/examples.md) file.

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

Let's assume the following BIDS dataset.
```
.
├── dataset_description.json 🔵
├── prov
│   ├── prov-proc1_act.json 🔵
│   ├── prov-proc1_env.json 🔵
│   ├── prov-proc1_io.json 🔵
│   ├── prov-proc1_soft.json 🔵
│   ├── prov-proc2_act.json 🟠
│   ├── prov-proc2_env.json 🟠
│   ├── prov-proc2_io.json 🟠
│   └── prov-proc2_soft.json 🟠
├── README.md
└── sub-01
    ├── anat
    │   ├── sub-01_T1w.json 🔵
    │   └── sub-01_T1w.nii
    └── func
        ├── sub-01_task-tonecounting_bold.json 🔵
        └── sub-01_task-tonecounting_bold.nii
```

```shell
# Merge provenance metadata from files marked with 🟠 or 🔵 inside a single JSON-LD file
bids_prov merge -o prov/prov-proc1.jsonld

# You can focus on a BIDS entity
# The following command merges provenance metadata from files marked with 🔵
bids_prov merge -o prov/prov-proc1.jsonld -e proc1

# You can specify the dataset location too (it is the current directory by default)
bids_prov merge -o prov/prov-proc1.jsonld -d path/to/another/dataset

# Use the --derivative option when working with a BIDS derivative dataset
bids_prov merge -o prov/prov-proc1.jsonld --derivative
```

The output JSON-LD file looks like:

```JSON
{
  "@context": "https://bids-specification--2099.org.readthedocs.build/en/2099/provenance-context.json",
  "Records": {
    "Software": [
      {
        "Id": "bids::prov#spm-fa0baf93",
        "AlternativeIdentifier": [
          "RRID:SCR_007037"
        ],
        "Label": "SPM",
        "Version": "SPM12r7771"
      }
    ],
    "Activities": [
      {
        "Id": "bids::prov#preprocessing-yBHdvts7",
        "Label": "Preprocessing",
        "AssociatedWith": [
          "bids::prov#spm-fa0baf93"
        ]
 	  }
    ]
    ...
  }
}
```

### `bids_prov extract` - Isolate the provenance of a given prov:Entity

> [!TIP] Find executable examples for this command inside the [docs/examples.md](docs/examples.md) file.

```shell
bids_prov merge -h
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

```shell
bids_prov extract -i prov/prov-proc1.jsonld -n bids::sub-01/anat/sub-01_T1w.nii -o prov/prov-sub01T1w.jsonld
```

### `bids_prov check` - Perform a sanity check on a provenance graph

> [!TIP] Find executable examples for this command inside the [docs/examples.md](docs/examples.md) file.


### `bids_prov visualize` - Visualize a provenance graph as an image

> [!TIP] Find executable examples for this command inside the [docs/examples.md](docs/examples.md) file.


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
