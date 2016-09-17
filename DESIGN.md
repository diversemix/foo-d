# Design
This document sets out the general design for the application and the rationale (give as quoted text) behind the descisions.

## General Architecture
The architecture chosen is that of a microservice.

One of the non-functional requirements is that this application is easy to use. To satisfy this requirement I have chosen to go with a web user interface.
> Using a web interface for an application is pretty much a defacto standard today and the UX is one most are familiar with.

The main functionality of the application is performed by the `foo-d-service`. This service will offer a RESTful API for any other service / application to consume.

> This is deliberately separated out from the webui although it could easily be combined. This is to preserve a separation of responsibilities - no least of all because the scaling of the foo-d-service is not dependant on the scaling for the webui. Either of these could be scaled by using HAProxy in-front of several instances in a round-robin fashion. Of course this can only be done if written in a stateless way.

## Choice of Technologies

* The `webui` uses Flask and bootstrap.
> I have chosen to use Flask for the web framework as it is a light and commonly used framework. Other alternatives could be Django, but that assumes a database so is unsuitable.
Bootstrap has been used as it gives some easy to build eye-candy out of the bag.

* The `foo-d-service` uses Flask.
> Again Flask has been chosen as it lightweight and easy to create a RESTful API with.

* Redis is used as the KV store.
> Redis has been chosen as writing your own KV storage in python is not suitable. Primarily because there is already a good one out there and there is no good reason not to use it. **Principle: Don't reinvent the wheel**

NOTE: Considerations if writing a KV store in python would be to cut down the memory footprint by using `__slots__`, also store the locations in some sort of btree ordered by both lat and long.
