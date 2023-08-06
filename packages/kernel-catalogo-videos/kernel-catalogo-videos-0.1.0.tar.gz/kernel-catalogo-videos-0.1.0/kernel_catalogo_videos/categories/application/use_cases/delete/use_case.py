"""
Caso de uso para criar uma categoria
"""


# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.delete.input import DeleteCategoryInput


class DeleteCategoryUseCase(UseCase[DeleteCategoryInput, None]):
    """
    Classe para deletar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository) -> None:
        self.repo = repo

    def execute(self, input_params: DeleteCategoryInput) -> None:
        # pylint: disable=unexpected-keyword-arg
        self.repo.delete(input_params.id)
