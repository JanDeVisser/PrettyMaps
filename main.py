#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

if __name__ == '__main__':
    import gripe
    gripe.add_app_dir("prettymaps", __file__)

    import grit
    app = grit.app

    import webapp2
    import gripe
    import grumble
    import grumble.image

    import prettymaps

    request = webapp2.Request.blank('/')
    response = request.get_response(app)
    # print response
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status

    cookie = response.headers["Set-Cookie"]
    parts = cookie.split(";")
    cookie = parts[0]

    request = webapp2.Request.blank("/login")
    request.headers['Cookie'] = cookie
    print request.cookies['grit']
    response = request.get_response(app)
    # print response
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    print "Requested /login and got OK"

    request = webapp2.Request.blank("/login")
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.POST["userid"] = "jan@de-visser.net"
    request.POST["password"] = "wbw417"
    request.POST["remember"] = "X"
    response = request.get_response(app)
    # print response
    assert response.status_int == 302, "Expected 302 Moved Temporarily, got %s" % response.status
    location = response.headers["Location"]
    assert location == "http://localhost/", "Expected to be redirected to 'http://localhost:8080/', got '%s' instead" % location
    print "POSTed login data and got redirected to /"

    request = webapp2.Request.blank(location)
    request.headers['Cookie'] = cookie
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    # print response.body
    # assert re.match(u"Really", response.body)
    print "Requested / and got OK"

    request = webapp2.Request.blank("/image/throbber.gif")
    request.headers['Cookie'] = cookie
    response = request.get_response(app)
    assert response.status_int == 200, "/image/throbber.gif: Expected 200 OK, got %s" % response.status
    print "Requested /image/throbber.gif and got OK"

    request = webapp2.Request.blank("/css/grizzle.css")
    request.headers['Cookie'] = cookie
    response = request.get_response(app)
    assert response.status_int == 200, "/css/grizzle.css: Expected 200 OK, got %s" % response.status
    print "Requested /css/grizzle.css and got OK"

    request = webapp2.Request.blank("/json/project", POST = '{ "project_name": "Baden Duathlon", "description": "Baden Duathlon" }')
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    project = d["data"][0]["key"]
    print "Created Project and got OK. Project key:", project

    request = webapp2.Request.blank("/json/project/%s" % project)
    request.headers['Cookie'] = cookie
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    d = d["data"]
    print "Requested Project and got OK"

    descr = d["description"]
    d["description"] = descr + " XX"
    request = webapp2.Request.blank("/json/project")
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    request.json = d
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    print "Updated Project and got OK"

    d["description"] = descr
    request = webapp2.Request.blank("/json/project")
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    request.json = d
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    print "Updated Project and got OK"

    request = webapp2.Request.blank("/json/map",
        POST='{ "parent": "%s", "map_name": "Run Course", "description": "Baden Duathlon Run 1 Course" }' % project)
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    run_map = d["data"][0]["key"]
    print "Created Run Map and got OK. Map key:", run_map

    request = webapp2.Request.blank("/json/map",
        POST='{ "parent": "%s", "map_name": "Bike Course", "description": "Baden Duathlon Bike Course" }' % project)
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    bike_map = d["data"][0]["key"]
    print "Created Bike Map and got OK. Map key:", bike_map

    request = webapp2.Request.blank("/json/map",
        POST='{ "parent": "%s", "map_name": "7 Miler", "description": "Baden Road Races 7 Miler" }' % project)
    request.headers['Cookie'] = cookie
    request.method = "POST"
    request.content_type = "application/x-www-form-urlencoded"
    request.charset = "utf8"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    seven_miler_map = d["data"][0]["key"]
    print "Created Seven Miler Map and got OK. Map key:", seven_miler_map

    request = webapp2.Request.blank("/json/map/%s" % run_map)
    request.headers['Cookie'] = cookie
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    d = response.json
    d = d["data"]
    print "Requested Run Map and got OK"

    with open("test/BadenDuRun1.gpx", "rb") as fh:
        gpx = fh.read()
    request = webapp2.Request.blank("/gpx/%s" % run_map, POST = { "image": ("BadenDuRun1.gpx", gpx) })
    request.headers['Cookie'] = cookie
    request.method = "POST"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    print "Uploaded Run GPX document and got OK"

    with open("test/BadenDuBike.gpx", "rb") as fh:
        gpx = fh.read()
    request = webapp2.Request.blank("/gpx/%s" % bike_map, POST = { "image": ("BadenDuBike.gpx", gpx) })
    request.headers['Cookie'] = cookie
    request.method = "POST"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    print "Uploaded Bike GPX document and got OK"

    with open("test/Baden7Miler.gpx", "rb") as fh:
        gpx = fh.read()
    request = webapp2.Request.blank("/gpx/%s" % seven_miler_map, POST = { "image": ("BadenDuBike.gpx", gpx) })
    request.headers['Cookie'] = cookie
    request.method = "POST"
    response = request.get_response(app)
    assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    print "Uploaded Seven Miler GPX document and got OK"

    #
    # try:
    #     os.remove("image/Desert_1.jpg")
    # except:
    #     pass
    #
    # request = webapp2.Request.blank("/img/test/icon/%s" % k)
    # request.headers['Cookie'] = cookie
    # response = request.get_response(app)
    # assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    # etag = response.etag
    # with open("%s/image/Desert_1.jpg" % gripe.root_dir(), "wb") as fh:
    #     fh.write(response.body)
    # print "Downloaded Test image and got OK"
    #
    # request = webapp2.Request.blank("/img/test/icon/%s" % k)
    # request.headers['Cookie'] = cookie
    # request.if_none_match = etag
    # response = request.get_response(app)
    # assert response.status_int == 304, "Expected 304 Not Modified, got %s" % response.status
    # print "Downloaded Test image again and got Not Modified"
    #
    # with open("%s/image/Koala.jpg" % gripe.root_dir(), "rb") as fh:
    #     img = fh.read()
    # request = webapp2.Request.blank("/img/test/icon/%s" % k, POST = { "contentType": "image/jpeg", "image": ("Koala.jpg", img) })
    # request.headers['Cookie'] = cookie
    # request.method = "POST"
    # response = request.get_response(app)
    # assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    # print "Updated Test with new image and got OK"
    #
    # request = webapp2.Request.blank("/img/test/icon/%s" % k)
    # request.headers['Cookie'] = cookie
    # request.if_none_match = etag
    # response = request.get_response(app)
    # assert response.status_int == 200, "Expected 200 OK, got %s" % response.status
    # print "Downloaded new Test image and got OK"

#    request = webapp2.Request.blank("/json/test/%s" % k)
#    request.headers['Cookie'] = "grit=%s" % cookie
#    request.method = "DELETE"
#    response = request.get_response(app)
#    assert response.status_int == 200, "Expected OK"

    print "all done"
