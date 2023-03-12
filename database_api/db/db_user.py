from database_api.db.models import User, Author
from database_api.schemas import UserBase, AuthorBase
from sqlalchemy.orm import Session

def create_author(request: AuthorBase, db: Session):
    new_author = Author(
        username = request.username,
        id = request.id,
        image_url = request.image_url
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def create_user(request: UserBase, db: Session):
    
    try: 
        _ = create_author(request, db)
    except:
        pass

    new_user = User(
        username = request.username,
        last_update = request.last_update
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user