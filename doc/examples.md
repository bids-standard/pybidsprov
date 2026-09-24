# Executable examples for PyBIDSProv

This is a collection examples for PyBIDSProv that you can actually run using the test data provided in the repository.

> [!WARNING] Be sure to create the `outputs/` directory before running the examples.
> ```shell
> mkdir outputs
> ```

## `bids_prov merge` examples

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

## Extract

In this example, we generate the sub-graph representing the provenance of the file identified with `bids::sub-01/anat/c1sub-01_T1w.nii` in the provenance of the [tests/test_data/provenance_ds01](/tests/test_data/provenance_ds01) dataset.

```shell
bids_prov extract -i tests/test_data/provenance_ds01.jsonld -n bids::sub-01/anat/c1sub-01_T1w.nii -o outputs/provenance_ds01_extract1.jsonld
```

The generated `outputs/provenance_ds01_extract1.jsonld` file should be equal to the [`tests/test_data/provenance_ds01_extract1.jsonld`](/tests/test_data/provenance_ds01_extract1.jsonld) file.

The corresponding image looks like:

![Provenance graph for the sub-01/anat/c1sub-01_T1w.nii file in the tests/test_data/provenance_ds01 dataset](/doc/assets/provenance_ds01_extract1.png)

You can compare it with the provenance of the whole dataset:

![Provenance graph for dataset tests/test_data/provenance_ds01](/doc/assets/prov-ds01_spm.png)

## Visualize

```shell
bids_prov visualize -i tests/test_data/provenance_ds02.jsonld -o outputs/provenance_ds02.png
```

The generated `outputs/prov-ds02.png` image file should look like this:

![Provenance graph for dataset tests/test_data/provenance_ds02](/doc/assets/prov-ds02.png)

```shell
bids_prov visualize -i tests/test_data/provenance_ds01_spm.jsonld -o outputs/provenance_ds01_spm.png
```

The generated `outputs/prov-ds01_spm.png` image file should look like this:

![Provenance graph for the prov-spm entity in dataset tests/test_data/provenance_ds01](/doc/assets/prov-ds01_spm.png)

