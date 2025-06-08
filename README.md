# WordPressPostCreator

Creates multiple WordPress posts from a single text file

[![License](https://img.shields.io/github/license/hocnat/WordPressPostCreator)](https://github.com/hocnat/WordPressPostCreator/blob/main/LICENSE)

## Motivation

I run a blog where I publish a kind of diary about my travels. During a trip, in the evenings, I quickly jot down what we experienced throughout the day in a notes app on my phone. When I get home from the trip, the manual process of turning this into a series of blog posts was incredibly tedious and repetitive. For each entry, I had to:

* Create a new post.
* Copy and paste the title.
* Copy and paste the content.
* Assign the correct category.
* Set the correct publication date.
* Save the post as a draft.

Repeating these steps dozens of time is a huge waste of time. Therefore, I wanted to automate these steps.

This script automates that entire monotonous process. It handles the "scaffolding" work, allowing me to focus on the creative part:

* Refining the text.
* Formatting content with paragraphs and subheadings.
* Adding featured images and galleries.
* Adding tags.

## Usage

Follow these steps to set up and run the script.

### Prerequisites

Before you begin, ensure you have the following set up.

#### WordPress application password

This script authenticates with your WordPress site using a secure application password.

1.  Log in to your WordPress dashboard.
2.  Go to `Users` | `Profile`.
3.  Scroll down to the `Application Passwords` section.
4.  Enter a name for the new password (e.g., `create_posts.py`) and click `Add New Application Password`.
5.  **Important:** Copy the generated password (e.g., `abcd efgh ijkl mnop qrst uvwx`) immediately. You will not be able to see it again.

#### Python and dependencies

The script requires Python to run.

1. **Install Python**: If you don't have it already, download and install Python from the [official website](https://www.python.org/downloads/). During installation on Windows, it's highly recommended to check the box `Add Python to PATH`.

2. **Install required package**: This script depends on the `requests` library. You can install it using `pip`, Python's package installer. Open your terminal or command prompt and run:
   ```shell
   pip install requests
   ```

### Get the code

Clone this repository to your local machine using the following command:

```shell
git clone https://github.com/hocnat/WordPressPostCreator.git
cd WordPressPostCreator
```

### Configure the script

Before running the script, you need to configure it with your site's details.

Open the `create_posts.py` file in a text editor and update the constants at the top of the file:

```python
WP_URL = "https://your-domain.com"       # The URL of your WordPress site
WP_USERNAME = "your_wp_username"         # Your WordPress username
POST_SPLIT_REGEX = r'(?=^day \d+:)'      # Regex to detect the start of a new post
POST_TIME_STR = "22:00"                  # The fixed time for the posts
```

### Run the script

Execute the script from your terminal by providing the required parameters. The script will then prompt you to securely enter your application password.

**Example command:**

```shell
python create_posts.py --category-path "Travel > Sweden > Sweden 2025" --file "sweden2025.txt" --start-date "2025-06-07"
```

After you run this command, you will be prompted:
`Please enter the application password for user 'your_wp_username':`

Enter the application password you generated earlier. It will not be visible as you type.

#### Parameters

*   `--category-path` **(Required)**: The full category hierarchy for the posts.
    *   Use `>` as a separator (e.g., `"Parent > Child > Grandchild"`).
    *   The script will automatically create any categories in the path that do not already exist.
*   `--file` **(Required)**: The path to the input text file containing your content.
*   `--start-date` **(Required)**: The publication date for the very first post in `YYYY-MM-DD` format.
    *   Subsequent posts will have their date automatically incremented by one day.

## Used tools

* [Python](https://www.python.org/) - Python Software Foundation - *Python Software Foundation License*
  * The core programming language for the script.
* [Requests](https://requests.readthedocs.io/en/latest/) - Python Software Foundation - *Apache 2.0 License*
  * HTTP library used for making API calls to WordPress.
* [WordPress](https://wordpress.org/) - WordPress Foundation - *GPLv2 (or later)*
  * The script interacts with WordPress via its built-in REST API.
* [Gemini](https://gemini.google.com) - Google
  * Used as a development assistant for creating the script and writing documentation.

## License

[MIT License](https://github.com/hocnat/WordPressPostCreator/blob/main/LICENSE) Copyright 2025 © [hocnat](https://github.com/hocnat)