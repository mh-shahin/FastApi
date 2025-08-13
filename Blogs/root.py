from pyexpat import model
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# get operation 

@app.get("/get")
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# get operation with responsive model. that means i can rettrive specific data. 
@app.get("/get/{id}", status_code=200, response_model= schemas.showBlog)
def specificBlog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Details": f"Blog with the {id} is not available"}
    return blog

# this is delete operation
@app.delete("/get/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "Done"

# this is update operation for specific blog or element
@app.put("/get/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")

    blog_query.update(request.model_dump())  # Convert Pydantic model to dict
    db.commit()
    return {"message": "Updated successfully"}
