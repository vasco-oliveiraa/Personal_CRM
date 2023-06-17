# Sau - Your Personal CRM

## Large Files with DVC

This repository uses DVC (Data Version Control) to manage large files efficiently. DVC allows us to track and version large files separately from the Git repository.

When you clone this repository, you will need to retrieve the large files that are tracked by DVC. Please follow the steps below after cloning:

1. Install DVC by following the installation instructions provided on the official DVC website (https://dvc.org/).

2. Run the following command to retrieve the large files:

`dvc pull`

This command will download the necessary large files from the remote storage location or the local DVC cache.

3. Once the large files are downloaded, you can use them within the project.

Please note that the large files themselves are not stored in the Git repository. Instead, DVC stores only the metadata and pointers to these files. This approach allows for efficient storage, versioning, and collaboration with large datasets.

If you have any questions or issues regarding the large files or DVC usage, please refer to the DVC documentation or reach out to us for assistance.

 
