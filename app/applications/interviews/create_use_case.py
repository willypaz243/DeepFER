from app.domain.interfaces.use_case import UseCase


class CreateUseCase(UseCase):
    def __init__(self, repository):
        self.repository = repository

    def run(self):
        return super().run()