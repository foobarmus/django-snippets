# Copyright (c) 2011, Mark Donald
# All rights reserved.
# 
# This software was written as a web services coding exercise.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Furthermore, if you intend to use it on a live site, you should check the
# Alexa toolbar terms of service, which may have changed since the time of
# writing.

import os, httplib2, urllib, re, oauth2, time
from xml.dom import minidom as xml

from django.shortcuts import render_to_response
from django.template import Context
from django.utils import simplejson as json

from django_snippets.search_the_web.models import User
from exceptions import WebService, UserDoesNotExist
import config


# Alexa support

def getu(ip):
    try:
        user = User.gql('WHERE userip = :1', ip).get()
        if not user:
            raise UserDoesNotExist
    except UserDoesNotExist:
        user = User(userip=ip)
        user.put()
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
    return results[:10]


# page generator

def search(request):
    try:
        user = getu(request.META['REMOTE_ADDR'])
        f = request.GET
        results = None
        sort = None
        broadcast = (f.has_key('broadcast') and f['broadcast']) and f['broadcast'] or None
        if f.has_key('q') and f['q']:
            qbits = re.split('sort:\s*(\w*)', f['q'])
            if len(qbits) > 1:
                sort = qbits.pop(1).lower()
                if not sort in ['alexa']: # , 'other_supported_rank', 'etc']
                    if not sort == 'yahoo':
                        broadcast = '%s rank not supported. Using default... (yahoo)' % sort.capitalize()
                    sort = None
                query = ' '.join([w.strip() for w in qbits]).strip()
            else:
                query = f['q']

            # oauth request payload
            url = 'http://yboss.yahooapis.com/ysearch/web?q=%s' % urllib.quote(query)
            consumer = oauth2.Consumer(**config.yboss)
            params = {
                'oauth_version':'1.0',
                'oauth_nonce':oauth2.generate_nonce(),
                'oauth_timestamp':int(time.time()),
            }
            oauth_request = oauth2.Request(method='GET', url=url, parameters=params)
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)
            oauth_header=oauth_request.to_header(realm='yahooapis.com')

            # yboss request/response
            http = httplib2.Http()
            response, content = http.request(url, 'GET', headers=oauth_header)
            if response.status != 200:
                raise WebService('Response Code %s: %s' % (response.status,
                                                           response.reason))

            # mash up search results with additional info
            ysearch_dom = json.loads(content)
            results = mash(ysearch_dom, user, sort)

        args = Context({
            'results':results,
            'broadcast':broadcast,
            'q':f.has_key('q') and f['q'] or None
        })
        return render_to_response('results.html', args)

    except WebService, e:
        return render_to_response('error.html', {'broadcast':'Unable to retrieve results... %s' % e})

    except:
        return render_to_response('error.html', {'broadcast':'Error processing result set...'})
