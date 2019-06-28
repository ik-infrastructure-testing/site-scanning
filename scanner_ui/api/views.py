from django.shortcuts import render
from django.conf import settings
import boto3
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import DomainsSerializer
import os
import json
from collections import defaultdict

# Create your views here.

def getScanFromS3(path):
	s3_resource = boto3.resource('s3')
	response = s3_resource.Object(settings.BUCKETNAME,path).get()
	return {'body': response['Body'].read(), 'lastmodified': response['LastModified']}

# If scantype is None, then we want all the scans.
def getScantype(scantype=None):
	scans = []
	for f in getMetadatafromS3():
		if not re.search('\.json$', f.key):
			continue
		s3scantype = os.path.dirname(f.key)
		if scantype == None or s3scantype == scantype:
			scandomain = os.path.basename(os.path.splitext(f.key)[0])
			scandata = getScanFromS3(f.key)
			json_data = json.loads(scandata['body'])
			lastmodified = scandata['lastmodified']
			scans.append({"domain": scandomain, "scantype": s3scantype, "path": f.key, "lastmodified": lastmodified, "data": json_data})
	return scans

# If domain is None, then we want all the domains.
def getDomain(domain=None):
	scans = []
	for f in getMetadatafromS3():
		scandomain = os.path.basename(os.path.splitext(f.key)[0])
		if domain == None or scandomain == domain:
			scantype = os.path.dirname(f.key)
			scandata = getScanFromS3(f.key)
			json_data = json.loads(scandata['body'])
			lastmodified = scandata['lastmodified']
			scans.append({"domain": scandomain, "scantype": scantype, "path": f.key, "lastmodified": lastmodified, "data": json_data})
	return scans

def getMetadatafromS3():
	s3_resource = boto3.resource('s3')
	return s3_resource.Bucket(settings.BUCKETNAME).objects.all()


class DomainsViewset(viewsets.ViewSet):
	def list(self, request):
		domains = getDomain()
		serializer = DomainsSerializer(domains, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		domains = getDomain(pk)
		serializer = DomainsSerializer(domains, many=True)
		return Response(serializer.data)

class ScansViewset(viewsets.ViewSet):
	def list(self, request):
		domains = getScantype()
		serializer = DomainsSerializer(domains, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		domains = getScantype(pk)
		serializer = DomainsSerializer(domains, many=True)
		return Response(serializer.data)