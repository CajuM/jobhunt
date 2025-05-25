# Job Hunting Scripts

These scripts are used to scrap GitHub for info on organizations.
In the end you will be left with a TSV file that contains the name of the organization, it's URL, it's declared location and the number of stars of its select repositories.
What I did with that TSV was to select all organizations with a URL and at least one repository with over 1000 stars.

The `get_all_orgs.sh` script does what the name suggests, it fetches a list of all the organizations on GitHub. It takes no arguments, does not read from `stdin` and its output goes to `stdout`. A full list can be found in `gh-orgs.txt`.

The `get_orgs_tsv.py` script scrapes the mentioned data for each organization in `stdin` and outputs the TSV to `stdout`. It takes one argument, the number of subprocesses. Due to GitHub's present throttling policy, this value should be set to 29.

The `sorry.sh` script is called after each batch of URL's is fetched by `get_orgs_tsv.py`. At this point, the script is expect to be throttled, so the user must edit this file such that his public IP is reset to a new value. In the case of my ISP, bringing the interface up and down on my home router is sufficient to get a new DHCP lease.

Several sample results are provided `gh-orgs.txt` that contains a largely complete list of all the organizations on GitHub. `gh-orgs.tsv` that contains the scrapped data for all organizations on GitHub. And `gh-orgs-gtek.tsv` that contains only the organizations in `gh-orgs.tsv` that have at least one repository with over 1000 stars and a URL.
