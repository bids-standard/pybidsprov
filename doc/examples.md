# Executable examples for PyBIDSProv

This is a collection examples for PyBIDSProv that you can actually run using the test data provided in the repository.

> [!WARNING]
>
> Be sure to create the `outputs/` directory before running the examples.
> ```shell
> mkdir outputs
> ```

## `bids_prov merge` examples

### Theoretical example

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

### Merge all provenance metadata

In this example, we merge the provenance metadata contained in the [tests/test_data/provenance_ds02](/tests/test_data/provenance_ds02) dataset.

```shell
bids_prov merge -d tests/test_data/provenance_ds02 -o outputs/provenance_ds02.jsonld
```

The generated `outputs/provenance_ds02.jsonld` file should be equal to the [`tests/test_data/provenance_ds02.jsonld`](/tests/test_data/provenance_ds02.jsonld) file.

### Merge provenance metadata for a given `prov-` entity

In this example, we merge the provenance metadata corresponding to the `prov-spm` BIDS entity contained in the [tests/test_data/provenance_ds01](/tests/test_data/provenance_ds01) dataset.

```shell
bids_prov merge -d tests/test_data/provenance_ds01 -o outputs/provenance_ds01_spm.jsonld -e spm
```

The generated `outputs/provenance_ds01_spm.jsonld` file should be equal to the [`tests/test_data/provenance_ds01_spm.jsonld`](/tests/test_data/provenance_ds01_spm.jsonld) file.

## `bids_prov extract` examples

In this example, we generate the sub-graph representing the provenance of the file identified with `bids::sub-01/anat/c1sub-01_T1w.nii` in the provenance of the [tests/test_data/provenance_ds01](/tests/test_data/provenance_ds01) dataset.

```shell
bids_prov extract -i tests/test_data/provenance_ds01.jsonld -n bids::sub-01/anat/c1sub-01_T1w.nii -o outputs/provenance_ds01_extract1.jsonld
```

The generated `outputs/provenance_ds01_extract1.jsonld` file should be equal to the [`tests/test_data/provenance_ds01_extract1.jsonld`](/tests/test_data/provenance_ds01_extract1.jsonld) file.

The corresponding graph looks like:

![Provenance graph for the sub-01/anat/c1sub-01_T1w.nii file in the tests/test_data/provenance_ds01 dataset](/doc/assets/provenance_ds01_extract1.png)

You can compare it with the provenance of the whole dataset:

![Provenance graph for dataset tests/test_data/provenance_ds01](/doc/assets/provenance_ds01.png)

## `bids_prov check` examples

In this example, we check the graph contained in the [tests/test_data/provenance_ds01.jsonld](/tests/test_data/provenance_ds01.jsonld) file:

```shell
bids_prov check -i tests/test_data/provenance_ds01.jsonld
	INFO:bids_prov.check:All prov:Activities that did not use any prov:Entity : 0
	INFO:bids_prov.check:[]
	INFO:bids_prov.check:All prov:Activity that did not generated any prov:Entity : 1
	INFO:bids_prov.check:['<bids::prov#preprocessing-yBHdvts7>']
```

## `bids_prov visualize` examples

```shell
bids_prov visualize -i tests/test_data/provenance_ds02.jsonld -o outputs/provenance_ds02.png
```

The generated `outputs/prov-ds02.png` image file should look like this:

![Provenance graph for dataset tests/test_data/provenance_ds02](/doc/assets/provenance_ds02.png)

```shell
bids_prov visualize -i tests/test_data/provenance_ds01_spm.jsonld -o outputs/provenance_ds01_spm.png
```

The generated `outputs/prov-ds01_spm.png` image file should look like this:

![Provenance graph for the prov-spm entity in dataset tests/test_data/provenance_ds01](/doc/assets/provenance_ds01_spm.png)
