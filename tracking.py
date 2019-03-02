#!/usr/bin/env python3
# USPS API Tracking
# Tested on Python 3.4.2 running on Debian 8.7
# https://github.com/LiterallyLarry/USPS-Tracking-Python
#
# You must provide your API key as 'api_key' before running this program! You can sign up for an API key here: https://www.usps.com/business/web-tools-apis/welcome.htm
# Modified by Seth Phillips

from urllib import request, parse
from xml.etree import ElementTree
import argparse, json, sys, os

USPS_API_URL = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2";

API_KEY = '941SIMPL7834'

if not API_KEY:
    sys.exit("Error: Could not find USPS API key");


def submit_track_id(track_id):
    xml = "<TrackRequest USERID=\"%s\">" % API_KEY;
    xml += "<TrackID ID=\"%s\"></TrackID>" % track_id;
    xml += "</TrackRequest>";
    target = "%s&%s" % (USPS_API_URL, parse.urlencode({"XML": xml}));
    request_obj = request.urlopen(target);
    result = request_obj.read();
    request_obj.close();
    return result;


def usps_track(track_id):
    track_xml = submit_track_id(track_id);
    # print(track_xml)
    track_result = ElementTree.ElementTree(ElementTree.fromstring(track_xml));

    summary = track_result.findall('.//TrackSummary')
    if summary:
        # print('summary: %s' % summary[0].text)
        return summary[0].text

    error = track_result.findall('.//Description')
    if error:
        # print('error: %s' % error[0].text)
        return error[0].text
        # print('\n\nsummary: %s' % summary.text);
        # print('\n\nerror: %s' % error.text);

        # if summary is None:
        #     print('Error in XML!');
        #     print(track_xml);
        # else:
        #     print('\n\nmsg: %s' % summary.text);


if __name__ == "__main__":
    usps_track()
