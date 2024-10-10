
class Movie:
    def __init__(self, title: str, description: str, rating: float):
        self.title = title
        self.description = description
        self.rating = rating
        
    def __eq__(self, other):
        return (self.title == other.title
                and self.description == other.description
                and self.rating == other.rating)

    def __dict__(self):
        return {
            'title': self.title,
            'description': self.description,
            'rating': self.rating
        }
