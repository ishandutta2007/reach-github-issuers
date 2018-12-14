# reach-github-issuers

This is a repo which collects mail id of all forkers of a repo and send them a specific mail.

### To Setup:

On how to setup gmail API follow [this](https://github.com/shankarj67/python-gmail-api/blob/563c7bf722c69be4fed2204e2829d0ab843d8729/README.md#install)

### To run:

1. `python3 github-issuers-crawler.py --issue ISSUE_FULL_URL`

2. The above script will create email-list.csv with all issue collaborators' details.

3. Modify the templates `help_request.html` as per need. If you need to rename or recreate new html template feel free to do so, just make sure you update name of it in `send_main.py`(as of now hardcoded)

4. `python3 send_mail.py`

### Support:

If you want the good work to continue please support us on

* [PAYPAL](https://www.paypal.me/ishandutta2007)
* [BITCOIN ADDRESS: 3LZazKXG18Hxa3LLNAeKYZNtLzCxpv1LyD](https://www.coinbase.com/join/5a8e4a045b02c403bc3a9c0c)
