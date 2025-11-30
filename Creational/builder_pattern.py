# Reference : https://algomaster.io/learn/lld/builder

"""
The Builder Design Pattern is a creational pattern that lets you construct complex objects step-by-step,
separating the construction logic from the final representation.
It’s particularly useful in situations where:
    . An object requires many optional fields, and not all of them are needed every time.
    . You want to avoid telescoping constructors or large constructors with multiple parameters.
    . The object construction process involves multiple steps that need to happen in a particular order.
"""

#1. The Problem: Building Complex HttpRequest Objects

"""
magine you're building a system that needs to configure and create HTTP requests.
Each HttpRequest can contain a mix of required and optional fields depending on the use case.
"""

# The Naive Approach: Telescoping Constructors
"""
A common approach is to use constructor overloading often referred to as the telescoping constructor anti-pattern.
"""

class HttpRquestTelescoping:

    def __init__(self,url,method="GET",headers=None,query_params=None,body=None,timeout=300):

        self.url = url
        self.method = method
        self.headers = headers if headers else {}
        self.query_params = query_params if query_params else {}
        self.body = body
        self.timeout = timeout

        print(f"HttpRequest Created: URL={url}, "
              f"Method={method}, "
              f"Headers={len(self.headers)}, "
              f"Params={len(self.query_params)}, "
              f"Body={body is not None}, "
              f"Timeout={timeout}")



# Client Code

if __name__ =="__main__":

    req1 = HttpRquestTelescoping("https://api.example.com/data")

    req2 = HttpRquestTelescoping("https://api.example.com/data",
                                 "POST",None,None,'{"key":"value"}')
    
    req3 = HttpRquestTelescoping("https://api.example.com/data",
                                 "PUT",
                                 {"X-API-Key":"Secret"},
                                 None,
                                 "config_data",5000),


# What’s Wrong with This Approach?

"""
1. Hard to Read and Write
    Multiple parameters of the same type (e.g., String, Map) make it easy to accidentally swap arguments.
2. Error-Prone
    Clients must pass null for optional parameters they don’t want to set, increasing the risk of bugs.
3. Inflexible and Fragile
    If you want to set parameter 5 but not 3 and 4, you’re forced to pass null for 3 and 4.
    You must follow the exact parameter order, which hurts readability and usability.
"""

# The Builder pattern separates the construction of a complex object from its representation.

"""
In the Builder Pattern:

The construction logic is encapsulated in a Builder.
The final object (the "Product") is created by calling a build() method.
The object itself typically has a private or package-private constructor, forcing construction through the builder.
"""

## Implementing Builder

class HttpRequest:

    def __init__(self,builder):

        self.url = builder.url
        self.method = builder.http_method
        self.headers = builder.headers
        self.query_params = builder.query_params
        self.body = builder.http_body
        self.timeout = builder.http_timeout
    
    def __str__(self):
        return (f"HttpRequest(url={self.url}, method={self.method}, headers={self.headers}, "
                f"query_params={self.query_params}, body={self.body}, timeout={self.timeout})")

    class Builder:

        def __init__(self,url):
            
            self.url = url
            self.http_method = "GET"
            self.headers = {}
            self.query_params = {}
            self.http_body = None
            self.http_timeout = 300
        
        def method(self,method):
            
            self.http_method = method
            return self     # Return builder instance for chaining 
        
        def add_header(self,key,value):

            self.headers[key] = value
            return self
        
        def add_query_param(self,key,value):
            self.query_params[key] = value
            return self
        
        def body(self,body):
            self.http_body = body
            return self
        
        def timeout(self,timeout):
            self.http_timeout = timeout
            return self

        def build(self):
            return HttpRequest(self)
    

if __name__ == "__main__":

    req1 = HttpRequest.Builder("https://api.example.com/data").build()

    req2 = HttpRequest.Builder("https://api.example.com/data") \
            .method("POST") \
            .body('{"key":"value"}')\
            .timeout(1500)\
            .build()
    
    ## Method chaining
    
    req3 = HttpRequest.Builder("https://api.example.com/config") \
        .method("PUT") \
        .add_header("X-API-Key", "secret") \
        .add_query_param("env", "prod") \
        .body("config_payload") \
        .timeout(5000) \
        .build()

    print(req1)
    print(req2)
    print(req3)


