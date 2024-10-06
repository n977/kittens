from kittens.models.color import ColorCreate
from kittens.models.breed import BreedCreate
from kittens.models.kitten import KittenCreate
from kittens.models.user import UserCreate
from kittens.repos.color import ColorRepo
from kittens.repos.breed import BreedRepo
from kittens.repos.kitten import KittenRepo
from kittens.repos.user import UserRepo


def test_color_repo_save(colors: ColorRepo) -> None:
    color = ColorCreate(name="TEST_VALUE")
    colors.save(color)
    assert len(colors.list()) == 1

    # Save a duplicate.
    assert not colors.save(color)


def test_breed_repo_save(breeds: BreedRepo) -> None:
    breed = BreedCreate(name="TEST_VALUE")
    breeds.save(breed)
    assert len(breeds.list()) == 1

    # Save a duplicate.
    assert not breeds.save(breed)


def test_kitten_repo_save(
    kittens: KittenRepo, colors: ColorRepo, breeds: BreedRepo
) -> None:
    color = ColorCreate(name="TEST_VALUE")
    assert colors.save(color)
    _color = colors.list()[0]
    breed = BreedCreate(name="TEST_VALUE")
    assert breeds.save(breed)
    _breed = breeds.list()[0]
    kitten = KittenCreate(color_id=_color.id, age=0, breed_id=_breed.id, description="TEST_VALUE")  # type: ignore
    assert kittens.save(kitten)
    assert len(kittens.list()) == 1


def test_user_repo_save(users: UserRepo) -> None:
    user = UserCreate(username="TEST_VALUE", password="TEST_VALUE")
    assert users.save(user)
    _users = users.list()
    assert len(_users) == 1

    # Verify if the password was properly hashed.
    assert not users.verify(_users[0], "TEST_VALUE_INVALID")
    assert users.verify(_users[0], "TEST_VALUE")

    # Save a duplicate.
    assert not users.save(user)
