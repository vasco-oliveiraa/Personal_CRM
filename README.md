# Sau - Nurture relationships effortlessly

Sau is an application designed to help individuals keep in touch with those they care about and support them in strengthening their relationships, especially with people they don't interact with regularly. The name "Sau" is derived from "Saudade," a Portuguese word that signifies a melancholic longing or yearning.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
Sau aims to address the challenge of maintaining meaningful connections with friends and loved ones, even when life gets busy or physical distance separates us. It caters to a target audience primarily consisting of 25 to 35-year-olds who value strong and healthy relationships. The application particularly supports individuals living outside their home country, enabling them to keep close ties with their loved ones far away.

## Features
- **Conversation Starter:** Sau includes an innovative Conversation Starter feature. When the application detects a significant gap in interactions with a particular contact, longer than the desired frequency of interaction, it scans the contact's interests and analyses recent news articles. Based on this analysis, Sau generates a personalized message suggesting a conversation topic related to an interesting article, tailored to the contact's interests.

## Installation
To reproduce Sau on your local machine, please follow these steps:
1. Adjust the environment variables in the .env file to match your configuration.
2. Run the `DatabaseSetup.py` script to set up the MySQL database.
3. Launch the application by running `streamlit run App.py`.

## Usage
Upon running the application, you will be presented with an intuitive user interface. Sau assists you in managing your contacts and interactions effectively. It automatically identifies contacts with whom you have had minimal recent interaction and generates conversation starters to initiate engaging discussions. Simply select a contact, review the suggested message, and send it to rekindle the conversation.

## Contributing
We welcome contributions and ideas from the community! If you have any suggestions, feature requests, or bug reports, please reach out to us. You can contribute to Sau by submitting pull requests or contacting us with your ideas for further improvement. Let's work together to make Sau even better!

## License
[Specify the license under which your project is released. If you're not sure which license to use, you can refer to the Open Source Initiative (https://opensource.org/licenses) for more information and guidance.]

## Contact
For any questions, suggestions, or support, please feel free to reach out to us at [provide your contact email or any relevant communication channel].

## Acknowledgements
We would like to express our gratitude to the following individuals and resources that have contributed to the development of Sau:
- [List any libraries, frameworks, or resources that you utilized]
- [Acknowledge any individuals or communities that provided valuable feedback or support]

## Large Files with DVC

This repository uses DVC (Data Version Control) to manage large files efficiently. DVC allows us to track and version large files separately from the Git repository.

When you clone this repository, you will need to retrieve the large files that are tracked by DVC. Please follow the steps below after cloning:

1. Install DVC by following the installation instructions provided on the official DVC website (https://dvc.org/).

2. Run the following command to retrieve the large files:
   
   `dvc pull`
   This command will download the necessary large files from the remote storage location or the local DVC cache.

4. Once the large files are downloaded, you can use them within the project.

Please note that the large files themselves are not stored in the Git repository. Instead, DVC stores only the metadata and pointers to these files. This approach allows for efficient storage, versioning, and collaboration with large datasets.

If you have any questions or issues regarding the large files or DVC usage, please refer to the DVC documentation or reach out to us for assistance.

 
