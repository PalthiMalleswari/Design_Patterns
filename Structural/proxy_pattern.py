
#  Reference - https://algomaster.io/learn/lld/proxy
#  Refactoring Guru - https://refactoring.guru/design-patterns/proxy


"""
The Proxy Design Pattern is a structural pattern that provides a placeholder or surrogate 
for another object, allowing you to control access to it.
"""

#  Problem - Eager Loading
"""
Imagine you're building an image gallery application. Users can scroll through a list of image thumbnails,
and when they click on one, the full high-resolution image is displayed.
"""


from abc import ABC,abstractmethod
import time

class Image(ABC):

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def get_file_name(self):
        pass

class HighResolutionImage(Image):

    def __init__(self,file_name):
        
        self.file_name = file_name
        self.image_data = None
        self.load_image_from_disk()
    
    def get_file_name(self):
        
        return self.file_name
    
    def display(self):
        
        print(f"Displaying Image: {self.file_name}")
    
    def load_image_from_disk(self):

        print(f"Loading {self.file_name} from Disk")

        try:

            time.sleep(2)   # Simulate disk I/O Delay
            self.image_data = bytearray(10*1024*1024) # Simulate's 10 MB Memory Usage
        
        except KeyboardInterrupt:
            pass

        print(f"Image {self.file_name} Loaded")
    
class Application:

    def main():

        print("Application Started, Intializing images for gallery")

        img1 = HighResolutionImage("photo1.png")
        img2 = HighResolutionImage("photo2.png")
        img3 = HighResolutionImage("photo3.png")

        print("USer Viewing an Images")

        img1.display()

# if __name__ == "__main__":

#     Application.main()

#  Pitfalls of this implementation

"""
1.Resource-Intensive Initialization
2. No Control Over Access
"""

# Proxy Design Pattern

"""
The Proxy Design Pattern provides a stand-in or placeholder for another object to control access to it.
Instead of the client interacting directly with the “real” object (e.g., HighResolutionImage),
it interacts with a Proxy that implements the same interface.
"""

# Subject - Image Class
# Real Subject is - High Resolution Image Class
# Proxy Class

class ImageProxy(Image):

    def __init__(self,file_name):
        
        self.file_name = file_name
        self.real_image = None

    
    def get_file_name(self):
        
        return self.file_name
    
    def display(self):
        
        if self.real_image is None:

            print(f"ImageProxy: display() requested for {self.file_name}")
            self.real_image = HighResolutionImage(self.file_name)
        else:
            print(f"ImageProxy: Using Cached High Resolution Image for {self.file_name}")

        self.real_image.display()

#  Client Code

class ApplicationV2:

    def main():

        print("Application Started. Initializing image proxies for gallery...")

        img1 = ImageProxy("photo1.png")
        img2 = ImageProxy("photo2.png")
        img3 = ImageProxy("photo3.png")

        print(f"Gallery Intialized, No images loaded yet.")

        print(f"User Clicked on {img1.get_file_name()} Image")

        img1.display()

        print(f"User Clicked on {img3.get_file_name()} Image")

        img3.display()




if __name__ == "__main__":

    ApplicationV2.main()

# Insights of this Approach

"""
1. Lazy Loading : Only load when requested
2. Clean Interface (client code unaware of real or proxy object)
3. No code changes to real object
4. Reusability : Image Proxy can be reused for other optimizations like logging,caching
    or access control later
"""

# Extending with Other Proxy Types

# 1. Virtual Proxy

"""
Lazy initialization (virtual proxy). This is when you have a heavyweight service object that wastes system resources by being always up,
even though you only need it from time to time.Instead of creating the object when the app launches, you can delay the object’s 
initialization to a time when it’s really needed
"""


# 2. Protection Proxy

"""
Access Control : This is when you want only specific clients to be able to use the service object; for instance, when your objects are crucial parts of an operating system
and clients are various launched applications (including malicious ones).The proxy can pass the request to the service object only 
if the client’s credentials match some criteria.
"""

#  3. Logging Proxy

"""
Logging requests: This is when you want to keep a history of requests to the service object.
The proxy can log each request before passing it to the service.
"""

#  4. Caching Proxy

"""
Caching request results:This is when you need to cache results of client requests and manage the life cycle of this cache, especially if results are quite large.
The proxy can implement caching for recurring requests that always yield the same results. The proxy may use the parameters of requests as the cache keys.
"""

#  Smart reference

"""
The proxy can keep track of clients that obtained a reference to the service object or its results. From time to time, the proxy may go over the clients
and check whether they are still active. If the client list gets empty, the proxy might dismiss the service object and free the underlying system resources.
"""



#  Protection Proxy Example

class ImageProxy(Image):

    def __init__(self,file_name):
        
        self.file_name = file_name
        self.real_image = None

    
    def get_file_name(self):
        
        return self.file_name
    
    #  a method to check the permissions

    def check_user_access(self,user_role):

        print(f"ImageProxy Checking Access to {user_role}")

        return True if user_role == "Admin" else False
    
    def display(self,user_role):

        if not self.check_user_access(user_role):
            
            print(f"ProtectionProxy: Access Denied for {self.file_name}")

        if self.real_image is None:

            print(f"ImageProxy: display() requested for {self.file_name}")
            self.real_image = HighResolutionImage(self.file_name)
        
        else:
            print(f"ImageProxy: Using Cached High Resolution Image for {self.file_name}")

        self.real_image.display()

#  Logging Proxy Examples

from datetime import datetime

#  Will have logs before and after calling real service class
def display(self):
    print(f"LoggingProxy: Attempting to display {self.file_name} at {datetime.now()}")

    if self.real_image is None:
        print("ImageProxy: Lazy-loading image...")
        self.real_image = HighResolutionImage(self.file_name)

    self.real_image.display()

    print(f"LoggingProxy: Finished displaying {self.file_name} at {datetime.now()}")



# ================ Rate Limiting Proxy ==============

"""
In-Process Rate-Limiting  
"""

from collections import defaultdict,deque

class ApiService:

    def handle_request(self,user_id):

        print(f"Processing request for user id {user_id}")

class RateLimitingService:

    """
    Max 3 requests per user per 10 seconds
    """
    def __init__(self,service,limit=3,window=10):
        
        self.limit = limit
        self.window = window
        self.service = service
        self.requests = defaultdict(deque)
    
    def handle_request(self,user_id):

        now = time.time()

        user_requests = self.requests[user_id]

        #  Remove expired requests
        
        while user_requests and now-user_requests[0] >= self.window:
            # import pdb;pdb.set_trace()
            user_requests.popleft()
        
        if len(user_requests) >= self.limit:

            raise Exception("Rate limit exceeded")
        
        user_requests.append(now)
        self.service.handle_request(user_id)


# Application

if __name__ == "__main__":

    serice = ApiService()
    ratelimitproxy = RateLimitingService(serice)

    for i in range(14):
        try:
            ratelimitproxy.handle_request("user123")
            
        except Exception as e:
            print(e)
        time.sleep(1)


    
