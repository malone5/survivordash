<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">SurvivorDASH</h3>

  <p align="center">
    A data pipeline for the hit reality show Surivor
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

After going on a wild binge of Survivors seasons I was curious about the data an some insights that could
be derrived from it. So I looked into some survivor data sources and found an opportunity to sharpen my data engineering skills
and learn more about the seasons I thoughouly enjoyed.

Going into this project I have always dreaded non-portable and/or complicated development environments and
wanted to get my first exposure with Docker and ultimatly create a basic data ecosystem that could be portable and 
setup with minimal commands for anyone interested in using it.

Things I wanted to accomplish:
* Fetch and model multiple sources of survivor season data (Python)
* load it inot a warehouse-like environment (Postgres)
* explore the data in a BI-tool (Metabase)
* Create a workflow to quickly develop and manage environments (Docker)

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Docker](httpd://docker.com/)
* [Python](https://python.org/)
* [Pandas](https://pandas.pydata.org/)
* [Postgres](https://www.postgresql.org/)
* [Metabase](https://www.metabase.com/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites


* Docker


### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/malone5/survivordash.git
   cd survivordash
   ```
2. Create an ```.env``` file in the home directory. 
    ```sh
    touch .env
    ```
    ```sh
   POSTGRES_USER=<user>
   POSTGRES_PASSWORD=<pass>
   POSTGRES_DB=warehouse
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   MB_DB_DBNAME=metabase
   MB_EMAIL=dev@local.host
   MB_PASS=fakepass1
    ```
3. Start the continers
   ```sh
   make up
   ```

4. Run the pipeline (Make sure Metabase(localhost:4000) has completed installation)
   ```sh
   docker exec -it pipeline python /code/src/survivordash/run.py
   ```

5. Visit
   ```sh
   http://localhost:3000  [Metabase BI Tool]
   http://localhost:4000  [Postgres Adminer]
   ```
   MB_EMAIL and MB_PASS is what you will use to log into the metabase BI tool
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Thank you to trudorktimes.com for collecting survivor statistics and outcomes


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
