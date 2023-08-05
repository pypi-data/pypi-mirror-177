# pylint: disable=R0913
"""
Defines all API endpoints for The One API (https://the-one-api.dev/v2).
"""
from typing import Optional

from .decorators import token_required
from .models import (
    BookResponse,
    MovieResponse,
    QuoteResponse,
    ChapterResponse,
    CharacterResponse,
)


class Endpoints:
    """
    Mixin class that calls the API routes for The One API.
    """

    def get_books(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> BookResponse:
        """
        List of all "The Lord of the Rings" books.
        Token required: no
        """
        resp = self._make_api_request(
            '/book',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        books = BookResponse(**resp)
        return books

    def get_book_by_id(self, book_id: str) -> BookResponse:
        """
        Request one specific book.
        Token required: no
        """
        resp = self._make_api_request(f'/book/{book_id}')
        book = BookResponse(**resp)
        return book

    def get_chapters_by_book_id(
        self,
        book_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> ChapterResponse:
        """
        Request all chapters of one specific book.
        Token required: no
        """
        resp = self._make_api_request(
            f'/book/{book_id}/chapter',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        chapter = ChapterResponse(**resp)
        return chapter

    @token_required
    def get_movies(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> MovieResponse:
        """
        List of all movies, including the
        "The Lord of the Rings" and the "The Hobbit" trilogies.
        Token required: yes
        """
        resp = self._make_api_request(
            '/movie',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        movies = MovieResponse(**resp)
        return movies

    @token_required
    def get_movie_by_id(self, movie_id: str) -> MovieResponse:
        """
        Request one specific movie.
        Token required: yes
        """
        resp = self._make_api_request(f'/movie/{movie_id}')
        movie = MovieResponse(**resp)
        return movie

    @token_required
    def get_quotes_by_movie_id(
        self,
        movie_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> QuoteResponse:
        """
        Request all movie quotes
        for one specific movie (only working for the LotR trilogy).
        Token required: yes
        """
        resp = self._make_api_request(
            f'/movie/{movie_id}/quote',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        quotes = QuoteResponse(**resp)
        return quotes

    @token_required
    def get_characters(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> ChapterResponse:
        """
        List of characters including metadata like name, gender, realm, race and more.
        Token required: yes
        """
        resp = self._make_api_request(
            '/character',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        characters = CharacterResponse(**resp)
        return characters

    @token_required
    def get_character_by_id(self, character_id: str) -> CharacterResponse:
        """
        Request one specific character.
        Token required: yes
        """
        resp = self._make_api_request(f'/character/{character_id}')
        character = CharacterResponse(**resp)
        return character

    @token_required
    def get_quotes_by_character_id(
        self,
        character_id: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> QuoteResponse:
        """
        Request all movie quotes of one specific character.
        Token required: yes
        """
        resp = self._make_api_request(
            f'/character/{character_id}/quote',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        quotes = QuoteResponse(**resp)
        return quotes

    @token_required
    def get_quotes(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> QuoteResponse:
        """
        List of all movie quotes.
        Token required: yes
        """
        resp = self._make_api_request(
            '/quote',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        quote = QuoteResponse(**resp)
        return quote

    @token_required
    def get_quote_by_id(self, quote_id: str) -> QuoteResponse:
        """
        Request one specific movie quote.
        Token required: yes
        """
        resp = self._make_api_request(f'/quote/{quote_id}')
        quote = QuoteResponse(**resp)
        return quote

    @token_required
    def get_chapters(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> ChapterResponse:
        """
        List of all book chapters.
        Token required: yes
        """
        resp = self._make_api_request(
            '/chapter',
            limit=limit,
            page=page,
            offset=offset,
            sort=sort,
            filter=filter,
        )
        chapter = ChapterResponse(**resp)
        return chapter

    @token_required
    def get_chapter_by_id(self, chapter_id: str) -> ChapterResponse:
        """
        Request one specific book chapter.
        Token required: yes
        """
        resp = self._make_api_request(f'/chapter/{chapter_id}')
        chapter = ChapterResponse(**resp)
        return chapter
