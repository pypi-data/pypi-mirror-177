# PyCLI Utilities
- As name suggests, CLI Utilities is the python package containing various CLI utilities to perform various operations on different types on files.

- Every utility has its own sets of configuration options which you can explore by specifying -h or --help after utility's command. 

- This repository is open for everyone. Please feel free to suggest / add more CLI tools to this repository.

# Available Utilities

#### CSV Validator

```console
$ csv-validate file [options]
```

This utility is designed to validate CSV file by validating that each row of the CSV file has same number of columns. 


#### CSV NULL Cleaner

```console
$ csv-remove-nulls file [options]
```

This utility is designed to remove NULL characters (ascii code: 0) from the CSV file.
This utility basically does the two things:

- Replaces the NULL's with empty string
- Removes the empty or only separator contained rows (if any)


#### CSV Column Remover

```console
$ csv-remove-column file column_number [options]
```

This utility is designed to remove specific column from the CSV file.


#### CSV Column Shifter

```console
$ csv-shift-column file from_location to_location [options]
```

This utility is designed to shift particular column within the CSV file.


#### CSV Splitter

```console
$ csv-split file number_of_records [options]
```

This utility is designed to split the large CSV file into multiple CSV files by number of records.