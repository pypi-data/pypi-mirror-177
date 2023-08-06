"""
Buscar uma  categoria
"""


# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.get.input import GetCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.get.output import GetCategoryOutput


class GetCategoryUseCase(UseCase[GetCategoryInput, GetCategoryOutput]):
    """
    Classe para criar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository) -> None:
        self.repo = repo

    def execute(self, input_params: GetCategoryInput) -> GetCategoryOutput:
        category = self.repo.find_by_id(input_params.id)
        return self.__to_output(category=category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(klass=GetCategoryOutput, category=category)
