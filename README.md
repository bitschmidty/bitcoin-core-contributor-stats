# Bitcoin Core Contributor Stats

Create HTML-formatted contributor stats on the [Bitcoin github
repo](https://github.com/bitcoin/bitcoin). Based on
[bitcoin-core-stats](https://github.com/jnewbery/bitcoin-core-stats) but using a
different data source and pared down features.

## Usage

- Clone the [github-metadata-backup-bitcoin-bitcoin](https://github.com/bitcoin-data/github-metadata-backup-bitcoin-bitcoin),
  pull the latest master, and set the `GH_META_DIR` parameter in
  `contributor-stats.py`.
- Set the `user` (GitHub handle) and `year` (year to filter data) variables in `contributor-stats.py`
- Run `contributor-stats.py > your-output-file.html` to generate the HTML summary report.
