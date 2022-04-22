<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

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
    ```
3. Start the containers
   ```sh
   make up
   ```

4. Run the pipeline when Metabase is installed. This take 1-3 minutes after running "make up". A good way to see if Metabase is ready is to check localhost:3000 for a log-in screen.
   ```sh
   docker exec -it pipeline python /code/src/survivordash/run.py
   ```
   Once this process finished Metabase will be configured and loaded with survivor data.

5. Visit
   ```sh
   http://localhost:3000  [Metabase BI Tool]
   http://localhost:4000  [Postgres Adminer]
   ```
   Login to the Metabase dashboard with the credentials ```user=dev@local.host```   ```pass=zcYsPtaCys6vTytxEAUyz9sYz```
   
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Thank you to trudorktimes.com for collecting survivor statistics and outcomes


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
