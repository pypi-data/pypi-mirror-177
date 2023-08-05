# kyle_degennaro-SDK

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install The One API SDK.

```bash
pip install --upgrade pip
pip install kyle_degennaro-sdk
```

## Usage

```python
from lotr.client import Client

client = Client()
books = client.get_books()

# For endpoints that require authentication
# pass an access token to the Client or set an
# environment variable, ACCESS_TOKEN with your token.
access_token = 'ACCESS_TOKEN'
client = Client(access_token)

# Basic usage
data = client.get_books()
print(data.books)

book_id = data.books[0].id
data = client.get_chapters_by_book_id(book_id, limit=2)
print(data.chapters)

data = client.get_quotes(filter="dialog=Deagol!")
print(data.quotes)

data = client.get_movies(filter='runtimeInMinutes>200')
print(data.movies)

data = client.get_characters(limit=20, page=3, sort='name:asc', filter='race=Human')
print(data.characters)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)