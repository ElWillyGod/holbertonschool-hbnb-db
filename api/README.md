# Services Layer
---

## What
  This layer aims to provide an interface where the user can interact with.

## How
  To establish connections we use the Flask framework, where we define each
endpoint in a blueprint and attach them later to an app. To authenticate we
use a framework made for Flask that enables JWT. We create an instance of a
JWT manager, attach it with some stuff and pass it around for those endpoints
that need authorization. JWT also checks if the given token has admin
priviledges. At last we use Flassger (Flask + Swagger) to place a comprehensive
API documentation.

  We need to clarify that this layer calls the BL and the persistance layer,
so there is no need to call them one by one by a manager.

## How to use
  In the \_\_init\_\_.py file we define the factory pattern function for the
app, but we do not call it right there. It must be made and runned where it is
called.
