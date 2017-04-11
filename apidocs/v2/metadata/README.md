# V2 Metadata API

This is the Swagger file that defines the general API for retrieving metadata information from the Data Hub back end.

In Data Hub terms, metadata is data that does not require creation, updating or deletion as part of the normal lifecycle of the application, so can be safely consumed at load and kept in memory.

Metadata is nearly always an array of objects consisting of a UUID id and a string name. There is one exception however: ordered metadata.

## Ordered metadata

A couple of the metadata tables require the front end to display t
hem in a specific order, and that ordered cannot easily be inferred from the data itself (at least by a computer); these therefore have a third element to each object - an explicit order that allows the front end to display things in the order they were intended without complex parsing.