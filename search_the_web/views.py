# Search the Web - author: Mark Donald
#
# This software was written as a web services coding exercise.
#
# It is freeware, but if you intend to use it on a live site, please
# be careful. It is utterly unwarranted and unsupported. If it stops
# working it will not be fixed. Before using, you should also check
# the Alexa terms of service, which could have changed since I wrote
# this.

import os, httplib2, urllib, re, sys, oauth2, time, json
from xml.dom import minidom as xml

from django.shortcuts import render_to_response
from django.template import Context

from main.search_the_web.models import User
from exceptions import WebService, ResponseNotParsable
import config

# empty attribute tester for wrapped dictionaries

def actual(thing): return thing and True or False


# Alexa support

def getu(ip):
    try:
        user = User.objects.get(userip=ip)
    except User.DoesNotExist:
        user = User(userip=ip)
        user.save()
    return user

def arank(url, user):
    alexa = urllib.urlopen('http://xml.alexa.com/data?cli=10&dat=nsa&ver=quirk-searchstatus&uid=%s&userip=%s&url=%s'
                           % (user.uid.strftime('%Y%m%d%H%M%S'), user.userip, url))
    alexa_dom = xml.parseString(alexa.read())
    reach_elems = alexa_dom.getElementsByTagName('REACH') # or for a slightly different result - POPULARITY/TEXT
    alexa_rank = reach_elems and reach_elems[0].getAttribute('RANK') or '0'
    alexa_dom.unlink() # deallocate memory as early as possible, in case we're on a windoze server
    return alexa_rank


# mash function

def mash(ysearch_parsed, user, sort_instruction):
    results = []
    for result in ysearch_parsed['bossresponse']['web']['results']:
        # NOTE: potentially unsafe html tags included in data are stripped
        # by template parser, so no need to worry about them here
        results.append({
            'title':result['title'],
            'url':result['url'],
            'date':result['date'],
            'abstract':result['abstract'],
            'alexa_rank':arank(result['url'], user),
            # 'other_supported_rank':etc
        })
    if sort_instruction:
        results.sort(key=lambda result: int(result['%s_rank' % sort_instruction]), reverse=True)
    return results


# page generator

def search(request):
#    try:
        user = getu(request.META['REMOTE_ADDR'])
        f = request.GET
        results = None
        sort = None
        broadcast = (f.has_key('broadcast') and
                     actual(f['broadcast'])) and f['broadcast'] or None
        if f.has_key('q') and actual(f['q']):
            qbits = re.split('sort:\s*(\w*)', f['q'])
            if len(qbits) > 1:
                sort = qbits.pop(1).lower()
                if not sort in ['alexa']:
                    if not sort == 'yahoo':
                        broadcast = '%s rank not supported. Using default... (yahoo)' % sort.capitalize()
                    sort = None
                query = ' '.join([w.strip() for w in qbits]).strip()
            else:
                query = f['q']

            # oauth request payload
            url = 'http://yboss.yahooapis.com/ysearch/web?q='
            oauth_url = url + urllib.quote(query) # space -> '+' -> quote('+')
            consumer = oauth2.Consumer(**config.yboss)
            params = {
                'oauth_version':'1.0',
                'oauth_nonce':oauth2.generate_nonce(),
                'oauth_timestamp':int(time.time()),
            }
            oauth_request = oauth2.Request(method='GET', url=oauth_url, parameters=params)
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)
            oauth_header=oauth_request.to_header(realm='yahooapis.com')

            # yboss request/response
            http = httplib2.Http()
            response, content = http.request(oauth_url,
                                             'GET', headers=oauth_header)
            if response.status != 200:
                raise WebService('Response Code %s: %s' % (response.status,
                                                           response.reason))
            try:
                ysearch_dom = json.loads(content)
            except:
                raise ResponseNotParsable(content)

            # mash up search results with additional info
            results = mash(ysearch_dom, user, sort)

        args = Context({
            'results':results,
            'broadcast':broadcast,
            'q':f.has_key('q') and f['q'] or None
        })
        return render_to_response('results.html', args)

#    except ResponseNotParsable, e:
#        return HttpResponse(e)
#
#    except WebService, e:
#        return render_to_response('error.html', {'broadcast':'Unable to retrieve results... %s' % e})
#
#    except:
#        return render_to_response('error.html', {'broadcast':'Error processing result set...'})
