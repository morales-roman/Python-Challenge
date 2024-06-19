"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    if prefix:
        kwargs['Prefix'] = prefix

    while True:
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                yield obj
        next_token = resp.get('NextContinuationToken', None)
        if not next_token:
            break
        kwargs['ContinuationToken'] = next_token

"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):
    '''
    This function processes a list of items and extensions to return a consolidated list of dictionaries that at least includes the item ID and their quantities.
    '''
    items = [] # List to contain all processed items
    sp = False # Boolean flag to acknowledge if an item is the main plan/special plan
    cd = False # Boolean flag to acknowledge if an item was deleted/cancelled

    ext_p = {} # Dictionary to map extension prices to their quantities

    # Iterate over the extensions to map the prices id to their quantities
    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    # Iterate over the items to process them
    for item in obj['items'].data:
        product = {
            'id': item.id
        }

        if item.price.id != main_plan.id and item.price.id not in ext_p:
            # If the item is not the main plan and it is not in the prices-quantity dictionary, mark it as deleted
            product['deleted'] = True
            cd = True
        elif item.price.id in ext_p:
            # If the item is in the prices-quantity dictionary, check if the quantity is less than 1, mark it as deleted, if not set its quantity
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty
            # Remove the item from the prices-quantity dictionary
            del ext_p[item.price.id]
        elif item.price.id == main_plan.id:
            # If the item is the main plan, set the special plan flag to True
            sp = True


        items.append(product)
    if not sp:
        # If the main plan was not found in the items, add it to the list
        items.append({
            'id': main_plan.id,
            'qty': 1
        })
    
    # Add the remaining items from the prices-quantity dictionary to the list if their quantity is greater than 0
    for price, qty in ext_p.items():
        if qty < 1:
            continue
        items.append({
            'id': price,
            'qty': qty
        })
    
    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args):
    return Caller.__dict__[fn_to_call](*args)   

"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    '''
    This function detects the aspect ratio of a video based on its width and height and returns the corresponding preset configuration.
    '''
    v = None # Variable to store the preset configuration
    ar = w / h # Calculate the aspect ratio of the video

    if ar < 1:
        # If the aspect ratio is less than 1, return the preset configuration for portrait videos
        v = [r for r in config['p'] if r['width'] <= w] 
    elif ar > 4 / 3:
        # If the aspect ratio is greater than 4/3, return the preset configuration for landscape videos
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        # Otherwise, return the preset configuration for square videos
        v = [r for r in config['s'] if r['width'] <= w]

    # Return the preset configuration
    return v

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def process_request(self, method, endpoint, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']
        headers = {
            'Authorization': f'{token_type} {access_token}',
        }
        send = {
            'headers': headers,
            'params': kwargs
        }
        URL = f'{self.DOMAIN}/{endpoint}'

        response = getattr(requests, method)(URL, **send)
        return response

    def search_images(self, **kwargs):
        return self.process_request('get', self.SEARCH_IMAGES_ENDPOINT, **kwargs)
        
    def get_image(self, image_id, **kwargs):
        return self.process_request('get', self.GET_IMAGE_ENDPOINT, **kwargs)

    def download_image(self, image_id, **kwargs):
        return self.process_request('post', self.DOWNLOAD_IMAGE_ENDPOINT, **kwargs)

