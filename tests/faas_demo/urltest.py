from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Example usage:
url = 'https://openaitrials.openai.azure.com/completions'
if is_valid_url(url):
    print(f'The URL {url} is valid.')
else:
    print(f'The URL {url} is not valid.')
