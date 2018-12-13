import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, timedelta
import subprocess
from requests import session

import argparse
import constants

USER = constants.GITHUB_ID
PASSWORD = constants.GITHUB_PASS
GITHUB_SESSION_URL = 'https://github.com/session'

def get_bio(s, profile_url, issue_url, issue_title):
	html_source = s.get(profile_url).text
	line = ''
	try:
		parsed_html = BeautifulSoup(html_source, 'html.parser')

		username_val = profile_url.split('/')[-1]
		print('username:', username_val)
		line = line + username_val + ', '

		print('issue_url:', issue_url)
		line = line + issue_url + ', '

		print('issue_title:', issue_title)
		line = line + issue_title + ', '

		fullname = parsed_html.find("span", class_="vcard-fullname")
		if fullname is not None:
			fullname_val = fullname.find(text=True, recursive=False)
			print('fullname:', fullname_val)
			if fullname_val is not None:
				line = line + fullname_val
		line = line + ', '

		email_li = parsed_html.find("li", {'itemprop':"email"}, class_="vcard-detail")
		if email_li is not None:
			email = email_li.find("a", class_="u-email")
			if email is not None:
				email_val = email.find(text=True, recursive=False)
				print('email: ', email_val)
				if email_val is not None:
					line = line + email_val
		line = line + ', '

		org_li = parsed_html.find("li", {'itemprop':"worksFor"}, class_="vcard-detail")
		if org_li is not None:
			org = org_li.find("span", class_="p-org")
			if org is not None:
				org_val = org.find(text=True, recursive=True)
				print('organisation:', org_val)
				if org_val is not None:
					line = line + org_val

		line = line + '\n'
		print()
	except Exception:
		traceback.print_exc()
	return line

def get_issuers_profile_urls(root_url):
	profile_urls = []
	try:
		req = Request(root_url , headers={'User-Agent': 'Mozilla/5.0'})
		html_source = urlopen(req).read()
		parsed_html = BeautifulSoup(html_source, 'html.parser')
		headers = parsed_html.find_all("div", class_="timeline-comment-header")
		for header in headers:
			author = header.find("a", class_="author")
			profile_urls.append("https://github.com" + author['href'])
	except urllib.error.URLError as e:
		print("Seems URL changed for: " + root_url)
		print(e)
	except Exception as e:
		print("Unknown Error: " + root_url)
		print(e)
	return profile_urls

def get_issue_title(root_url):
	try:
		req = Request(root_url , headers={'User-Agent': 'Mozilla/5.0'})
		html_source = urlopen(req).read()
		parsed_html = BeautifulSoup(html_source, 'html.parser')
		return parsed_html.find("span", class_="js-issue-title").text.strip()
	except urllib.error.URLError as e:
		print("Seems URL changed for: " + root_url)
		print(e)
	except Exception as e:
		print("Unknown Error: " + root_url)
		print(e)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--issue', default="https://github.com/gatech-csl/jes/issues/99")
	args = parser.parse_args()
	profile_urls = get_issuers_profile_urls(args.issue)
	issue_title = get_issue_title(args.issue)
	with open('email-list.csv','wb') as file:
		with session() as s:
			req = s.get(GITHUB_SESSION_URL).text
			html = BeautifulSoup(req, 'html.parser')
			token = html.find("input", {"name": "authenticity_token"}).attrs['value']
			com_val = html.find("input", {"name": "commit"}).attrs['value']

			login_data = {'login': USER,
						'password': PASSWORD,
						'commit' : com_val,
						'authenticity_token' : token}

			s.post(GITHUB_SESSION_URL, data = login_data)

			for profile_url in profile_urls:
				line = get_bio(s, profile_url, args.issue, issue_title)
				file.write(bytes(line, 'UTF-8'))

	file = open('email-list.csv')
	lines = file.readlines()
	lines.sort()
	lines_deduped = list(set(lines))

	with open('deduped-email-list.csv', 'w') as f:
		f.write('Username, IssueUrl, IssueTitle, Fullname, EmailAddress, Organisation\n')
		for line in lines_deduped:
			f.write("%s" % line)
	os.unlink('email-list.csv')
	os.rename('deduped-email-list.csv','email-list.csv')

if __name__ == '__main__':
  main()