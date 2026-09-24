# Executable examples for PyBIDSProv

This is a collection examples for PyBIDSProv that you can actually run using the test data provided in the repository.

## Merge

```shell
mkdir outputs
bids_prov merge -d tests/test_data/provenance_ds02 -o outputs/prov-ds02.jsonld
```

The generated `outputs/prov-ds02.jsonld` file should be equal to the `tests/test_data/provenance_ds02.jsonld` file.

## 
