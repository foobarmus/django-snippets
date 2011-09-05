# Search the Web - author: Mark Donald
#
# This software was written as a web services coding exercise.
#
# It is freeware, but if you intend to use it on a live site, please
# be careful. It is utterly unwarranted and unsupported. If it stops
# working it will not be fixed. It may contain code that violates
# the terms of service of various websites.
#
# I hereby indemnify myself against the actions of anyone who uses
# it for any purpose other than assessing my programming skills.

import os, httplib, urllib, re, sys
import xml.dom.minidom as xml

from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse # can remove after yboss revamp - only used by ResponseNotParsable

from main.search_the_web.models import User
from exceptions import WebService, ResponseNotParsable
#import config
import django_oauth_consumer

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


# result generator - Yahoo BOSS

def mash(ysearch_dom, user, sort_instruction):
    results = []
    raw_results = ysearch_dom.getElementsByTagName('result')
    for result in raw_results:
        # NOTE: potentially unsafe html tags included in CDATA nodes are stripped
        # by template parser, so no need to worry about them here
        url = result.getElementsByTagName('url')[0].firstChild.data
        title_node = result.getElementsByTagName('title')[0].firstChild
        date_node = result.getElementsByTagName('date')[0].firstChild
        abstract_node = result.getElementsByTagName('abstract')[0].firstChild
        results.append({
            'title':title_node and title_node.data or '', # presence checks required for all except url
            'url':url,
            'date':date_node and date_node.data or '',
            'abstract':abstract_node and abstract_node.data or '',
            'alexa_rank':arank(url, user)
        })
    ysearch_dom.unlink()
    if sort_instruction:
        results.sort(key=lambda result: int(result['%s_rank' % sort_instruction]), reverse=True)
    return results


# page generator

def search(request):
#    try:
        user = getu(request.META['REMOTE_ADDR'])
        f = request.GET
        results = None
        broadcast = (f.has_key('broadcast') and actual(f['broadcast'])) and f['broadcast'] or None
        if f.has_key('q') and actual(f['q']):
            qbits = re.split('sort:\s*(\w*)', f['q'])
            if len(qbits) > 1:
                f['sort'] = qbits.pop(1).lower()
                if not f['sort'] in ['alexa']:
                    if not f['sort'] == 'yahoo':
                        broadcast = '%s rank not supported. Using default... (yahoo)' % f['sort'].capitalize()
                    f.sort = None
                query = ' '.join([w.strip() for w in qbits]).strip()
            else:
                query = f['q']

            cx = httplib.HTTPConnection('boss.yahooapis.com')
            cx.request('GET', '/ysearch/web/v1/%s?format=xml&appid=%s' % (urllib.quote_plus(query), ''))#config.appid))
            response = cx.getresponse()
            if response.status != 200:
                raise WebService('Response Code %s: %s' % (response.status, response.reason))
            raw = response.read()
            try:
                ysearch_dom = xml.parseString(raw)
            except:
                raise ResponseNotParsable(raw)
            results = mash(ysearch_dom, user, f['sort'])

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
