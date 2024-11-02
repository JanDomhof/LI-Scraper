# Graduate Entrepreneur Scraper Manual

![logo](https://cdn.prod.website-files.com/6500a75467c491094354b2ad/6501e1134e01a1ed893f0552_Graduate-Entrepreneur-Logo%204-p-500.png)

## Contents

0. [Intro](#intro)
1. [Getting started](#getting-started)
2. [What to run](#what-to-run)
3. [Code structure](#code-structure)
4. [Recurring problems (and how to fix them)](#recurring-problems-and-how-to-fix-them)
5. [Future recommendations](#future-recommendations)

## Intro

This scraper is intended to scrape LinkedIn profiles that match certain criteria, assign them to a certain team member, and then save them to the Graduate Entrepreneur database. One of the criteria is that the profiles must have studied at either the TU Delft, Erasmus University, or Erasmus MC. Therefore, this is our starting point. We scrape all known pages corresponding to the different faculties of the universities.

Let me give an example. On the [alumni section of the TU Delft LinkedIn page](https://www.linkedin.com/school/tudelft/people/), we see a lot of profiles from students and alumni. We want to find the profiles in this list that are most likely to be startup founders. Since a LinkedIn page will only load up to 1000 profiles, we cannot simply scroll down and save every profile (125.583 for the TU Delft page). By filtering on title keywords and admission/graduation years can select segments of this pool to find as many of the interesting profiles (i.e., needles in the haystack) as possible.

## Getting started

First, we need to clone this repository. For simplicity:

```
git clone [add github repo link]
```

Once cloned, we can continue to create and activate our virtual environment. **For MacOS**:

```
python3 -m venv venv
source ./venv/bin/activate
```

And **for Windows**:

```
python -m venv venv
.\venv\Scripts\activate.bat
```

To install the requirements, which are saved in the requirements.txt file, use:

```
pip install -r requirements.txt
```

If the above does not work, or there are some other modules to install, simply do so by running the program a bunch of times and installing whatever it prompts you that is still missing, until it runs successfully. Make sure to update the requirements.txt file with these modules ;)

To be able to run this software, you need a `.env` file that should hold credentials for LinkedIn, Edda, and their database. See the format for this `.env` file here below. Check this with your contact at Graduate Entrepreneur, they should be able to provide it to you if you are going to be in charge of this repository.

```
LI_USERNAME =
LI_PASSWORD =
EDDA_USERNAME =
EDDA_PASSWORD =
DB_USERNAME =
DB_PASSWORD =
SSL_LOCATION =
```

The last environment variable, `SSL_LOCATION`, is the location where you have saved the database ssl certificate, which Graduate Entrepreneur should also provide to you (download from Microsoft Azure).

## What to run

We run the `main.py` file, which is located in the root folder. After booting up, the scraper should start to do its job and nothing else needs to be done.

**Note:** keep the window with the Chrome browser open, as if you do not, it will stop running after some time.

## Code structure

Let me explain how the code works and how it is structured. Let's first go over the helper files:

- `bd.py` contains the database logic including connection setup and queries.
- `edda.py` contains logic on how to fetch data from edda. However, this is used in the other 2 scraper files, and not used for LinkedIn (while it is an interesting nice-to-have and something I included in the [Future recommendations section](#future-recommendations)).
- `resources.py` contains some helper classes that make life easier. The `Selector` class is the object that is used to select web elements on the page. The `UNI` class is a small object, that does not take up a lot of memory, so we can quickly create one for each page. Then, with each iteration, we create the larger UNIPage. The other classes contain `Selector`s with the corresponding XPATHs, which we can easily access from other parts of the code.
- `test.py` is just a simple test file I used to run and test small pieces of code.

Then the `main.py` file. This is obviously the file to run when booting up. The code has some comments and should be easy enough to read, so quickly: it sets up the driver, creates the uni pages, then runs the scraper for each of these pages, and finally creates and saves the report.

Now the interesting part: the `page.py` file. It contains 4 classes:

1. `BasePage`. This is the base class which contains all the scraper logic. The logic is implemented with the `selenium` framework, and so all the functions are built on top of that for ease of use. All other classes inherit from this one.
2. `LoginPage`. This class is used for logging into LinkedIn. This is separated from the rest for organizational purposes.
3. `UNIPage`. This is the class with all the logic for actually scraping the LinkedIn pages. Basically, it contains everything from creating the URLs with the correct keywords to scrolling down the page, extracting the information from the web elements, creating the profiles, checking whether they are potentially startup founders, and calling to insert them into the database. It is pretty well documented so I trust that you will find it easy enough to understand.
4. `BigUNIPage`. This class is meant for pages with more than 1000 results. In this case, we would need to also filter on admission/graduation years. This inherits everything from `UNIPage`, but overwrites the `create_urls()` function to also include the admission and graduation year filter.

This should give you a starting point for the codebase. I am sure there are more optimal ways to do this, so I am sure future iterations will be better and better.

## Recurring problems (and how to fix them)

There are some issues that might stop the program and lead to errors. When debugging, here are some common errors and things I usually check first.

### Chromedriver version mismatch.

This is a simple one. Chrome will automatically keep updating its installed version, and therefore we must do the same when initializing the drivers. In `main.py`, simply replace the `...` here below with the correct version number:

```
driver = uc.Chrome(options=options,version_main=...)
```

### XPATH label changes

To make it as hard as possible to build scrapers, LinkedIn tries to change up its website ever so often to try and break the scraper codes. It usually becomes clear from the error message where the error comes from, so try to find exactly what is going wrong by comparing the XPATH labels with the ones in the website inspector in your browser. If some label breaks often, try to find another method to select that certain div (e.g., by selecting its more stable parent element).

### Database timeout

Sometimes after some time the database connection breaks. I've built in points where this connection is reactivated when this happens, but I might still have missed some parts where this might occur. Make sure to reopen the connection whenever it breaks. I suppose it is expected that a connection might not last for hours/days on end.

## Future recommendations

Here I list some things that still need to be fixed or improved:

1. Optimizing filters such that the # of profiles for each filter are near the limit (1000/2500).
2. Use a LinkedIn premium account to increase the amount of loadable profiles per page (from 1000 to 2500).
3. Incorporating Erasmus MC??!!
4. Incorporating Edda correctly by fetching founder names and cross-checking with our scraped profiles.
5. Improving the database structure of linkedin_profiles.
6. Reporting issues with `Count on page` column being the same for each year segment.
7. Improving/reiterating the structure of the codebase.
8. Improving the structure of all 2 scrapers combined.
