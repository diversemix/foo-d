# Design
This document sets out the general design for the application and the rationale (give as quoted text) behind the descisions.

## General Architecture
The architecture chosen is that of a microservice.
> This may seem a little over-engineered and I certainly wouldn't necessarily solve the problem this way in a work situation as there are many other commercial factors to consider. However solving it in this way does give you a chance to see what can be done with the given technologies and hopefully you may learn something.

One of the non-functional requirements is the application be easy to use. To satisfy this requirement I have chosen to go with a web user interface.
> Using a web interface for an application is pretty much a defacto standard today and the UX is one most are familiar with. I have also chosen to go with bootstrap and jQuery (although its not currently used I would like to later put in an AJAX call to dynamically update the search results). The UI design is very basic and certainly I am not a UX designer and would always delegate that task to those skilled in this field.

The main functionality of the application is to search for pubs within a given radius. This task is performed by the `foo-d-service`.The data is loaded in via two CSV files, one that contains positional data for postcodes and one that contains the list of pubs and their respective postcode. This service will offer a RESTful API for any other service(s) / application(s) to consume. In our case it will be the web UI.

> This is deliberately separated out from the webui although it could easily be combined. This is to preserve a separation of responsibilities - no least of all because the scaling of the foo-d-service is not dependant on the scaling for the webui. Either of these could be scaled by using HAProxy in-front of several instances in a round-robin fashion. Of course this can only be done if written in a stateless way.

## Choice of Technologies

* The `webui` uses Flask and bootstrap.
> I have chosen to use Flask for the web framework as it is a light and commonly used framework. Other alternatives could be Django, but that assumes a database so is unsuitable.
Bootstrap has been used as it gives some easy to build eye-candy out of the bag.

* The `foo-d-service` uses Flask.
> Again Flask has been chosen as it lightweight and easy to create a RESTful API with.

* Redis is used as the KV store.
> Redis has been chosen as writing your own KV storage in python is not suitable. Primarily because there is already a good one out there and there is no good reason not to use it. **Principle: Don't reinvent the wheel**
**NOTE:** Considerations if writing a KV store in python would be to cut down the memory footprint by using `__slots__`, also store the locations in some sort of btree ordered by both lat and long. However I could not possibly provide as good a quality of solution as using redis (see next point).

* Redis to calculate distances.
> Taken from their site (http://redis.io/commands/geoadd) What Earth model does it use?
It just assumes that the Earth is a sphere, since the used distance formula is the Haversine formula. This formula is only an approximation when applied to the Earth, which is not a perfect sphere. The introduced errors are not an issue when used in the context of social network sites that need to query by radius and most other applications. However in the worst case the error may be up to 0.5%, so you may want to consider other systems for error-critical applications.

## Future Enhancements

* The use of the Google Maps API - the distances calculated currently are "as the crow flies" this does not take into account things like rivers, roads etc that is more real world. Using the Google Maps API would mean that the *actual* distances could be measured and therefore be of more use.

* More tests - there are one or two tests in here, but no where near enough for production quality. Any code that goes into production should have enough tests in that any developer working on the code would feel confident that any bugs they introduce through any change they make would be picked up. Tests also mean that you can progress to Continuous Integration and then to Dontinuous Deployment. (see https://github.com/diversemix/beefpi )

* More testing - there are issues with the code, but that is a reflection of its maturity.
