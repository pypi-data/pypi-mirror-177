"""
Models for The One API (https://the-one-api.dev/v2).
"""
from typing import List, Optional

from pydantic import BaseModel, Field  # pylint: disable=E0611


class DocBase(BaseModel):
    """
    Base model for the MongoDB document.
    """

    id: str = Field(alias='_id')


class ResponseBase(BaseModel):
    """
    Base model for the JSON response returned by the API.
    """

    total: int
    limit: int
    offset: Optional[int] = Field(alias='offset')
    page: int
    pages: int


class Book(DocBase):
    """
    Model for defining a book.
    """

    name: str


class BookResponse(ResponseBase):
    """
    Model for defining the response for the book resource.
    """

    books: List[Book] = Field(alias='docs')


class Chapter(DocBase):
    """
    Model for defining a Chapter.
    """

    chapter_name: str = Field(alias='chapterName')


class ChapterResponse(ResponseBase):
    """
    Model for defining the response for the chapter resource.
    """

    chapters: List[Chapter] = Field(alias='docs')


class Movie(DocBase):
    """
    Model for defining a movie.
    """

    name: str
    runtime_in_minutes: int = Field(alias='runtimeInMinutes')
    budget_in_millions: int = Field(alias='budgetInMillions')
    box_office_revenue_in_millions: int = Field(
        alias='boxOfficeRevenueInMillions'
    )
    academy_award_nominations: int = Field(alias='academyAwardNominations')
    academy_award_wins: int = Field(alias='academyAwardWins')
    rotten_tomatoes_score: int = Field(alias='rottenTomatoesScore')


class MovieResponse(ResponseBase):
    """
    Model for defining the response for the movie resource.
    """

    movies: List[Movie] = Field(alias='docs')


class Quote(DocBase):
    """
    Model for defining a quote.
    """

    dialog: str = Field(alias='dialog')
    movie_id: str = Field(alias='movie')
    character_id: str = Field(alias='character')


class QuoteResponse(ResponseBase):
    """
    Model for defining the response for the quote resource.
    """

    quotes: List[Quote] = Field(alias='docs')


class Character(DocBase):
    """
    Model for defining a character.
    """

    height: str = Field(alias='height')
    race: str = Field(alias='race')
    gender: Optional[str] = Field(alias='gender')
    birth: str = Field(alias='birth')
    spouse: str = Field(alias='spouse')
    death: str = Field(alias='death')
    realm: str = Field(alias='realm')
    hair: str = Field(alias='hair')
    name: str = Field(alias='name')
    wiki_url: Optional[str] = Field(alias='wikiUrl')


class CharacterResponse(ResponseBase):
    """
    Model for defining the response for the character resource.
    """

    characters: List[Character] = Field(alias='docs')
